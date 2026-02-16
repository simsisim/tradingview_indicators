"""
PV Gap Screener Visualization Generator

Generates combined chart+table visualizations for PV breakout and gap signals.
Reads configuration from config_pv_screener.txt
"""

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
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config_pv_screener.txt')
# Output directory to png subdirectory
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'png')

def process_csv(input_csv_path, columns_to_keep, sort_column, rows_to_display,
                chart_metric=None, filter_expression='', sort_ascending=False,
                show_bottom=True, sort_columns=None, sort_ascending_list=None):
    # If path is relative, join with WORK_DIR, else use as is
    if not os.path.isabs(input_csv_path):
        input_csv_path = os.path.join(WORK_DIR, input_csv_path)

    input_filename = os.path.basename(input_csv_path)
    print(f"Processing: {input_filename}...")

    try:
        # Load Data
        df = pd.read_csv(input_csv_path)
        print(f"  Loaded: {len(df)} rows")

        # Apply filter if specified
        if filter_expression:
            try:
                df_filtered = df.query(filter_expression)
                print(f"  Filtered: {len(df)} → {len(df_filtered)} rows (filter: {filter_expression})")
                if len(df_filtered) == 0:
                    print(f"  Warning: No rows match filter. Skipping file.")
                    return
            except Exception as e:
                print(f"  Warning: Filter failed: {e}. Using all rows.")
                df_filtered = df
        else:
            df_filtered = df

        # Select Columns
        available_columns = [col for col in columns_to_keep if col in df_filtered.columns]
        if len(available_columns) != len(columns_to_keep):
            missing = set(columns_to_keep) - set(available_columns)
            print(f"  Warning: Missing columns in {input_filename}: {missing}")

        df_selected = df_filtered[available_columns].copy()

        # Handle missing values
        # Replace empty strings with NaN
        df_selected = df_selected.replace('', pd.NA)

        # Fill numeric columns with 0
        numeric_cols = df_selected.select_dtypes(include=['float', 'float64', 'int', 'int64']).columns
        df_selected[numeric_cols] = df_selected[numeric_cols].fillna(0)

        # Fill string columns with '-'
        string_cols = df_selected.select_dtypes(include=['object']).columns
        df_selected[string_cols] = df_selected[string_cols].fillna('-')

        # Round numeric columns to 2 decimal places
        float_cols = df_selected.select_dtypes(include=['float', 'float64']).columns
        df_selected[float_cols] = df_selected[float_cols].round(2)

        # Format date columns (convert YYYYMMDD float to YYYY-MM-DD string)
        date_columns = [col for col in df_selected.columns if 'Date' in col]
        for col in date_columns:
            def format_date(val):
                if pd.isna(val) or val == 0:
                    return '-'
                # Convert float to int to string, then format
                date_str = str(int(val))
                if len(date_str) == 8:
                    return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
                return str(val)

            df_selected[col] = df_selected[col].apply(format_date)

        # Sort (supports multi-column sorting)
        if sort_columns and sort_ascending_list:
            # Multi-column sort
            for col in sort_columns:
                if col not in df_selected.columns:
                    print(f"  Error: Sort column '{col}' not found in data.")
                    return

            df_sorted = df_selected.sort_values(by=sort_columns, ascending=sort_ascending_list)
            sort_desc = ', '.join([f"{col} ({'asc' if asc else 'desc'})"
                                   for col, asc in zip(sort_columns, sort_ascending_list)])
            print(f"  Sorted by: {sort_desc}")
        else:
            # Single column sort (backward compatibility)
            if sort_column not in df_selected.columns:
                print(f"  Error: Sort column '{sort_column}' not found in data.")
                return

            df_sorted = df_selected.sort_values(by=sort_column, ascending=sort_ascending)
            print(f"  Sorted by '{sort_column}' ({'ascending' if sort_ascending else 'descending'})")

        # Check if we have enough rows
        if len(df_sorted) < rows_to_display:
            print(f"  Note: Only {len(df_sorted)} rows available (requested {rows_to_display})")
            actual_rows = len(df_sorted)
        else:
            actual_rows = rows_to_display

        # Extract date and week from filename
        base_name_no_ext = os.path.splitext(input_filename)[0]
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})$', base_name_no_ext)
        subtitle = ""
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                week_num = dt.isocalendar()[1]
                subtitle = f"PV Gap Screener | Date: {date_str} | Week: {week_num}"
            except ValueError:
                pass

        # Define column widths dynamically for PV screener columns
        final_widths = []
        flexible_cols_count = 0
        used_width = 0.0

        for col_name in df_sorted.columns:
            if col_name == 'Symbol':
                w = 0.08
                final_widths.append(w)
                used_width += w
            elif col_name == 'Description':
                w = 0.25
                final_widths.append(w)
                used_width += w
            elif 'Flag' in col_name or 'Direction' in col_name:
                w = 0.04  # Small for flags
                final_widths.append(w)
                used_width += w
            elif 'Date' in col_name:
                w = 0.08  # Date columns
                final_widths.append(w)
                used_width += w
            elif 'Days Ago' in col_name or 'Type' in col_name:
                w = 0.06  # Small integers
                final_widths.append(w)
                used_width += w
            else:
                final_widths.append(None) # Mark for flexible width
                flexible_cols_count += 1

        # Distribute remaining width
        remaining_width = 1.0 - used_width

        if flexible_cols_count > 0:
            flex_width = max(0.01, remaining_width / flexible_cols_count)
            col_widths = [w if w is not None else flex_width for w in final_widths]
        else:
            col_widths = final_widths

        # Calculate dynamic figure height based on rows
        fig_height = 2 + (actual_rows * 0.45)

        # Helper function to draw table on an axis
        def draw_table_on_axis(ax, df, title):
            import textwrap
            from datetime import datetime

            ax.axis('off')
            ax.axis('tight')

            # Identify date columns for special coloring
            date_col_indices = [i for i, col in enumerate(df.columns) if 'Date' in col]

            # Find Symbol column index
            symbol_col_index = df.columns.get_loc('Symbol') if 'Symbol' in df.columns else -1

            # Check if 'Price vs SMA %' exists for conditional coloring
            has_price_sma = 'Price vs SMA %' in df.columns
            if has_price_sma:
                price_sma_values = df['Price vs SMA %'].values
            else:
                price_sma_values = None

            # Check if both date columns exist for date proximity check
            has_both_dates = 'PV Breakout Date' in df.columns and 'Gap1 Date' in df.columns
            if has_both_dates and has_price_sma:
                def dates_within_3_days(pv_date_str, gap_date_str):
                    """Check if two dates are within 3 days of each other"""
                    try:
                        if pv_date_str == '-' or gap_date_str == '-':
                            return False
                        pv_date = datetime.strptime(pv_date_str, '%Y-%m-%d')
                        gap_date = datetime.strptime(gap_date_str, '%Y-%m-%d')
                        diff = abs((pv_date - gap_date).days)
                        return diff <= 3
                    except:
                        return False

                # Identify rows where BOTH conditions are met:
                # 1. Dates are within 3 days AND
                # 2. Price vs SMA % > 0
                close_date_rows = []
                for i in range(len(df)):
                    pv_date = df.iloc[i]['PV Breakout Date']
                    gap_date = df.iloc[i]['Gap1 Date']
                    price_sma = price_sma_values[i]
                    if dates_within_3_days(pv_date, gap_date) and price_sma > 0:
                        close_date_rows.append(i)
            else:
                close_date_rows = []

            # Prepare alternating row colors with special coloring
            colors = []
            for i in range(len(df)):
                row_colors = []
                # Check if this row should be fully green (dates within 3 days)
                is_close_date_row = i in close_date_rows

                for j, col in enumerate(df.columns):
                    if is_close_date_row:
                        # Entire row green when PV and Gap dates are close (except dates stay pink)
                        if j in date_col_indices:
                            row_colors.append('#FFE6E6')  # Keep dates pink
                        else:
                            row_colors.append('#A5D6A7')  # Medium green for close dates
                    elif j in date_col_indices:
                        # Pink/red background for date columns
                        row_colors.append('#FFE6E6')
                    elif j == symbol_col_index and price_sma_values is not None:
                        # Green background for Symbol if Price vs SMA % is positive
                        if price_sma_values[i] > 0:
                            row_colors.append('#C8E6C9')  # Light green
                        elif i % 2 != 0:
                            row_colors.append('#E0E0E0')
                        else:
                            row_colors.append('w')
                    elif i % 2 != 0:
                        row_colors.append('#E0E0E0')
                    else:
                        row_colors.append('w')
                colors.append(row_colors)

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
                y_offset = 0.02 * (max(values) - min(values)) if len(values) > 0 and max(values) != min(values) else 0.1
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
            gs = GridSpec(2, 1, figure=fig, height_ratios=[chart_height, table_height],
                         hspace=0.15, top=0.95, bottom=0.00)

            # Create subplots
            ax_chart = fig.add_subplot(gs[0])
            ax_table = fig.add_subplot(gs[1])

            # Draw chart first (on top)
            chart_success = draw_chart_on_axis(ax_chart, df, chart_metric)

            # Draw table below
            table_title = f'{title_prefix} {actual_rows} Assets by {primary_sort}'
            draw_table_on_axis(ax_table, df, table_title)

            # Add overall title and subtitle with proper spacing
            if subtitle:
                # Place subtitle at very top
                fig.text(0.5, 0.985, subtitle, ha='center', va='top', fontsize=11)
                # Place main title slightly below
                fig.text(0.5, 0.965, f'{title_prefix} {actual_rows} Assets',
                        ha='center', va='top', fontsize=16, fontweight='bold')
            else:
                fig.suptitle(f'{title_prefix} {actual_rows} Assets',
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

        # Determine sort description for titles
        if sort_columns and sort_ascending_list:
            primary_sort = sort_columns[0]
        else:
            primary_sort = sort_column

        # Top N
        top_n = df_sorted.head(actual_rows)

        # Use chart_metric if specified, otherwise fall back to primary sort column
        metric_to_chart = chart_metric if chart_metric else primary_sort

        # Create TradingView watchlist
        def create_tradingview_watchlist():
            """Create TradingView watchlist for stocks with recent PV and Gap signals"""
            # Filter for stocks with both PV Days Ago < 20 AND Gap Days Ago < 20
            if 'PV Days Ago' in df_sorted.columns and 'Gap1 Days Ago' in df_sorted.columns:
                watchlist_df = df_sorted[
                    (df_sorted['PV Days Ago'] < 20) &
                    (df_sorted['Gap1 Days Ago'] < 20)
                ].copy()

                if len(watchlist_df) > 0:
                    # Sort by PV Days Ago first, then Gap1 Size %
                    if 'Gap1 Size %' in watchlist_df.columns:
                        watchlist_df = watchlist_df.sort_values(
                            by=['PV Days Ago', 'Gap1 Size %'],
                            ascending=[True, False]
                        )
                    else:
                        watchlist_df = watchlist_df.sort_values(by='PV Days Ago', ascending=True)

                    # Get symbols
                    symbols = watchlist_df['Symbol'].tolist()

                    # Extract date from filename (last _YYYY-MM-DD before .csv)
                    date_match = re.search(r'_(\d{4}-\d{2}-\d{2})\.csv$', input_filename)
                    if date_match:
                        file_date = date_match.group(1)
                        watchlist_filename = f'io-PVscreener_{file_date}.txt'
                    else:
                        watchlist_filename = 'io-PVscreener.txt'

                    watchlist_path = os.path.join(OUTPUT_DIR, watchlist_filename)

                    with open(watchlist_path, 'w') as f:
                        # Write header comment
                        f.write(f"# TradingView Watchlist: io-PVscreener\n")
                        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"# Filter: PV Days Ago < 20 AND Gap Days Ago < 20\n")
                        f.write(f"# Stocks: {len(symbols)}\n")
                        f.write(f"# Sort: PV Days Ago (asc), Gap1 Size % (desc)\n")
                        f.write(f"#\n")

                        # Write symbols (one per line)
                        for symbol in symbols:
                            f.write(f"{symbol}\n")

                    print(f"  Created TradingView watchlist: {watchlist_filename} ({len(symbols)} symbols)")
                else:
                    print(f"  No stocks match watchlist criteria (PV Days Ago < 20 AND Gap Days Ago < 20)")
            else:
                print(f"  Skipping watchlist creation: Required columns not found")

        create_tradingview_watchlist()

        # Generate visualizations
        create_combined_visualization(top_n, metric_to_chart, 'Top', f'{base_name}_top.png')

        if show_bottom:
            # Bottom N (reverse the sort for bottom)
            if sort_columns and sort_ascending_list:
                # For multi-sort, reverse all ascending flags
                bottom_n = df_sorted.tail(actual_rows).sort_values(
                    by=sort_columns,
                    ascending=[not asc for asc in sort_ascending_list])
            else:
                bottom_n = df_sorted.tail(actual_rows).sort_values(
                    by=sort_column,
                    ascending=not sort_ascending)

            create_combined_visualization(bottom_n, metric_to_chart, 'Bottom', f'{base_name}_bottom.png')

    except FileNotFoundError:
        print(f"  Error: Could not find file {input_csv_path}")
    except pd.errors.EmptyDataError:
        print(f"  Error: File {input_filename} is empty")
    except KeyError as e:
        print(f"  Error: Missing column in CSV - {e}")
    except Exception as e:
        print(f"  An error occurred processing {input_filename}: {e}")
        import traceback
        traceback.print_exc()

