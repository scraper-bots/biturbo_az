#!/usr/bin/env python3
"""
Biturbo.az Car Listings Scraper (Async Version)
Scrapes car listings and detailed information from biturbo.az using asyncio and aiohttp for faster performance
"""

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BiturboScraperAsync:
    def __init__(self, max_concurrent=50):
        self.base_url = "https://www.biturbo.az"
        self.max_concurrent = max_concurrent
        self.session = None

        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(limit=self.max_concurrent, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def get_page(self, url, semaphore, retries=3):
        """Get page content with error handling and retries"""
        async with semaphore:
            for attempt in range(retries):
                try:
                    async with self.session.get(url) as response:
                        response.raise_for_status()
                        content = await response.text()
                        return content
                except aiohttp.ClientError as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                    if attempt < retries - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        logger.error(f"Failed to fetch {url} after {retries} attempts")
                        return None

    async def extract_listing_urls(self, page_url):
        """Extract all car listing URLs from a listings page"""
        logger.info(f"Extracting listing URLs from: {page_url}")

        semaphore = asyncio.Semaphore(1)  # Only one request for the main page
        content = await self.get_page(page_url, semaphore)
        if not content:
            return []

        soup = BeautifulSoup(content, 'html.parser')

        # Find all product items with links
        listing_urls = []
        product_items = soup.find_all('div', class_='products-i')

        for item in product_items:
            link_element = item.find('a', class_='products-i-link')
            if link_element and link_element.get('href'):
                full_url = urljoin(self.base_url, link_element['href'])
                listing_urls.append(full_url)

        logger.info(f"Found {len(listing_urls)} listing URLs")
        return listing_urls

    async def extract_listing_details(self, listing_url, semaphore):
        """Extract detailed information from a single car listing"""
        logger.info(f"Extracting details from: {listing_url}")

        content = await self.get_page(listing_url, semaphore)
        if not content:
            return None

        soup = BeautifulSoup(content, 'html.parser')

        data = {
            'url': listing_url,
            'listing_id': '',
            'title': '',
            'price': '',
            'currency': 'AZN',
            'brand': '',
            'model': '',
            'year': '',
            'body_type': '',
            'color': '',
            'engine_volume': '',
            'engine_power': '',
            'fuel_type': '',
            'mileage': '',
            'transmission': '',
            'drivetrain': '',
            'seller_name': '',
            'seller_phone': '',
            'views': '',
            'updated_date': '',
            'location': '',
            'extras': '',
            'description': ''
        }

        try:
            # Extract title
            title_element = soup.find('h2', class_='product-name')
            if title_element:
                data['title'] = title_element.get_text(strip=True)

            # Extract price
            price_element = soup.find('div', class_='product-price')
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Extract numeric price
                price_match = re.search(r'(\d+(?:\s?\d+)*)', price_text.replace(',', ''))
                if price_match:
                    data['price'] = price_match.group(1).replace(' ', '')

            # Extract seller information
            seller_name_element = soup.find('div', class_='seller-name')
            if seller_name_element:
                name_p = seller_name_element.find('p')
                if name_p:
                    data['seller_name'] = name_p.get_text(strip=True)

            # Extract phone number
            phone_element = soup.find('a', class_='phone')
            if phone_element:
                data['seller_phone'] = phone_element.get_text(strip=True)

            # Extract listing ID, views, and updated date from statistics
            stats_div = soup.find('div', class_='product-statistics')
            if stats_div:
                stats_paragraphs = stats_div.find_all('p')
                for p in stats_paragraphs:
                    text = p.get_text()
                    if 'Baxışların sayı' in text:
                        views_match = re.search(r'(\d+)', text)
                        if views_match:
                            data['views'] = views_match.group(1)
                    elif 'Yeniləndi' in text:
                        date_match = re.search(r':\s*(.+)', text)
                        if date_match:
                            data['updated_date'] = date_match.group(1).strip()
                    elif 'Elanın nömrəsi' in text:
                        id_match = re.search(r'(\d+)', text)
                        if id_match:
                            data['listing_id'] = id_match.group(1)

            # Extract product properties
            properties_list = soup.find('ul', class_='product-properties')
            if properties_list:
                property_items = properties_list.find_all('li', class_='product-properties-i')

                for item in property_items:
                    label_element = item.find('label')
                    value_element = item.find('div', class_='product-properties-value')

                    if label_element and value_element:
                        label = label_element.get_text(strip=True)
                        value = value_element.get_text(strip=True)

                        # Map Azerbaijani labels to data fields
                        if 'Marka' in label:
                            data['brand'] = value
                        elif 'Model' in label:
                            data['model'] = value
                        elif 'Buraxılış ili' in label:
                            year_match = re.search(r'(\d{4})', value)
                            if year_match:
                                data['year'] = year_match.group(1)
                        elif 'Ban növü' in label:
                            data['body_type'] = value
                        elif 'Rəng' in label:
                            data['color'] = value
                        elif 'Mühərrikin həcmi' in label:
                            data['engine_volume'] = value
                        elif 'Mühərrikin gücü' in label:
                            data['engine_power'] = value
                        elif 'Yanacaq növü' in label:
                            data['fuel_type'] = value
                        elif 'Yürüş' in label:
                            data['mileage'] = value
                        elif 'Sürətlər qutusu' in label:
                            data['transmission'] = value
                        elif 'Ötürücü' in label:
                            data['drivetrain'] = value

            # Extract extras
            extras_div = soup.find('div', class_='product-extras')
            if extras_div:
                extras_items = extras_div.find_all('p', class_='product-extras-i')
                extras_list = [item.get_text(strip=True) for item in extras_items]
                data['extras'] = '; '.join(extras_list)

            # Extract description
            description_element = soup.find('p', class_='product-text')
            if description_element:
                data['description'] = description_element.get_text(strip=True).replace('\n', ' ').replace('\r', ' ')

            logger.info(f"Successfully extracted data for listing {data['listing_id']}")
            return data

        except Exception as e:
            logger.error(f"Error extracting data from {listing_url}: {e}")
            return None

    async def scrape_listings(self, base_url="https://www.biturbo.az/az/axtar", start_page=1, end_page=3, max_listings_per_page=None):
        """Scrape listings from multiple pages concurrently"""
        start_time = time.time()

        all_listing_urls = []

        # Generate page URLs and extract listings from each page
        for page_num in range(start_page, end_page + 1):
            if page_num == 1:
                page_url = f"{base_url}/"
            else:
                page_url = f"{base_url}/{page_num}/"

            logger.info(f"Extracting listings from page {page_num}: {page_url}")
            page_listings = await self.extract_listing_urls(page_url)

            if not page_listings:
                logger.warning(f"No listings found on page {page_num}")
                continue

            if max_listings_per_page:
                page_listings = page_listings[:max_listings_per_page]

            all_listing_urls.extend(page_listings)

            # Small delay between page requests
            await asyncio.sleep(1)

        logger.info(f"Found total of {len(all_listing_urls)} listings across {end_page - start_page + 1} pages")

        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self.max_concurrent)

        # Create tasks for all listings
        tasks = [
            self.extract_listing_details(url, semaphore)
            for url in all_listing_urls
        ]

        logger.info(f"Starting to scrape {len(tasks)} listings concurrently")

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out None results and exceptions
        all_data = []
        for result in results:
            if isinstance(result, dict) and result:
                all_data.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Task failed with exception: {result}")

        end_time = time.time()
        logger.info(f"Scraping completed in {end_time - start_time:.2f} seconds")
        logger.info(f"Successfully scraped {len(all_data)} out of {len(all_listing_urls)} listings")

        return all_data

    def save_to_csv(self, data, filename='biturbo_listings_async.csv'):
        """Save scraped data to CSV file"""
        if not data:
            logger.warning("No data to save")
            return

        logger.info(f"Saving {len(data)} listings to {filename}")

        # Define CSV columns
        fieldnames = [
            'seller_name', 'seller_phone', 'listing_id', 'url', 'title', 'brand', 'model', 'year', 'body_type',
            'color', 'engine_volume', 'engine_power', 'fuel_type', 'mileage',
            'transmission', 'drivetrain', 'price', 'currency', 'views', 'updated_date', 'location', 'extras', 'description'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                writer.writerow(row)

        logger.info(f"Data saved successfully to {filename}")

async def main():
    """Main function to run the async scraper"""

    # Configuration - easily changeable parameters
    START_PAGE = 1          # Start from page 1
    END_PAGE = 50          # End at page 50 (scrape pages 1-50, ~2000 listings)
    MAX_CONCURRENT = 10    # Number of concurrent requests
    MAX_LISTINGS_PER_PAGE = None  # None = all listings per page (40 per page)
    OUTPUT_FILENAME = 'biturbo_listings.csv'

    try:
        async with BiturboScraperAsync(max_concurrent=MAX_CONCURRENT) as scraper:
            # Scrape listings from multiple pages
            data = await scraper.scrape_listings(
                start_page=START_PAGE,
                end_page=END_PAGE,
                max_listings_per_page=MAX_LISTINGS_PER_PAGE
            )

            # Save to CSV
            scraper.save_to_csv(data, filename=OUTPUT_FILENAME)

            logger.info("Async scraping completed successfully!")

    except Exception as e:
        logger.error(f"Async scraping failed: {e}")

def configure_and_run():
    """Function to configure scraping parameters and run"""
    import sys

    if len(sys.argv) > 1:
        try:
            start_page = int(sys.argv[1])
            end_page = int(sys.argv[2]) if len(sys.argv) > 2 else start_page
            print(f"Scraping pages {start_page} to {end_page}")

            # Modify the main function parameters
            async def configured_main():
                async with BiturboScraperAsync(max_concurrent=10) as scraper:
                    data = await scraper.scrape_listings(
                        start_page=start_page,
                        end_page=end_page,
                        max_listings_per_page=None
                    )
                    scraper.save_to_csv(data, filename=f'biturbo_pages_{start_page}_to_{end_page}.csv')
                    logger.info("Configured scraping completed successfully!")

            asyncio.run(configured_main())
            return

        except ValueError:
            print("Usage: python3 biturbo_scraper_async.py [start_page] [end_page]")
            print("Example: python3 biturbo_scraper_async.py 1 5  # Scrapes pages 1-5")
            sys.exit(1)

    # Run default configuration
    asyncio.run(main())

if __name__ == "__main__":
    # Check if aiohttp is available
    try:
        import aiohttp
        configure_and_run()
    except ImportError:
        logger.error("aiohttp not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "aiohttp"])
        import aiohttp
        configure_and_run()