import ast
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

# Configuration
WORK_DIR = '/home/imagda/_invest2024/latex/macroeconomics/pics/market_helath_topBottom/pine_screener_performance/csv/'
CONFIG_FILE = '/home/imagda/_invest2024/latex/macroeconomics/pics/market_helath_topBottom/pine_screener_performance/run_top_losers_gainers_v2.txt'
# Output directory to png subdirectory
OUTPUT_DIR = os.path.join(WORK_DIR, '../png/')

def process_csv(input_csv_path, columns_to_keep, sort_column, rows_to_display):
    # If path is relative, join with WORK_DIR, else use as is
    if not os.path.isabs(input_csv_path):
        input_csv_path = os.path.join(WORK_DIR, input_csv_path)
        
    input_filename = os.path.basename(input_csv_path)
    print(f"Processing: {input_filename}...")
    
    try:
        # Load Data
        df = pd.read_csv(input_csv_path)
        
        # Select Columns
        available_columns = [col for col in columns_to_keep if col in df.columns]
        if len(available_columns) != len(columns_to_keep):
            missing = set(columns_to_keep) - set(available_columns)
            print(f"  Warning: Missing columns in {input_filename}: {missing}")
        
        df_filtered = df[available_columns].copy()
        
        # Handle NaN
        df_filtered = df_filtered.fillna(0)
        
        # Round numeric columns to 2 decimal places
        numeric_cols = df_filtered.select_dtypes(include=['float', 'float64']).columns
        df_filtered[numeric_cols] = df_filtered[numeric_cols].round(2)

        # Format RS columns as integers
        rs_cols = [col for col in df_filtered.columns if col.startswith('RS ')]
        for col in rs_cols:
            if pd.api.types.is_numeric_dtype(df_filtered[col]):
                df_filtered[col] = df_filtered[col].round(0).astype(int)
        
        # Rename Beschreibung to Description
        if 'Beschreibung' in df_filtered.columns:
            df_filtered = df_filtered.rename(columns={'Beschreibung': 'Description'})

        # Sort
        # Check if sort column exists, if not, try to rename it if it was 'Beschreibung'
        actual_sort_col = sort_column
        if sort_column == 'Beschreibung' and 'Description' in df_filtered.columns:
            actual_sort_col = 'Description'
            
        if actual_sort_col not in df_filtered.columns:
             print(f"  Error: Sort column '{actual_sort_col}' not found in data.")
             return

        df_sorted = df_filtered.sort_values(by=actual_sort_col, ascending=False)
        
        # Extract date and week from filename
        # Pattern: Name_YYYY-MM-DD.csv
        # We process the filename without extension first for cleaner regex matching if needed, 
        # or just match the pattern.
        base_name_no_ext = os.path.splitext(input_filename)[0]
        date_match = re.search(r'(.*)_(\d{4}-\d{2}-\d{2})$', base_name_no_ext)
        subtitle = ""
        if date_match:
            dataset_name = date_match.group(1)
            date_str = date_match.group(2)
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                week_num = dt.isocalendar()[1]
                subtitle = f"{dataset_name} | Date: {date_str} | Week: {week_num}"
            except ValueError:
                pass # Invalid date format despite regex match?

        # Define column widths
        # Define column widths dynamically
        # Symbol: 10%, Description: 30%
        # RS columns (0-99): Small width (4%)
        # Rest: Distribute remaining space
        
        final_widths = []
        flexible_cols_count = 0
        used_width = 0.0
        
        for col_name in df_sorted.columns:
            if col_name == 'Symbol':
                w = 0.10
                final_widths.append(w)
                used_width += w
            elif col_name == 'Description':
                w = 0.30
                final_widths.append(w)
                used_width += w
            elif col_name.startswith('RS '):
                w = 0.04
                final_widths.append(w)
                used_width += w
            else:
                final_widths.append(None) # Mark for flexible width
                flexible_cols_count += 1
        
        # Distribute remaining width
        remaining_width = 1.0 - used_width
        
        # Avoid division by zero or negative widths if user adds too many columns
        if flexible_cols_count > 0:
            flex_width = max(0.01, remaining_width / flexible_cols_count)
            col_widths = [w if w is not None else flex_width for w in final_widths]
        else:
            col_widths = final_widths
        
        # Calculate dynamic figure height based on rows
        # Base height for 15 rows was around 8.
        # Let's approximate: 2 (header/title) + 0.4 * rows?
        # 15 rows -> 2 + 6 = 8.
        # 20 rows -> 2 + 8 = 10.
        fig_height = 2 + (rows_to_display * 0.45) 

        # Update create_table_image to accept widths
        def create_table_with_widths(df, title, filename):
            import textwrap
            
            fig, ax = plt.subplots(figsize=(12, fig_height))
            ax.axis('off')
            ax.axis('tight')
            
            # Prepare alternating row colors
            colors = []
            for i in range(len(df)):
                if i % 2 != 0:
                    colors.append(['#E0E0E0'] * len(df.columns))
                else:
                    colors.append(['w'] * len(df.columns))
            
            # Wrap headers
            # Wrap text to approx 10 chars to encourage 2 lines
            wrapped_columns = ["\n".join(textwrap.wrap(c, width=12, break_long_words=False)) for c in df.columns]

            table = ax.table(
                cellText=df.values, 
                colLabels=wrapped_columns, 
                loc='center', 
                cellLoc='center', 
                colWidths=col_widths,
                cellColours=colors
            )
            
            # Adjust header height (row 0)
            cells = table.get_celld()
            for (row, col), cell in cells.items():
                if row == 0:
                    # Increase header height
                    current_height = cell.get_height()
                    cell.set_height(current_height * 2.5) 
            
            table.auto_set_font_size(False)
            table.set_fontsize(8) # Reduced font size
            table.scale(1.2, 1.2)
            
            plt.title(title, fontsize=16, pad=20)
            if subtitle:
                plt.text(0.5, 0.96, subtitle, ha='center', va='center', transform=fig.transFigure, fontsize=12)
            
            # Ensure output directory exists (create it just in case, though main should do it)
            if not os.path.exists(OUTPUT_DIR):
                 try:
                     os.makedirs(OUTPUT_DIR)
                 except OSError as e:
                     print(f"Error creating directory {OUTPUT_DIR}: {e}")
                     return

            out_path = os.path.join(OUTPUT_DIR, filename)
            plt.savefig(out_path, bbox_inches='tight', dpi=300)
            plt.close()
            print(f"  Created {filename}")

        # Derive base name
        base_name = os.path.splitext(input_filename)[0]

        # Top N (Gainers)
        top_n = df_sorted.head(rows_to_display)
        create_table_with_widths(top_n, f'Top {rows_to_display} Assets by {sort_column}', f'{base_name}_top.png')
        
        # Bottom N (Losers)
        bottom_n = df_sorted.tail(rows_to_display).sort_values(by=actual_sort_col, ascending=True)
        create_table_with_widths(bottom_n, f'Bottom {rows_to_display} Assets by {sort_column}', f'{base_name}_bottom.png')
        
    except FileNotFoundError:
        print(f"  Error: Could not find file {input_csv_path}")
    except pd.errors.EmptyDataError:
        print(f"  Error: File {input_filename} is empty")
    except KeyError as e:
        print(f"  Error: Missing column in CSV - {e}")
    except Exception as e:
        print(f"  An error occurred processing {input_filename}: {e}")

