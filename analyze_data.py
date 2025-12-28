import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('biturbo_listings.csv')

print("="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"Total listings: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")

print("\n" + "="*80)
print("PRICE ANALYSIS")
print("="*80)
# Convert price to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')
print(f"Price statistics (AZN):")
print(df[df['currency'] == 'AZN']['price'].describe())

print("\n" + "="*80)
print("BRAND ANALYSIS")
print("="*80)
print(f"Top 15 brands by listing count:")
print(df['brand'].value_counts().head(15))

print("\n" + "="*80)
print("MODEL ANALYSIS (TOP BRANDS)")
print("="*80)
top_brands = df['brand'].value_counts().head(5).index
for brand in top_brands:
    print(f"\n{brand} - Top 5 models:")
    print(df[df['brand'] == brand]['model'].value_counts().head(5))

print("\n" + "="*80)
print("YEAR ANALYSIS")
print("="*80)
df['year'] = pd.to_numeric(df['year'], errors='coerce')
print(f"Year range: {df['year'].min()} - {df['year'].max()}")
print(f"\nTop 10 years by listing count:")
print(df['year'].value_counts().head(10))

print("\n" + "="*80)
print("TRANSMISSION ANALYSIS")
print("="*80)
print(df['transmission'].value_counts())

print("\n" + "="*80)
print("FUEL TYPE ANALYSIS")
print("="*80)
print(df['fuel_type'].value_counts())

print("\n" + "="*80)
print("BODY TYPE ANALYSIS")
print("="*80)
print(df['body_type'].value_counts())

print("\n" + "="*80)
print("VIEWS ANALYSIS")
print("="*80)
df['views'] = pd.to_numeric(df['views'], errors='coerce')
print(f"Views statistics:")
print(df['views'].describe())
print(f"\nTop 10 most viewed listings:")
print(df.nlargest(10, 'views')[['brand', 'model', 'year', 'price', 'views']])

print("\n" + "="*80)
print("PRICE BY BRAND (TOP 10 BRANDS)")
print("="*80)
top_10_brands = df['brand'].value_counts().head(10).index
for brand in top_10_brands:
    brand_data = df[df['brand'] == brand]['price']
    print(f"{brand}: Mean={brand_data.mean():.0f} AZN, Median={brand_data.median():.0f} AZN")

print("\n" + "="*80)
print("MILEAGE ANALYSIS")
print("="*80)
# Extract numeric mileage
df['mileage_numeric'] = df['mileage'].str.extract('(\d+)').astype(float)
print(f"Mileage statistics (km):")
print(df['mileage_numeric'].describe())

print("\n" + "="*80)
print("PRICE vs VIEWS CORRELATION")
print("="*80)
correlation = df[['price', 'views']].corr()
print(correlation)

print("\n" + "="*80)
print("COLOR PREFERENCES")
print("="*80)
print(df['color'].value_counts().head(10))

print("\n" + "="*80)
print("DRIVETRAIN ANALYSIS")
print("="*80)
print(df['drivetrain'].value_counts())
