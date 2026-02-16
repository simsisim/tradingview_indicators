#!/usr/bin/env python3
"""60% for Tech, 35% for Others"""
import csv, math

def calc(count, pct):
    if count == 0: return 0
    return min(39, max(min(5, count), math.ceil(count * pct)))

csv_file = "/home/imagda/_invest2024/tradingview/myIndicators/stock_vs_industry_industry_vs_SPY/all_industries_top39_stock_counts.csv"
rows = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    for row in reader:
        is_tech = row['Category'] in ['Technology - Software/Services', 'Technology - Hardware/Electronics']
        row['Include top'] = calc(int(row['Stock_Count']), 0.60 if is_tech else 0.35)
        rows.append(row)

with open(csv_file, 'w', newline='') as f:
    csv.DictWriter(f, fields).writeheader()
    csv.DictWriter(f, fields).writerows(rows)

total = sum(int(r['Include top']) for r in rows)
print(f"✅ 60% Tech / 35% Others → Total: {total} stocks")