def parse_config(config_path):
    files = []
    columns_to_keep = []
    sort_column = ''
    rows_to_display = 20 # Default
    
    with open(config_path, 'r') as f:
        lines = f.readlines()
        
    section = None
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith('###'):
            if 'files to run' in line:
                section = 'files'
            else:
                section = None # End of section?
            continue
            
        if section == 'files':
            files.append(line)
        
        if line.startswith('COLUMNS_TO_KEEP'):
            try:
                # Extract the list part: COLUMNS_TO_KEEP = [...]
                parts = line.split('=', 1)
                if len(parts) == 2:
                    columns_to_keep = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing columns: {e}")
                
        if line.startswith('SORT_COLUMN'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                     # ast.literal_eval handles strings cleanly (removes quotes)
                    sort_column = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing sort column: {e}")
        
        if line.startswith('ROWS_TO_DISPLAY'):
             try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    rows_to_display = int(parts[1].strip())
             except Exception as e:
                 print(f"Error parsing rows to display: {e}")
                 
    return files, columns_to_keep, sort_column, rows_to_display

def main():
    config_path = os.path.join(WORK_DIR, CONFIG_FILE)
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    print(f"Reading config from: {config_path}")
    files, columns_to_keep, sort_column, rows_to_display = parse_config(config_path)
    
    # Ensure Output Directory Exists
    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating output directory: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    else:
        print(f"Output directory: {OUTPUT_DIR}")

    print(f"Config:")
    print(f"  Files: {len(files)}")
    print(f"  Columns: {columns_to_keep}")
    print(f"  Sort By: {sort_column}")
    print(f"  Rows to Display: {rows_to_display}")

    if not files:
        print("No files found in config.")
        return
        
    if not columns_to_keep:
        # Fallback defaults?
        print("Error: No columns defined.")
        return
        
    if not sort_column:
        print("Error: No sort column defined.")
        return

    for filename in files:
        process_csv(filename, columns_to_keep, sort_column, rows_to_display)

if __name__ == "__main__":
    main()
