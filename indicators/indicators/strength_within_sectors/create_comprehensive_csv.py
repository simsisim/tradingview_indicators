#!/usr/bin/env python3
"""
Create CSV with ALL industries as columns and top 39 stocks as rows.
Industries are sorted alphabetically, stocks are already sorted by market cap in HTML.
"""

import os
from bs4 import BeautifulSoup
import csv

HTML_DIR = "/home/imagda/_invest2024/tradingview/myIndicators/stock_vs_industry_industry_vs_SPY/docus/industries_stocks_market_cap"
OUTPUT_CSV = "/home/imagda/_invest2024/tradingview/myIndicators/stock_vs_industry_industry_vs_SPY/all_industries_top39_by_marketcap.csv"

def clean_industry_name(filename):
    """Extract clean industry name from filename"""
    name = filename.replace("_ Industry Performance — USA — TradingView.html", "")
    name = name.replace("_", "/")
    return name.strip()

def extract_top_stocks(html_file, max_stocks=39):
    """Extract top N stock symbols from HTML (already sorted by market cap)"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    tables = soup.find_all('table')
    stocks = []
    
    for table in tables:
        headers = table.find_all('th')
        header_texts = [th.get_text(strip=True) for th in headers]
        
        # Find market cap column
        market_cap_col = -1
        for idx, header in enumerate(header_texts):
            if 'Market cap' in header or 'Market Cap' in header:
                market_cap_col = idx
                break
        
        if market_cap_col == -1:
            continue
        
        # Extract rows (already sorted by market cap descending in HTML)
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > market_cap_col:
                symbol_cell = cells[0]
                symbol_link = symbol_cell.find('a')
                
                if symbol_link:
                    symbol = symbol_link.get_text(strip=True)
                    if symbol:
                        stocks.append(symbol)
                        if len(stocks) >= max_stocks:
                            return stocks[:max_stocks]
        
        if stocks:
            break
    
    return stocks[:max_stocks]

def main():
    print("=" * 70)
    print("Creating Comprehensive Industry CSV (Top 39 Stocks by Market Cap)")
    print("=" * 70)
    
    # Find all HTML files
    html_files = []
    for filename in sorted(os.listdir(HTML_DIR)):
        if filename.endswith('.html'):
            html_files.append(filename)
    
    print(f"\nFound {len(html_files)} HTML files")
    
    # Extract data from each file
    all_industries = {}
    
    for filename in html_files:
        industry_name = clean_industry_name(filename)
        html_path = os.path.join(HTML_DIR, filename)
        stocks = extract_top_stocks(html_path, max_stocks=39)
        
        if stocks:
            all_industries[industry_name] = stocks
            print(f"  ✓ {industry_name}: {len(stocks)} stocks")
    
    # Create CSV with industries as columns
    print(f"\nCreating CSV with {len(all_industries)} industries...")
    
    # Sort industries alphabetically
    sorted_industries = sorted(all_industries.keys())
    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header row - industry names
        writer.writerow(sorted_industries)
        
        # Data rows - up to 39 rows (one per stock position)
        for i in range(39):
            row = []
            for industry in sorted_industries:
                stocks = all_industries[industry]
                if i < len(stocks):
                    row.append(stocks[i])
                else:
                    row.append('')  # Empty cell if industry has fewer stocks
            writer.writerow(row)
    
    print(f"\n✓ Created: {OUTPUT_CSV}")
    print(f"✓ Industries: {len(sorted_industries)}")
    print(f"✓ Max stocks per industry: 39")
    print("=" * 70)

if __name__ == "__main__":
    main()