def parse_config(config_path):
    files = []
    columns_to_keep = []
    sort_column = ''
    rows_to_display = 20 # Default
    chart_metric = None # Default to None (will use sort_column)
    filter_expression = '' # Default no filter
    sort_ascending = False # Default descending
    show_bottom = True # Default show bottom chart
    sort_columns = None # For multi-column sort
    sort_ascending_list = None # For multi-column sort

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
                section = None
            continue

        if section == 'files':
            files.append(line)

        if line.startswith('COLUMNS_TO_KEEP'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    columns_to_keep = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing columns: {e}")

        if line.startswith('SORT_COLUMNS'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    sort_columns = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing sort columns: {e}")

        if line.startswith('SORT_COLUMN') and not line.startswith('SORT_COLUMNS'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    sort_column = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing sort column: {e}")

        if line.startswith('SORT_ASCENDING'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    value = parts[1].strip()
                    # Try to parse as list first (for multi-column)
                    try:
                        sort_ascending_list = ast.literal_eval(value)
                        if not isinstance(sort_ascending_list, list):
                            sort_ascending_list = None
                            raise ValueError()
                    except:
                        # Parse as boolean (for single column)
                        sort_ascending = value.lower() in ['true', '1', 'yes']
                        sort_ascending_list = None
            except Exception as e:
                print(f"Error parsing sort ascending: {e}")

        if line.startswith('SHOW_BOTTOM'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    value = parts[1].strip()
                    show_bottom = value.lower() in ['true', '1', 'yes']
            except Exception as e:
                print(f"Error parsing show bottom: {e}")

        if line.startswith('CHART_METRIC'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    chart_metric = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing chart metric: {e}")

        if line.startswith('FILTER_EXPRESSION'):
            try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    filter_expression = ast.literal_eval(parts[1].strip())
            except Exception as e:
                print(f"Error parsing filter expression: {e}")

        if line.startswith('ROWS_TO_DISPLAY'):
             try:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    rows_to_display = int(parts[1].strip())
             except Exception as e:
                 print(f"Error parsing rows to display: {e}")

    return files, columns_to_keep, sort_column, rows_to_display, chart_metric, filter_expression, sort_ascending, show_bottom, sort_columns, sort_ascending_list

def main():
    config_path = CONFIG_FILE
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    print(f"Reading config from: {config_path}")
    files, columns_to_keep, sort_column, rows_to_display, chart_metric, filter_expression, sort_ascending, show_bottom, sort_columns, sort_ascending_list = parse_config(config_path)

    # Ensure Output Directory Exists
    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating output directory: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    else:
        print(f"Output directory: {OUTPUT_DIR}")

    print(f"Config:")
    print(f"  Files: {len(files)}")
    print(f"  Columns: {columns_to_keep}")

    if sort_columns and sort_ascending_list:
        sort_desc = ', '.join([f"{col} ({'asc' if asc else 'desc'})"
                               for col, asc in zip(sort_columns, sort_ascending_list)])
        print(f"  Sort By: {sort_desc}")
    else:
        print(f"  Sort By: {sort_column} ({'ascending' if sort_ascending else 'descending'})")

    print(f"  Chart Metric: {chart_metric if chart_metric else (sort_columns[0] if sort_columns else sort_column)}")
    print(f"  Filter: {filter_expression if filter_expression else 'None'}")
    print(f"  Show Bottom: {show_bottom}")
    print(f"  Rows to Display: {rows_to_display}")

    if not files:
        print("No files found in config.")
        return

    if not columns_to_keep:
        print("Error: No columns defined.")
        return

    if not sort_column and not sort_columns:
        print("Error: No sort column defined.")
        return

    for filename in files:
        process_csv(filename, columns_to_keep, sort_column, rows_to_display,
                   chart_metric, filter_expression, sort_ascending,
                   show_bottom, sort_columns, sort_ascending_list)

if __name__ == "__main__":
    main()
