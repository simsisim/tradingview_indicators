import re
import os

input_file = '/home/imagda/_invest2024/latex/macroeconomics/pics/market_health/sustainability_ratios/io_assets.txt'
output_file = '/home/imagda/_invest2024/latex/macroeconomics/pics/market_health/sustainability_ratios/tradingview_watchlist_io.txt'

sections = {
    'io_assets_classes': [],
    'io_GOVT': [],
    'io_main_indices': [],
    'io_SPY': [],
    'io_DJP': []
}

# Mapping headers to keys
header_patterns = {
    'ASSET CLASSES': 'io_assets_classes',
    'GOVERNMENT BONDS': 'io_GOVT',
    'MAIN INDEXES': 'io_main_indices',
    'SPY SECTORS': 'io_SPY',
    'COMMODITIES': 'io_DJP'
}

all_tickers = []
current_section = None

regex = r'^([A-Z0-9]+(?:[:][A-Z0-9]+)?)(?:[:;]|\s|$)'

# Check if input file exists
if not os.path.exists(input_file):
    print(f"Error: File {input_file} not found.")
    exit(1)

with open(input_file, 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Check for header
    if line.startswith('#'):
        clean_line = line.replace('#', '').replace('=', '').strip().upper()
        if not clean_line:
            continue
            
        # Try to find matching section
        for pattern, section_key in header_patterns.items():
            if pattern in clean_line:
                current_section = section_key
                break
        continue

    # Extract ticker
    match = re.match(regex, line)
    if match:
        ticker = match.group(1)
        
        # Add to all_tickers if not present (preserve order)
        if ticker not in all_tickers:
            all_tickers.append(ticker)
        
        # Add to current section
        if current_section:
            sections[current_section].append(ticker)

# Write output
with open(output_file, 'w') as f:
    # 1. io_assets (All)
    f.write('### io_assets\n')
    for t in all_tickers:
        f.write(f"{t}\n")
    
    # Other sections as requested
    ordered_keys = ['io_assets_classes', 'io_GOVT', 'io_SPY', 'io_main_indices', 'io_SPY', 'io_DJP']
    
    for key in ordered_keys:
        f.write(f"\n### {key}\n")
        if key in sections:
            for t in sections[key]:
                f.write(f"{t}\n")

print(f"Generated watchlist at {output_file}")
