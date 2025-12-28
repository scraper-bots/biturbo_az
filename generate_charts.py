import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Load data
print("Loading data...")
df = pd.read_csv('biturbo_listings.csv')

# Data preprocessing
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['views'] = pd.to_numeric(df['views'], errors='coerce')
df['mileage_numeric'] = df['mileage'].str.extract('(\d+)').astype(float)
df['vehicle_age'] = 2024 - df['year']

# Create charts directory if it doesn't exist
import os
os.makedirs('charts', exist_ok=True)

print("Generating charts...")

# Chart 1: Market Share by Top 15 Brands
print("1. Market share by brand...")
plt.figure(figsize=(12, 8))
brand_counts = df['brand'].value_counts().head(15)
colors = sns.color_palette("Blues_r", n_colors=15)
plt.barh(range(len(brand_counts)), brand_counts.values, color=colors)
plt.yticks(range(len(brand_counts)), brand_counts.index)
plt.xlabel('Number of Listings', fontsize=12, fontweight='bold')
plt.ylabel('Brand', fontsize=12, fontweight='bold')
plt.title('Market Share: Top 15 Automotive Brands\n1,460 Active Listings',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
# Add value labels
for i, v in enumerate(brand_counts.values):
    plt.text(v + 5, i, str(v), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/01_market_share_by_brand.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 2: Average Price by Top 10 Brands
print("2. Average price by brand...")
plt.figure(figsize=(12, 8))
top_brands = df['brand'].value_counts().head(10).index
brand_prices = df[df['brand'].isin(top_brands)].groupby('brand')['price'].mean().sort_values(ascending=True)
colors = sns.color_palette("Greens_r", n_colors=10)
plt.barh(range(len(brand_prices)), brand_prices.values, color=colors)
plt.yticks(range(len(brand_prices)), brand_prices.index)
plt.xlabel('Average Price (AZN)', fontsize=12, fontweight='bold')
plt.ylabel('Brand', fontsize=12, fontweight='bold')
plt.title('Price Positioning: Average Listing Price by Top 10 Brands',
          fontsize=14, fontweight='bold', pad=20)
# Add value labels
for i, v in enumerate(brand_prices.values):
    plt.text(v + 500, i, f'{v:,.0f} AZN', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/02_average_price_by_brand.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3: Listing Volume by Year (2000-2024)
print("3. Listing trends by year...")
plt.figure(figsize=(14, 6))
year_counts = df[(df['year'] >= 2000) & (df['year'] <= 2024)]['year'].value_counts().sort_index()
plt.plot(year_counts.index, year_counts.values, marker='o', linewidth=2.5,
         markersize=8, color='#2E86AB')
plt.fill_between(year_counts.index, year_counts.values, alpha=0.3, color='#2E86AB')
plt.xlabel('Model Year', fontsize=12, fontweight='bold')
plt.ylabel('Number of Listings', fontsize=12, fontweight='bold')
plt.title('Market Trends: Listing Volume by Vehicle Model Year (2000-2024)',
          fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.xticks(range(2000, 2025, 2), rotation=45)
plt.tight_layout()
plt.savefig('charts/03_listing_volume_by_year.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 4: Transmission Type Distribution
print("4. Transmission type preferences...")
plt.figure(figsize=(10, 6))
transmission_counts = df['transmission'].value_counts()
# Map to English for clarity
transmission_map = {'Avtomat': 'Automatic', 'Mexaniki': 'Manual', 'Variator': 'CVT'}
transmission_counts.index = transmission_counts.index.map(transmission_map)
colors = ['#A23B72', '#F18F01', '#C73E1D']
plt.barh(range(len(transmission_counts)), transmission_counts.values, color=colors)
plt.yticks(range(len(transmission_counts)), transmission_counts.index)
plt.xlabel('Number of Listings', fontsize=12, fontweight='bold')
plt.ylabel('Transmission Type', fontsize=12, fontweight='bold')
plt.title('Transmission Preferences: Market Distribution',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
# Add percentage labels
total = transmission_counts.sum()
for i, v in enumerate(transmission_counts.values):
    pct = (v/total)*100
    plt.text(v + 15, i, f'{v} ({pct:.1f}%)', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/04_transmission_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 5: Average Price by Vehicle Age
print("5. Price depreciation analysis...")
plt.figure(figsize=(14, 6))
age_price = df[df['vehicle_age'] <= 30].groupby('vehicle_age')['price'].agg(['mean', 'median']).reset_index()
plt.plot(age_price['vehicle_age'], age_price['mean'], marker='o', linewidth=2.5,
         markersize=6, label='Average Price', color='#06A77D')
plt.plot(age_price['vehicle_age'], age_price['median'], marker='s', linewidth=2.5,
         markersize=6, label='Median Price', color='#D62828', linestyle='--')
plt.xlabel('Vehicle Age (Years)', fontsize=12, fontweight='bold')
plt.ylabel('Price (AZN)', fontsize=12, fontweight='bold')
plt.title('Value Retention: Pricing Trends by Vehicle Age',
          fontsize=14, fontweight='bold', pad=20)
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/05_price_by_vehicle_age.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 6: Color Preferences (Top 10)
print("6. Color preferences...")
plt.figure(figsize=(12, 8))
color_counts = df['color'].value_counts().head(10)
colors_palette = sns.color_palette("Spectral", n_colors=10)
plt.barh(range(len(color_counts)), color_counts.values, color=colors_palette)
plt.yticks(range(len(color_counts)), color_counts.index)
plt.xlabel('Number of Listings', fontsize=12, fontweight='bold')
plt.ylabel('Vehicle Color', fontsize=12, fontweight='bold')
plt.title('Consumer Preferences: Top 10 Vehicle Colors',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
# Add value labels
for i, v in enumerate(color_counts.values):
    plt.text(v + 8, i, str(v), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/06_color_preferences.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 7: Drivetrain Distribution
print("7. Drivetrain distribution...")
plt.figure(figsize=(10, 6))
drivetrain_counts = df['drivetrain'].value_counts()
# Map to English
drivetrain_map = {'Ön': 'Front-Wheel Drive', 'Arxa': 'Rear-Wheel Drive', 'Tam': 'All-Wheel Drive'}
drivetrain_counts.index = drivetrain_counts.index.map(drivetrain_map)
colors = ['#5F0F40', '#9A031E', '#FB8B24']
plt.barh(range(len(drivetrain_counts)), drivetrain_counts.values, color=colors)
plt.yticks(range(len(drivetrain_counts)), drivetrain_counts.index)
plt.xlabel('Number of Listings', fontsize=12, fontweight='bold')
plt.ylabel('Drivetrain Type', fontsize=12, fontweight='bold')
plt.title('Drivetrain Configuration: Market Distribution',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
# Add percentage labels
total = drivetrain_counts.sum()
for i, v in enumerate(drivetrain_counts.values):
    pct = (v/total)*100
    plt.text(v + 15, i, f'{v} ({pct:.1f}%)', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/07_drivetrain_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 8: Price Range Distribution
print("8. Price range analysis...")
plt.figure(figsize=(14, 6))
price_bins = [0, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 100000, 350000]
price_labels = ['0-5K', '5-10K', '10-15K', '15-20K', '20-25K', '25-30K', '30-40K', '40-50K', '50-100K', '100K+']
df['price_range'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)
price_range_counts = df['price_range'].value_counts().sort_index()
colors = sns.color_palette("RdYlGn_r", n_colors=len(price_range_counts))
plt.bar(range(len(price_range_counts)), price_range_counts.values, color=colors, edgecolor='black', linewidth=1.2)
plt.xticks(range(len(price_range_counts)), price_range_counts.index, rotation=45, ha='right')
plt.xlabel('Price Range (AZN)', fontsize=12, fontweight='bold')
plt.ylabel('Number of Listings', fontsize=12, fontweight='bold')
plt.title('Price Segmentation: Inventory Distribution Across Price Ranges',
          fontsize=14, fontweight='bold', pad=20)
# Add value labels
for i, v in enumerate(price_range_counts.values):
    plt.text(i, v + 5, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/08_price_range_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 9: Top 20 Models by Listing Count
print("9. Most popular models...")
plt.figure(figsize=(12, 10))
# Combine brand and model
df['brand_model'] = df['brand'] + ' ' + df['model']
model_counts = df['brand_model'].value_counts().head(20)
colors = sns.color_palette("viridis", n_colors=20)
plt.barh(range(len(model_counts)), model_counts.values, color=colors)
plt.yticks(range(len(model_counts)), model_counts.index, fontsize=9)
plt.xlabel('Number of Listings', fontsize=12, fontweight='bold')
plt.ylabel('Brand & Model', fontsize=12, fontweight='bold')
plt.title('Market Leaders: Top 20 Most Listed Vehicle Models',
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
# Add value labels
for i, v in enumerate(model_counts.values):
    plt.text(v + 1, i, str(v), va='center', fontweight='bold', fontsize=8)
plt.tight_layout()
plt.savefig('charts/09_top_models_by_count.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 10: Average Views by Price Range
print("10. Engagement analysis...")
plt.figure(figsize=(14, 6))
views_by_price = df.groupby('price_range')['views'].mean().sort_index()
colors = sns.color_palette("coolwarm", n_colors=len(views_by_price))
plt.bar(range(len(views_by_price)), views_by_price.values, color=colors, edgecolor='black', linewidth=1.2)
plt.xticks(range(len(views_by_price)), views_by_price.index, rotation=45, ha='right')
plt.xlabel('Price Range (AZN)', fontsize=12, fontweight='bold')
plt.ylabel('Average Views', fontsize=12, fontweight='bold')
plt.title('Customer Engagement: Average Listing Views by Price Segment',
          fontsize=14, fontweight='bold', pad=20)
plt.axhline(y=df['views'].mean(), color='red', linestyle='--', linewidth=2, label=f'Overall Average: {df["views"].mean():.0f}')
plt.legend(fontsize=11)
# Add value labels
for i, v in enumerate(views_by_price.values):
    plt.text(i, v + 10, f'{v:.0f}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/10_engagement_by_price_range.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 11: Price Comparison - Top 5 Brands by Segment
print("11. Brand price positioning...")
plt.figure(figsize=(14, 7))
top_5_brands = df['brand'].value_counts().head(5).index
brand_price_data = []
for brand in top_5_brands:
    brand_df = df[df['brand'] == brand]['price']
    brand_price_data.append(brand_df)

positions = np.arange(len(top_5_brands))
bp = plt.boxplot(brand_price_data, positions=positions, labels=top_5_brands,
                 patch_artist=True, showmeans=True, widths=0.6)

# Color the boxes
colors = ['#E63946', '#F1FAEE', '#A8DADC', '#457B9D', '#1D3557']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

plt.xlabel('Brand', fontsize=12, fontweight='bold')
plt.ylabel('Price (AZN)', fontsize=12, fontweight='bold')
plt.title('Price Variability: Distribution Comparison Across Top 5 Brands',
          fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('charts/11_price_comparison_top_brands.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 12: Mileage Distribution
print("12. Mileage analysis...")
plt.figure(figsize=(14, 6))
mileage_bins = [0, 50, 100, 150, 200, 250, 300, 400, 500, 1000]
mileage_labels = ['0-50K', '50-100K', '100-150K', '150-200K', '200-250K', '250-300K', '300-400K', '400-500K', '500K+']
df['mileage_range'] = pd.cut(df['mileage_numeric'], bins=mileage_bins, labels=mileage_labels)
mileage_counts = df['mileage_range'].value_counts().sort_index()
colors = sns.color_palette("YlOrRd", n_colors=len(mileage_counts))
plt.bar(range(len(mileage_counts)), mileage_counts.values, color=colors, edgecolor='black', linewidth=1.2)
plt.xticks(range(len(mileage_counts)), mileage_counts.index, rotation=45, ha='right')
plt.xlabel('Mileage Range (Kilometers)', fontsize=12, fontweight='bold')
plt.ylabel('Number of Listings', fontsize=12, fontweight='bold')
plt.title('Vehicle Usage: Inventory Distribution by Mileage',
          fontsize=14, fontweight='bold', pad=20)
# Add value labels
for i, v in enumerate(mileage_counts.values):
    plt.text(i, v + 5, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/12_mileage_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 13: Year-over-Year Listing Activity (2015-2024 vehicles)
print("13. Recent model year trends...")
plt.figure(figsize=(14, 6))
recent_years = df[(df['year'] >= 2015) & (df['year'] <= 2024)]
year_avg_price = recent_years.groupby('year').agg({'year': 'count', 'price': 'mean'}).rename(columns={'year': 'count'})
year_avg_price = year_avg_price.reset_index()

fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.set_xlabel('Model Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Listings', fontsize=12, fontweight='bold', color='#1F77B4')
bar1 = ax1.bar(year_avg_price['year'], year_avg_price['count'], color='#1F77B4', alpha=0.7, label='Listing Count')
ax1.tick_params(axis='y', labelcolor='#1F77B4')
ax1.set_xticks(year_avg_price['year'])

ax2 = ax1.twinx()
ax2.set_ylabel('Average Price (AZN)', fontsize=12, fontweight='bold', color='#FF7F0E')
line1 = ax2.plot(year_avg_price['year'], year_avg_price['price'], color='#FF7F0E',
                 marker='o', linewidth=3, markersize=8, label='Average Price')
ax2.tick_params(axis='y', labelcolor='#FF7F0E')

plt.title('Recent Market Activity: Listing Volume & Pricing for 2015-2024 Models',
          fontsize=14, fontweight='bold', pad=20)
fig.tight_layout()
plt.savefig('charts/13_recent_year_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 14: Market Concentration - Brand Market Share Percentage
print("14. Market concentration analysis...")
plt.figure(figsize=(14, 6))
top_10_brands = df['brand'].value_counts().head(10)
other_count = len(df) - top_10_brands.sum()
all_brands = pd.concat([top_10_brands, pd.Series({'Others': other_count})])
percentages = (all_brands / len(df) * 100).sort_values(ascending=True)

colors = sns.color_palette("tab20", n_colors=len(percentages))
plt.barh(range(len(percentages)), percentages.values, color=colors)
plt.yticks(range(len(percentages)), percentages.index)
plt.xlabel('Market Share (%)', fontsize=12, fontweight='bold')
plt.ylabel('Brand', fontsize=12, fontweight='bold')
plt.title('Market Concentration: Brand Share Distribution (Top 10 + Others)',
          fontsize=14, fontweight='bold', pad=20)
# Add percentage labels
for i, v in enumerate(percentages.values):
    plt.text(v + 0.2, i, f'{v:.1f}%', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/14_market_concentration.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 15: Average Mileage by Vehicle Age
print("15. Mileage accumulation trends...")
plt.figure(figsize=(14, 6))
age_mileage = df[(df['vehicle_age'] > 0) & (df['vehicle_age'] <= 25)].groupby('vehicle_age')['mileage_numeric'].mean().reset_index()
plt.plot(age_mileage['vehicle_age'], age_mileage['mileage_numeric'],
         marker='o', linewidth=2.5, markersize=7, color='#6A4C93')
plt.fill_between(age_mileage['vehicle_age'], age_mileage['mileage_numeric'], alpha=0.3, color='#6A4C93')
plt.xlabel('Vehicle Age (Years)', fontsize=12, fontweight='bold')
plt.ylabel('Average Mileage (Thousands km)', fontsize=12, fontweight='bold')
plt.title('Usage Patterns: Average Mileage Accumulation by Vehicle Age',
          fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/15_mileage_by_age.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*80)
print("SUCCESS! All 15 charts generated in the 'charts/' directory")
print("="*80)
print("\nGenerated charts:")
print("  1. Market share by brand")
print("  2. Average price by brand")
print("  3. Listing volume by year")
print("  4. Transmission distribution")
print("  5. Price by vehicle age")
print("  6. Color preferences")
print("  7. Drivetrain distribution")
print("  8. Price range distribution")
print("  9. Top models by count")
print(" 10. Engagement by price range")
print(" 11. Price comparison - top brands")
print(" 12. Mileage distribution")
print(" 13. Recent year trends")
print(" 14. Market concentration")
print(" 15. Mileage by age")
print("="*80)
