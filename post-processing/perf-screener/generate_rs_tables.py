import ast
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

# Configuration
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(SCRIPT_DIR, 'csv')
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'run_top_losers_gainers_v2.txt')
# Output directory to png subdirectory
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'png')

def process_csv(input_csv_path, columns_to_keep, sort_column, rows_to_display,
                chart_metric=None, generate_charts=True, generate_tables=True):
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

        # Helper function to draw table on an axis
        def draw_table_on_axis(ax, df, title):
            import textwrap

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
            wrapped_columns = ["\n".join(textwrap.wrap(c, width=12, break_long_words=False)) for c in df.columns]

            table = ax.table(
                cellText=df.values,
                colLabels=wrapped_columns,
                loc='center',
                cellLoc='center',
                colWidths=col_widths,
                cellColours=colors,
                bbox=[0, 0.15, 1, 0.85]  # [left, bottom, width, height] - shift table up
            )

            # Adjust header height (row 0)
            cells = table.get_celld()
            for (row, col), cell in cells.items():
                if row == 0:
                    current_height = cell.get_height()
                    cell.set_height(current_height * 2.5)

            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1.2, 1.2)

            ax.set_title(title, fontsize=14, pad=-3, fontweight='bold')

        # Helper function to draw chart on an axis
        def draw_chart_on_axis(ax, df, chart_metric):
            """Draw vertical bar chart on the provided axis"""

            # Validate metric exists
            if chart_metric not in df.columns:
                print(f"  Warning: Chart metric '{chart_metric}' not found in columns. Skipping chart.")
                return False

            # Prepare data
            symbols = df['Symbol'].tolist()
            values = df[chart_metric].tolist()

            # Determine colors based on values
            colors = []
            for val in values:
                if val > 0.5:
                    colors.append('#2E7D32')  # Green for positive
                elif val < -0.5:
                    colors.append('#C62828')  # Red for negative
                else:
                    colors.append('#757575')  # Gray for near-zero

            # Create vertical bar chart
            x_pos = range(len(symbols))
            bars = ax.bar(x_pos, values, color=colors, alpha=0.8, width=0.7)

            # Set x-axis labels
            ax.set_xticks(x_pos)
            ax.set_xticklabels(symbols, rotation=45, ha='right')

            # Add value labels on bars
            for i, (bar, val) in enumerate(zip(bars, values)):
                y_offset = 0.02 * (max(values) - min(values)) if len(values) > 0 else 0.1
                if val >= 0:
                    y_pos = val + y_offset
                    va = 'bottom'
                else:
                    y_pos = val - y_offset
                    va = 'top'
                ax.text(i, y_pos, f'{val:.2f}', ha='center', va=va, fontsize=8)

            # Styling
            ax.set_ylabel(chart_metric, fontsize=10)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            return True

        # Combined function to create table + chart
        def create_combined_visualization(df, chart_metric, title_prefix, filename):
            """Create combined table and chart in one figure - chart above table"""
            from matplotlib.gridspec import GridSpec

            # Wide format: 100% wider, 50% shorter
            fig_width = 24  # Doubled from 12

            # Calculate heights - reduced by 50%
            chart_height = 4  # Reduced from 8
            table_height = fig_height * 0.65  # Reduced
            combined_height = chart_height + table_height + 0.5  # Minimal padding

            # Create figure with GridSpec for vertical layout
            fig = plt.figure(figsize=(fig_width, combined_height))
            # 2 rows, 1 column - CHART on top, TABLE on bottom
            # Adjusted hspace to prevent overlap between chart x-axis and table title
            # Set bottom to 0 to maximize table space
            gs = GridSpec(2, 1, figure=fig, height_ratios=[chart_height, table_height],
                         hspace=0.15, top=0.95, bottom=0.00)

            # Create subplots
            ax_chart = fig.add_subplot(gs[0])
            ax_table = fig.add_subplot(gs[1])

            # Draw chart first (on top)
            chart_success = draw_chart_on_axis(ax_chart, df, chart_metric)

            # Draw table below
            table_title = f'{title_prefix} {rows_to_display} Assets by {sort_column}'
            draw_table_on_axis(ax_table, df, table_title)

            # Add overall title and subtitle with proper spacing
            if subtitle:
                # Place subtitle at very top
                fig.text(0.5, 0.985, subtitle, ha='center', va='top', fontsize=11)
                # Place main title slightly below
                fig.text(0.5, 0.965, f'{title_prefix} {rows_to_display} Assets',
                        ha='center', va='top', fontsize=16, fontweight='bold')
            else:
                fig.suptitle(f'{title_prefix} {rows_to_display} Assets',
                           fontsize=16, fontweight='bold', y=0.98)

            # Ensure output directory exists
            if not os.path.exists(OUTPUT_DIR):
                try:
                    os.makedirs(OUTPUT_DIR)
                except OSError as e:
                    print(f"Error creating directory {OUTPUT_DIR}: {e}")
                    return

            # Save figure
            out_path = os.path.join(OUTPUT_DIR, filename)
            plt.savefig(out_path, bbox_inches='tight', dpi=300)
            plt.close()
            print(f"  Created {filename}")

        # Derive base name
        base_name = os.path.splitext(input_filename)[0]

        # Top N (Gainers)
        top_n = df_sorted.head(rows_to_display)

        # Bottom N (Losers)
        bottom_n = df_sorted.tail(rows_to_display).sort_values(by=actual_sort_col, ascending=True)

        # Use chart_metric if specified, otherwise fall back to sort_column
        metric_to_chart = chart_metric if chart_metric else sort_column

        # Generate combined visualizations (table + chart in one file)
        create_combined_visualization(top_n, metric_to_chart, 'Top', f'{base_name}_top.png')
        create_combined_visualization(bottom_n, metric_to_chart, 'Bottom', f'{base_name}_bottom.png')
        
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
    chart_metric = None # Default to None (will use sort_column)
    generate_charts = True # Default
    generate_tables = True # Default

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

        if line.startswith('CHART_METRIC'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    chart_metric = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing chart metric: {e}")

        if line.startswith('GENERATE_CHARTS'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    value = parts[1].strip()
                    generate_charts = value.lower() in ['true', '1', 'yes']
            except Exception as e:
                print(f"Error parsing generate charts: {e}")

        if line.startswith('GENERATE_TABLES'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    value = parts[1].strip()
                    generate_tables = value.lower() in ['true', '1', 'yes']
            except Exception as e:
                print(f"Error parsing generate tables: {e}")

        if line.startswith('ROWS_TO_DISPLAY'):
             try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    rows_to_display = int(parts[1].strip())
             except Exception as e:
                 print(f"Error parsing rows to display: {e}")

    return files, columns_to_keep, sort_column, rows_to_display, chart_metric, generate_charts, generate_tables

def main():
    config_path = CONFIG_FILE
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    print(f"Reading config from: {config_path}")
    files, columns_to_keep, sort_column, rows_to_display, chart_metric, generate_charts, generate_tables = parse_config(config_path)

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
    print(f"  Chart Metric: {chart_metric if chart_metric else sort_column}")
    print(f"  Generate Charts: {generate_charts}")
    print(f"  Generate Tables: {generate_tables}")
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
        process_csv(filename, columns_to_keep, sort_column, rows_to_display,
                   chart_metric, generate_charts, generate_tables)

if __name__ == "__main__":
    main()
