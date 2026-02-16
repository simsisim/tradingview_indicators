#!/usr/bin/env python3
"""
Calculate V27 character count using UPDATED all_industries_top39_stock_counts.csv (60% allocations).
"""

import csv

# Files
allocation_csv = "/home/imagda/_invest2024/tradingview/myIndicators/stock_vs_industry_industry_vs_SPY/all_industries_top39_stock_counts.csv"
top39_csv = "/home/imagda/_invest2024/tradingview/myIndicators/stock_vs_industry_industry_vs_SPY/all_industries_top39_by_marketcap.csv"

# Read allocations - USE THE INCLUDE TOP COLUMN!
industry_allocations = {}
with open(allocation_csv, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        industry = row['Industry']
        # Use the "Include top" column (60% rule applied)
        include_top = int(row['Include top'])
        industry_allocations[industry] = include_top

print(f"✅ Loaded {len(industry_allocations)} industries with 60% allocations\n")

# Read top39 CSV to get actual stock symbols
with open(top39_csv, 'r') as f:
    reader = csv.reader(f)
    industry_names = next(reader)
    all_rows = list(reader)

# Build stock lists per industry
industry_stocks = {}
for idx, industry_name in enumerate(industry_names):
    industry_name = industry_name.strip()
    if not industry_name:
        continue
    
    stocks = []
    for row in all_rows:
        if idx < len(row):
            stock = row[idx].strip()
            if stock:
                stocks.append(stock)
    
    industry_stocks[industry_name] = stocks

# Calculate new indArr character count
def estimate_industry_line_chars(industry_name, stocks):
    """Estimate characters needed for industry.new() line"""
    base = f"industry.new('{industry_name}',array.from("
    stocks_str = ','.join([f"'{s}'" for s in stocks])
    close = ")),\n"
    return len(base + stocks_str + close)

# Calculate total
new_indArr_chars = len("var indArr=array.from(\n")
total_stocks = 0
industry_count = 0

for industry, stocks in sorted(industry_stocks.items()):
    include_top = industry_allocations.get(industry, 5)
    selected_stocks = stocks[:include_top]
    total_stocks += len(selected_stocks)
    industry_count += 1
    
    chars = estimate_industry_line_chars(industry, selected_stocks)
    new_indArr_chars += chars

new_indArr_chars += len("     )\n")

# Constants
v26_total = 79615
current_indArr = 16019

# Calculate
v27_estimated = v26_total - current_indArr + new_indArr_chars

print(f"📊 V27 CHARACTER COUNT (60% Rule Applied):\n")
print(f"V26 Stats:")
print(f"  Total: {v26_total:,} characters")
print(f"  Current indArr: {current_indArr:,} characters\n")

print(f"New indArr (60% rule):")
print(f"  Industries: {industry_count}")
print(f"  Total stocks: {total_stocks:,} (was 2,962)")
print(f"  Stock reduction: {2962 - total_stocks:,} ({(2962-total_stocks)/2962*100:.1f}%)")
print(f"  New indArr size: {new_indArr_chars:,} characters")
print(f"  Change from v26: {new_indArr_chars - current_indArr:+,} characters\n")

print(f"V27 Projection:")
print(f"  {v26_total:,} - {current_indArr:,} + {new_indArr_chars:,} = {v27_estimated:,} characters\n")

print(f"TradingView Limit:")
print(f"  Limit: 80,000 characters")
if v27_estimated <= 80000:
    diff = 80000 - v27_estimated
    pct = diff / 800
    print(f"  ✅ UNDER by {diff:,} chars ({pct:.1f}%)")
    print(f"\n🎉 SUCCESS! V27 fits within the limit!")
else:
    diff = v27_estimated - 80000
    pct = diff / 800
    print(f"  ⚠️ OVER by {diff:,} chars ({pct:.1f}%)")
    print(f"\n❌ Still need to reduce by {diff:,} characters")

# Show tech industries
print(f"\n🎯 TECH & ELECTRONICS (60% Rule):")
tech_keywords = ['semiconductor', 'software', 'internet', 'electronic', 'computer', 'data processing', 'information technology', 'telecommunications equipment']
for industry in sorted(industry_allocations.keys()):
    if any(kw in industry.lower() for kw in tech_keywords):
        allocated = industry_allocations.get(industry, 5)
        available = len(industry_stocks.get(industry, []))
        print(f"  {industry:50} {allocated:2}/{available:2}")
