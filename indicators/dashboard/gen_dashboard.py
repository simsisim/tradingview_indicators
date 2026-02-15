#!/usr/bin/env python3
"""
Generate TradingView Pine Script dashboard from watchlist CSV

USAGE:
    python3 gen_dashboard.py [input_csv] [output_pine]

EXAMPLES:
    # Use default files (watchlist.csv -> dashboard.pine)
    python3 gen_dashboard.py

    # Specify custom input CSV
    python3 gen_dashboard.py my_watchlist.csv

    # Specify both input and output files
    python3 gen_dashboard.py watchlist.csv custom_dashboard.pine

CSV FORMAT:
    The CSV file must have these columns:
    - Ticker: Stock symbol (e.g., AAPL, TSLA, GETTEX:RHM)
    - Trigger: Entry/trigger price
    - Stop: Stop loss price
    - Notes: Industry or notes about the stock

FEATURES GENERATED:
    - 20 symbol slots (auto-populated from CSV)
    - Separate Pre-MP and Post-MP columns
    - EMA 10, EMA 20, SMA 50 metrics
    - Separated metrics and distance columns
    - SlingShot signals
    - Price/Volume Breakout detection
    - Candle pattern recognition (Kicker, Oops, OEL/OEH, Inside/Engulf, 3Bar)
    - Risk:Reward calculations
    - Previous Day High/Low levels
"""

import pandas as pd
import os
from typing import List

def read_watchlist_csv(csv_file_path: str = 'watchlist.csv') -> pd.DataFrame:
    """Read and clean the watchlist CSV data."""
    try:
        # Read CSV
        df = pd.read_csv(csv_file_path)

        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()

        # Ensure required columns exist
        required_columns = ['Ticker', 'Trigger', 'Stop', 'Notes']
        for col in required_columns:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in CSV")

        # Fill NaN values appropriately
        df['Ticker'] = df['Ticker'].fillna('')
        df['Trigger'] = df['Trigger'].fillna('')
        df['Stop'] = df['Stop'].fillna('')
        df['Notes'] = df['Notes'].fillna('')

        # Remove empty rows (rows with no ticker)
        df = df[df['Ticker'].str.strip() != '']

        return df

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()


def generate_symbol_inputs(df: pd.DataFrame, max_symbols: int = 20) -> str:
    """Generate the symbol input sections for PineScript."""
    symbol_inputs = []

    for i in range(1, max_symbols + 1):
        if i <= len(df):
            row = df.iloc[i-1]
            ticker = str(row['Ticker']).strip() if pd.notna(row['Ticker']) else ''
            name = ticker  # Use ticker as name
            trigger = str(row['Trigger']).strip() if pd.notna(row['Trigger']) and str(row['Trigger']).strip() != '' else ''
            stop = str(row['Stop']).strip() if pd.notna(row['Stop']) and str(row['Stop']).strip() != '' else ''
            notes = str(row['Notes']).strip() if pd.notna(row['Notes']) else ''

            # Escape single quotes in notes for PineScript
            notes = notes.replace("'", "\\'")

            show = 'true' if ticker != '' else 'false'
        else:
            ticker = ''
            name = ''
            trigger = ''
            stop = ''
            notes = ''
            show = 'false'

        symbol_input = f"""show_{i} = input.bool({show}, '', group='Symbols', inline='Line {i}', display = display.none)
ticker_{i} = input.symbol('{ticker}', '', group='Symbols', inline='Line {i}', display = display.none)
name_{i} = input.string('{name}', '', group='Symbols', inline='Line {i}', display = display.none)
trigger_{i} = input.string('{trigger}', 'Trigger', group='Symbols', inline='Line {i}', display = display.none)
stop_{i} = input.string('{stop}', 'Stop', group='Symbols', inline='Line {i}', display = display.none)
notes_{i} = input.string('{notes}', 'Notes', group='Symbols', inline='Line {i}', display = display.none)
bg_{i} = input.color(color.new(#909090, 70), '', group='Symbols', inline='Line {i}', display = display.none)
txt_{i} = input.color(#d6d6d6, '', group='Symbols', inline='Line {i}', display = display.none)"""

        symbol_inputs.append(symbol_input)

    return '\n\n'.join(symbol_inputs)


def generate_table_rows(max_symbols: int = 20) -> str:
    """Generate the table row filling code."""
    table_rows = []

    for i in range(1, max_symbols + 1):
        table_row = f"""[s{i}_sling, s{i}_slingprice] = _sling(ticker_{i}, sling_ema_len)
[s{i}_pv_signal, s{i}_pv_price] = _pv_breakout(ticker_{i}, pv_price_period, pv_volume_period, pv_trendline_length)
[s{i}_kicker, s{i}_oel, s{i}_oeh, s{i}_oopsUp, s{i}_oopsDn, s{i}_inside, s{i}_engulf, s{i}_b3Up, s{i}_b3Dn] = combo_data(ticker_{i})
s{i}_pdh = _pdh(ticker_{i})
s{i}_pdl = _pdl(ticker_{i})
row := _t(show_{i}, ticker_{i}, name_{i}, txt_{i}, bg_{i}, _val(ticker_{i}, name_{i}), trigger_{i}, stop_{i}, notes_{i}, row, s{i}_sling, s{i}_slingprice, s{i}_pv_signal, s{i}_pv_price, s{i}_kicker, s{i}_oopsUp, s{i}_oopsDn, s{i}_oel, s{i}_oeh, s{i}_inside, s{i}_engulf, s{i}_b3Up, s{i}_b3Dn, s{i}_pdh, s{i}_pdl, {i-1})"""

        table_rows.append(table_row)

    return '\n\n'.join(table_rows)


def get_template_header() -> str:
    """Return the header part of the Pine Script template (before symbol inputs)."""
    return """// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © valpatradd

//@version=6
indicator('Custom Performance Table - Dashboard', 'Dashboard', true)

// ---- Combo Input Toggles ----
var gCombo = 'Candle Combos'
kickerBool   = input.bool(true, 'Kicker', inline='c1', group=gCombo)
oopsBool     = input.bool(true, 'Oops', inline='c1', group=gCombo)
oelBool      = input.bool(true, 'Open=High/Low', inline='c1', group=gCombo)
insideBool   = input.bool(true, 'Inside/Engulf', inline='c2', group=gCombo)
threeBarBool = input.bool(true, '3 Bar Break', inline='c2', group=gCombo)

val = input.string('Chg %', 'Performance', ['Chg %'], display = display.none)
val_ema1 = input.string('EMA 10', 'Metric1', options=['EMA 10', 'EMA 20', 'SMA 50'], display = display.none)
val_ema2 = input.string('EMA 20', 'Metric2', options=['EMA 10', 'EMA 20', 'SMA 50'], display = display.none)
val_ema3 = input.string('SMA 50', 'Metric3', options=['EMA 10', 'EMA 20', 'SMA 50'], display = display.none)

sling_ema_len = input.int(4, "Slingshot EMA Length", minval=1, group="Slingshot")

// Price and Volume Breakout - Updated to match TradeDots original logic
pv_price_period = input.int(60, "Price Breakout Period", minval=1, group="Price & Volume Breakout")
pv_volume_period = input.int(60, "Volume Breakout Period", minval=1, group="Price & Volume Breakout")
pv_trendline_length = input.int(200, "Trendline Length", minval=1, group="Price & Volume Breakout")

// Z-Score and RAROC parameters removed - only Chg % performance used

// ---- Column Visibility Controls ----
var gColVis = 'Column Visibility'
show_basic = input.bool(true, 'Basic Info (Name, Price, Chg Open %, Performance)', group=gColVis)
show_premp = input.bool(false, 'Pre-MP', group=gColVis)
show_postmp = input.bool(false, 'Post-MP', group=gColVis)
show_price_levels = input.bool(true, 'Price Levels (PDL, PDH after Name)', group=gColVis)
show_metrics = input.bool(true, 'Metrics (EMA/SMA)', group=gColVis)
show_distances = input.bool(true, 'Distances to Metrics', group=gColVis)
show_trading = input.bool(true, 'Trading (Trigger, Stop, R:R)', group=gColVis)
show_slingshot = input.bool(true, 'SlingShot Signals', group=gColVis)
show_pv_breakout = input.bool(true, 'Price/Volume Breakout', group=gColVis)
show_combos = input.bool(true, 'Candle Combos', group=gColVis)
show_notes = input.bool(true, 'Industry', group=gColVis)

// ---- Performance Table Controls ----
// MODE selector: user chooses Label or Tooltip for symbol column
_name(_str) =>
    string[] parts = str.split(_str, ":")
    array.size(parts) > 1 ? array.get(parts, 1) : _str

mode = input.string('Name', 'Mode', ['Name', 'Tooltip'], group='Symbols', inline='Mode', display = display.none)

tf = input.timeframe('', 'Timeframe', group='Timeframe', inline='TF', display = display.none)
force_iday = input.bool(true, 'Force on Intraday', group='Timeframe', inline='Force', display = display.none)
in_force_tf = input.string('Daily', '', ['Daily', 'Weekly', 'Monthly', 'Yearly'], group='Timeframe', inline='Force', display = display.none)
force_tf = switch in_force_tf
    'Daily'   => 'D'
    'Weekly'  => 'W'
    'Monthly' => 'M'
    'Yearly'  => '12M'

input_tab_pos = input.string('Top Left', 'Position', ['Top Left', 'Top Center', 'Top Right', 'Middle Left', 'Middle Center', 'Middle Right', 'Bottom Left', 'Bottom Center', 'Bottom Right'], group='Table')
tab_pos = switch input_tab_pos
    'Top Left'    => position.top_left
    'Top Center'  => position.top_center
    'Top Right'   => position.top_right
    'Middle Left' => position.middle_left
    'Middle Center' => position.middle_center
    'Middle Right' => position.middle_right
    'Bottom Left'  => position.bottom_left
    'Bottom Center' => position.bottom_center
    'Bottom Right' => position.bottom_right

col_offset = input.int(0, 'Offset:  Horizontal', 0, group='Table', tooltip='Shifts the table to the right.')
row_offset = input.int(0, '             Vertical      ', 0, group='Table', inline='Offset', tooltip='Shifts the table downward.')
input_tab_size = input.string('Auto', 'Size', group='Table', options=['Auto', 'Tiny', 'Small', 'Normal', 'Large', 'Huge'])
tab_size = switch input_tab_size
    'Auto'   => size.auto
    'Tiny'   => size.tiny
    'Small'  => size.small
    'Normal' => size.normal
    'Large'  => size.large
    'Huge'   => size.huge

in_font = input.string('Default', 'Text Font', ['Default', 'Monospace'], group='Table')
font = switch in_font
    'Default'   => font.family_default
    'Monospace' => font.family_monospace

col_f = input.color(color.new(#363A45, 100), 'Frame', group='Table', inline='Frame')
w_f = input.int(0, '', 0, group='Table', inline='Frame')
col_b = input.color(color.new(#363A45, 100), 'Border', group='Table', inline='Border')
w_b = input.int(1, '', 0, group='Table', inline='Border')

// ---- SYMBOLS 1-20 ----
"""


def get_template_middle() -> str:
    """Return the middle part of the template (between symbols and table rows)."""
    return """
// ---- PERFORMANCE METRIC FUNCTIONS ----
custom_tf = timeframe.in_seconds(force_iday and timeframe.isintraday ? force_tf : tf)
chart_tf = timeframe.in_seconds(timeframe.period)
if chart_tf > custom_tf
    runtime.error('The selected timeframe is lower than the current chart timeframe.')

_chg(ticker) =>
    [c, c1] = request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, [close, close[1]])
    if na(c) or na(c1)
        na
    else
        chg = (c - c1) / c1 * 100
        chg := math.abs(chg) > 1e6 ? na : chg
        chg

_val(ticker, name) =>
    ticker == '' or name == '-' ? na : _chg(ticker)

// New: Previous Day High/Low and Market Sessions
_pdh(ticker) => request.security(ticker, "D", high[1])
_pdl(ticker) => request.security(ticker, "D", low[1])
_premarket_chg(ticker) =>
    d_close_prev = request.security(ticker, "D", close[1])
    d_open = request.security(ticker, "D", open)
    na(d_close_prev) or na(d_open) ? na : (d_open - d_close_prev) / d_close_prev * 100
_postmarket_chg(ticker) =>
    // Simplified post-market: always return 0.0 since market isn't closed during trading hours
    0.0
// Price/metrics helpers
_price(ticker) => request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, close)
_open(ticker)  => request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, open)
_metric_val(ticker, metric) =>
    tf_used = force_iday and timeframe.isintraday ? force_tf : tf
    price_series = request.security(ticker, tf_used, close)
    if metric == 'EMA 10'
        ta.ema(price_series, 10)
    else if metric == 'EMA 20'
        ta.ema(price_series, 20)
    else if metric == 'SMA 50'
        ta.sma(price_series, 50)
    else
        na
_dist(price, metric_value) =>
    na(price) or na(metric_value) or metric_value == 0 ? na : (price - metric_value) / metric_value * 100

// Helper functions to determine colors based on value comparison with price
_get_value_text_color(value_str, price) =>
    color.white  // Always white text for better contrast

_get_value_bg_color(value_str, price) =>
    if value_str == '' or na(price)
        color.new(#2D3748, 0)  // Neutral dark gray
    else
        value_num = str.tonumber(value_str)
        if na(value_num)
            color.new(#2D3748, 0)  // Neutral dark gray
        else if value_num < 0 or price < value_num
            color.new(#7D1007, 0)  // Dark red background (bearish)
        else
            color.new(#1B4332, 0)  // Dark green background (bullish)

// Slingshot
_sling(ticker, emaLen) =>
    [h, c, c1, c2, c3] = request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, [high, close, close[1], close[2], close[3]])
    ema  = request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, ta.ema(high, emaLen))
    ema1 = request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, ta.ema(high, emaLen)[1])
    ema2 = request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, ta.ema(high, emaLen)[2])
    ema3 = request.security(ticker, force_iday and timeframe.isintraday ? force_tf : tf, ta.ema(high, emaLen)[3])
    sling = c > ema and c1 < ema1 and c2 < ema2 and c3 < ema3
    [sling, sling ? c : na]

_pv_breakout(ticker, price_period, volume_period, trendline_length) =>
    tf_used = force_iday and timeframe.isintraday ? force_tf : tf
    [close_series, high_series, low_series, volume_series] = request.security(ticker, tf_used, [close, high, low, volume])

    // Calculate breakout levels (matching original TradeDots logic)
    price_highest = ta.highest(high_series, price_period)  // Highest high over period
    price_lowest = ta.lowest(low_series, price_period)     // Lowest low over period
    volume_highest = ta.highest(volume_series, volume_period)  // Highest volume over period

    // Calculate trendline (SMA of close)
    trendline = ta.sma(close_series, trendline_length)

    // Long breakout conditions (original TradeDots logic)
    long_price_breakout = close_series > price_highest[1]  // Close above previous highest high
    long_volume_breakout = volume_series > volume_highest[1]  // Volume above previous highest volume
    long_trend_filter = close_series > trendline  // Close above trendline

    // Short breakout conditions (original TradeDots logic)
    short_price_breakout = close_series < price_lowest[1]  // Close below previous lowest low
    short_volume_breakout = volume_series > volume_highest[1]  // Volume above previous highest volume
    short_trend_filter = close_series < trendline  // Close below trendline

    // Combined signals
    long_breakout = long_price_breakout and long_volume_breakout and long_trend_filter
    short_breakout = short_price_breakout and short_volume_breakout and short_trend_filter

    // Return signal type and breakout price
    signal = long_breakout ? "Long" : short_breakout ? "Short" : ""
    breakout_price = (long_breakout or short_breakout) ? close_series : na

    [signal, breakout_price]

// ---- CANDLESTICK COMBOS: CCS INTEGRATION ----
combo_data(ticker) =>
    [kicker, oel, oeh, oopsUp, oopsDn, inside, engulf, b3Up] = request.security(ticker, "D", [close[1] < open[1] and open > open[1], open == low, open == high, open < low[1] and close > low[1], open > high[1] and close <= high[1], high <= high[1] and low >= low[1], high > high[1] and low < low[1], high[1] < high[3] and close > high[1] and close > high[2] and close > high[3]])
    b3Dn = request.security(ticker, "D", low[1] > low[3] and close < low[1] and close < low[2] and close < low[3])
    [kicker, oel, oeh, oopsUp, oopsDn, inside, engulf, b3Up, b3Dn]

// ---- DYNAMIC COLUMN CALCULATION ----
// Calculate visible columns dynamically
basic_cols = show_basic ? 4 : 0  // Name, Price, Chg Open %, Performance
premp_cols = show_premp ? 1 : 0  // Pre-MP
postmp_cols = show_postmp ? 1 : 0  // Post-MP
price_level_cols = show_price_levels ? 2 : 0  // PDL, PDH (now integrated between Name and Price)
metric_cols = show_metrics ? 3 : 0  // Metric1/2/3 (EMA/SMA values)
distance_cols = show_distances ? 3 : 0  // 3 distance columns
trading_cols = show_trading ? 3 : 0  // Trigger, Stop, R:R
slingshot_cols = show_slingshot ? 2 : 0  // SlingShot?, Trigger Price
pv_breakout_cols = show_pv_breakout ? 2 : 0  // PV Breakout, Breakout Price
combo_cols = show_combos ? 5 : 0  // Kicker, Oops, OEL/OEH, IN/EN, 3Bar
notes_cols = show_notes ? 1 : 0  // Industry

visible_cols = basic_cols + premp_cols + postmp_cols + price_level_cols + metric_cols + distance_cols + trading_cols + slingshot_cols + pv_breakout_cols + combo_cols + notes_cols
total_cols = visible_cols + col_offset

// ---- TABLE ----
tab = table.new(tab_pos, total_cols, 22 + row_offset, frame_color=col_f, frame_width=w_f, border_color=col_b, border_width=w_b)
header_row = row_offset

// ---- DYNAMIC TABLE HEADER GENERATION ----
current_col = col_offset

// Basic Info columns
if show_basic
    table.cell(tab, current_col, header_row, mode == 'Name' ? "Name" : "Ticker", bgcolor=color.gray, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Price Level columns (moved after Name, before Price)
if show_price_levels
    table.cell(tab, current_col, header_row, "PDL", bgcolor=color.gray, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "PDH", bgcolor=color.gray, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Pre-MP column (separate control)
if show_premp
    table.cell(tab, current_col, header_row, "Pre-MP", bgcolor=color.yellow, text_color=color.black, text_size=tab_size, text_font_family=font)
    current_col += 1

if show_basic
    table.cell(tab, current_col, header_row, "Price", bgcolor=color.navy, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Chg Open %", bgcolor=color.gray, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Chg Daily%", bgcolor=color.gray, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Post-MP column (separate control)
if show_postmp
    table.cell(tab, current_col, header_row, "Post-MP", bgcolor=color.yellow, text_color=color.black, text_size=tab_size, text_font_family=font)
    current_col += 1


// Trading columns
if show_trading
    table.cell(tab, current_col, header_row, "Trigger", bgcolor=color.navy, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Stop", bgcolor=color.navy, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "R:R", bgcolor=color.gray, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Slingshot columns
if show_slingshot
    table.cell(tab, current_col, header_row, "SlingShot?", bgcolor=color.new(#B8660A, 50), text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Trigger Price", bgcolor=color.new(#B8660A, 50), text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Price & Volume Breakout columns
if show_pv_breakout
    table.cell(tab, current_col, header_row, "PV Breakout", bgcolor=color.teal, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Breakout Price", bgcolor=color.teal, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Combo columns
if show_combos
    table.cell(tab, current_col, header_row, "Kicker", bgcolor=color.new(color.gray, 75), text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Oops", bgcolor=color.new(color.gray, 85), text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "OEL/OEH", bgcolor=color.new(color.gray, 90), text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "IN/EN", bgcolor=color.new(color.gray, 90), text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "3Bar", bgcolor=color.new(color.gray, 85), text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Metrics columns (EMA/SMA values)
if show_metrics
    table.cell(tab, current_col, header_row, val_ema1, bgcolor=color.navy, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, val_ema2, bgcolor=color.navy, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, val_ema3, bgcolor=color.navy, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Distance columns (separated from metrics)
if show_distances
    table.cell(tab, current_col, header_row, "Dist to " + val_ema1, bgcolor=color.blue, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Dist to " + val_ema2, bgcolor=color.blue, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1
    table.cell(tab, current_col, header_row, "Dist to " + val_ema3, bgcolor=color.blue, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

// Industry column
if show_notes
    table.cell(tab, current_col, header_row, "Industry", bgcolor=color.purple, text_color=color.white, text_size=tab_size, text_font_family=font)
    current_col += 1

fill_offset(row) =>
    if col_offset > 0
        for j = 0 to col_offset - 1
            table.cell(tab, j, row, "", text_color=color.new(color.white, 100))

// Dynamic Table row function with conditional column rendering
_t(show, tkr, name, txtcol, bgcol, chg, trigger, stop, notes, base_row, sling, sling_price, pv_signal, pv_price,
   kicker, oopsUp, oopsDn, oel, oeh, inside, engulf, b3Up, b3Dn, pdh, pdl, symbol_index) =>
    if show and (tkr != '' or name == "-")
        fill_offset(base_row)

        // Calculate all data (only compute what's needed)
        p = show_basic or show_price_levels or show_distances or show_trading ? _price(tkr) : na
        o = show_basic ? _open(tkr) : na
        chg_open = show_basic and not na(o) and not na(p) ? ((p - o) / o * 100) : na
        chg_open_str = show_basic ? (na(chg_open) ? "" : str.tostring(chg_open, format.percent)) : ""

        // Pre-market and Post-market data
        float premarket = show_premp ? _premarket_chg(tkr) : na
        float postmarket = show_postmp ? _postmarket_chg(tkr) : na

        // Metrics (only calculate if needed)
        m1 = show_metrics or show_distances ? _metric_val(tkr, val_ema1) : na
        m2 = show_metrics or show_distances ? _metric_val(tkr, val_ema2) : na
        m3 = show_metrics or show_distances ? _metric_val(tkr, val_ema3) : na
        m1_s = show_metrics ? (na(m1) ? "" : str.tostring(m1, "#.##")) : ""
        m2_s = show_metrics ? (na(m2) ? "" : str.tostring(m2, "#.##")) : ""
        m3_s = show_metrics ? (na(m3) ? "" : str.tostring(m3, "#.##")) : ""
        d1 = show_distances ? _dist(p, m1) : na
        d2 = show_distances ? _dist(p, m2) : na
        d3 = show_distances ? _dist(p, m3) : na
        d1_s = show_distances ? (na(d1) ? "" : str.tostring(d1, "#.##") + "%") : ""
        d2_s = show_distances ? (na(d2) ? "" : str.tostring(d2, "#.##") + "%") : ""
        d3_s = show_distances ? (na(d3) ? "" : str.tostring(d3, "#.##") + "%") : ""

        // Trading data
        trigger_cell = show_trading ? (trigger == '' ? '' : trigger) : ''
        stop_cell = show_trading ? (stop == '' ? '' : stop) : ''
        notes_cell = show_notes ? (notes == '' ? '' : notes) : ''

        // Risk:Reward calculation: (trigger - current_price) / (trigger - stop)
        float rr_ratio = na
        rr_cell = ''
        if show_trading and trigger_cell != '' and stop_cell != '' and not na(p)
            trigger_num = str.tonumber(trigger_cell)
            stop_num = str.tonumber(stop_cell)
            if not na(trigger_num) and not na(stop_num) and trigger_num != stop_num
                reward = trigger_num - p
                risk = trigger_num - stop_num
                if risk != 0
                    rr_ratio := reward / risk
                    rr_cell := str.tostring(rr_ratio, "#.##")

        // Colors
        trigger_txt_color = show_trading ? _get_value_text_color(trigger_cell, p) : color.white
        trigger_bg_color = show_trading ? _get_value_bg_color(trigger_cell, p) : color.new(#2D3748, 0)
        stop_txt_color = show_trading ? _get_value_text_color(stop_cell, p) : color.white
        stop_bg_color = show_trading ? _get_value_bg_color(stop_cell, p) : color.new(#2D3748, 0)

        // R:R colors: green for favorable (>1), red for unfavorable (<1), gray for neutral
        rr_txt_color = show_trading ? color.white : color.white
        rr_bg_color = show_trading ? (rr_cell == '' or na(rr_ratio) ? color.new(#2D3748, 0) : rr_ratio > 1 ? color.new(#1B4332, 0) : rr_ratio < 1 ? color.new(#7D1007, 0) : color.new(#2D3748, 0)) : color.new(#2D3748, 0)

        pdh_txt_color = show_price_levels ? _get_value_text_color(str.tostring(pdh, "#.##"), p) : color.white
        pdh_bg_color = show_price_levels ? _get_value_bg_color(str.tostring(pdh, "#.##"), p) : color.new(#2D3748, 0)
        pdl_txt_color = show_price_levels ? _get_value_text_color(str.tostring(pdl, "#.##"), p) : color.white
        pdl_bg_color = show_price_levels ? _get_value_bg_color(str.tostring(pdl, "#.##"), p) : color.new(#2D3748, 0)

        // Performance column colors - simplified to only Chg %
        perf_txt_color = show_basic ? color.white : color.white
        perf_bg_color = show_basic ? (chg > 0 ? color.new(#1B4332, 0) : chg < 0 ? color.new(#7D1007, 0) : color.new(#2D3748, 0)) : color.new(#2D3748, 0)

        string valFormatted = show_basic ? str.tostring(chg, format.percent) : ""

        // Dynamic column placement
        current_col = col_offset

        // Basic Info columns
        if show_basic
            table.cell(tab, current_col, base_row, (mode == 'Name' and name == '') or mode == 'Tooltip' ? _name(tkr) : name, text_color=txtcol, text_size=tab_size, bgcolor=bgcol, text_font_family=font, tooltip=(mode == 'Tooltip' and name == '') or mode == 'Name' ? na : name)
            current_col += 1

        // Price Level columns (moved after Name, before Price)
        if show_price_levels
            table.cell(tab, current_col, base_row, na(pdl) ? "" : str.tostring(pdl, "#.##"), text_color=pdl_txt_color, text_size=tab_size, bgcolor=pdl_bg_color, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, na(pdh) ? "" : str.tostring(pdh, "#.##"), text_color=pdh_txt_color, text_size=tab_size, bgcolor=pdh_bg_color, text_font_family=font)
            current_col += 1

        // Pre-market column (separate control)
        if show_premp
            premarket_str = na(premarket) ? "" : str.tostring(premarket, format.percent)
            premarket_color = na(premarket) ? color.black : (premarket > 0 ? color.green : premarket < 0 ? color.red : color.black)
            table.cell(tab, current_col, base_row, premarket_str, text_color=premarket_color, text_size=tab_size, bgcolor=color.yellow, text_font_family=font)
            current_col += 1

        if show_basic
            table.cell(tab, current_col, base_row, na(p) ? "" : str.tostring(p, '#.##'), text_color=txtcol, text_size=tab_size, bgcolor=bgcol, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, chg_open_str, text_color=chg_open > 0 ? color.green : chg_open < 0 ? color.red : color.white, text_size=tab_size, bgcolor=bgcol, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, valFormatted, text_color=perf_txt_color, text_size=tab_size, bgcolor=perf_bg_color, text_font_family=font)
            current_col += 1

        // Post-market column (separate control)
        if show_postmp
            postmarket_str = na(postmarket) ? "" : str.tostring(postmarket, format.percent)
            postmarket_color = na(postmarket) ? color.black : (postmarket > 0 ? color.green : postmarket < 0 ? color.red : color.black)
            table.cell(tab, current_col, base_row, postmarket_str, text_color=postmarket_color, text_size=tab_size, bgcolor=color.yellow, text_font_family=font)
            current_col += 1


        // Trading columns
        if show_trading
            table.cell(tab, current_col, base_row, trigger_cell, text_color=trigger_txt_color, text_size=tab_size, bgcolor=trigger_bg_color, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, stop_cell, text_color=stop_txt_color, text_size=tab_size, bgcolor=stop_bg_color, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, rr_cell, text_color=rr_txt_color, text_size=tab_size, bgcolor=rr_bg_color, text_font_family=font)
            current_col += 1

        // Slingshot columns
        if show_slingshot
            table.cell(tab, current_col, base_row, sling ? "Yes" : "", text_color=color.white, text_size=tab_size, bgcolor=color.new(#B8660A, 50), text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, sling and not na(sling_price) ? str.tostring(sling_price, '#.##') : "", text_color=color.white, text_size=tab_size, bgcolor=color.new(#B8660A, 50), text_font_family=font)
            current_col += 1

        // Price & Volume Breakout columns
        if show_pv_breakout
            table.cell(tab, current_col, base_row, pv_signal, text_color=color.white, text_size=tab_size, bgcolor=pv_signal == "Long" ? color.new(color.green, 15) : pv_signal == "Short" ? color.new(color.red, 15) : color.new(color.teal, 15), text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, not na(pv_price) ? str.tostring(pv_price, '#.##') : "", text_color=color.white, text_size=tab_size, bgcolor=color.new(color.teal, 25), text_font_family=font)
            current_col += 1

        // Combo columns
        if show_combos
            table.cell(tab, current_col, base_row, kickerBool ? (kicker ? 'Kicker' : '') : '', bgcolor=kicker ? color.new(color.green, 10) : na, text_color=color.black, text_size=tab_size, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, oopsBool ? (oopsUp ? 'Oops+' : oopsDn ? 'Oops-' : '') : '', bgcolor=oopsUp ? color.new(color.green, 0) : oopsDn ? color.new(color.red, 0) : na, text_color=color.black, text_size=tab_size, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, oelBool ? (oel ? 'OEL' : oeh ? 'OEH' : '') : '', bgcolor=oel ? color.new(color.green, 10) : oeh ? color.new(color.red, 10) : na, text_color=color.black, text_size=tab_size, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, insideBool ? (inside ? 'Inside' : engulf ? 'Engulf' : '') : '', bgcolor=inside ? color.new(color.green, 12) : engulf ? color.new(color.red, 12) : na, text_color=color.black, text_size=tab_size, text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, threeBarBool ? (b3Up ? '3Bar+' : b3Dn ? '3Bar-' : '') : '', bgcolor=b3Up ? color.new(color.green, 0) : b3Dn ? color.new(color.red, 0) : na, text_color=color.black, text_size=tab_size, text_font_family=font)
            current_col += 1

        // Metrics columns (EMA/SMA values)
        if show_metrics
            table.cell(tab, current_col, base_row, m1_s, text_color=color.white, text_size=tab_size, bgcolor=color.new(color.navy, 40), text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, m2_s, text_color=color.white, text_size=tab_size, bgcolor=color.new(color.navy, 40), text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, m3_s, text_color=color.white, text_size=tab_size, bgcolor=color.new(color.navy, 40), text_font_family=font)
            current_col += 1

        // Distance columns (separated from metrics)
        if show_distances
            table.cell(tab, current_col, base_row, d1_s, text_color=color.white, text_size=tab_size, bgcolor=color.new(color.blue, 20), text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, d2_s, text_color=color.white, text_size=tab_size, bgcolor=color.new(color.blue, 20), text_font_family=font)
            current_col += 1
            table.cell(tab, current_col, base_row, d3_s, text_color=color.white, text_size=tab_size, bgcolor=color.new(color.blue, 20), text_font_family=font)
            current_col += 1

        // Industry column
        if show_notes
            table.cell(tab, current_col, base_row, notes_cell, text_color=color.white, text_size=tab_size, bgcolor=color.new(color.purple, 20), text_font_family=font)
            current_col += 1

        base_row + 1
    else
        base_row

// Fill vertical offset rows (if any)
if row_offset > 0
    for i = 0 to row_offset - 1
        for j = 0 to total_cols - 1
            table.cell(tab, j, i, "", text_color=color.new(color.white, 100))

// ---- FILL TABLE FOR 20 SYMBOLS ----
int row = header_row + 1

"""


def get_template_footer() -> str:
    """Return the footer part of the template (after table rows)."""
    return """
// --- END OF SCRIPT ---"""


def generate_dashboard(csv_file: str = 'watchlist.csv', output_file: str = 'dashboard.pine'):
    """Main function to generate dashboard.pine from watchlist CSV."""
    try:
        print(f"Reading watchlist CSV: {csv_file}")
        df = read_watchlist_csv(csv_file)

        if df.empty:
            print("Error: No valid symbols found in CSV file.")
            return False

        print(f"Found {len(df)} symbols in watchlist")

        # Generate dynamic sections
        print("Generating symbol inputs...")
        symbol_inputs = generate_symbol_inputs(df, max_symbols=20)

        print("Generating table rows...")
        table_rows = generate_table_rows(max_symbols=20)

        # Assemble complete Pine Script
        print("Assembling Pine Script...")
        pinescript_content = get_template_header()
        pinescript_content += symbol_inputs
        pinescript_content += get_template_middle()
        pinescript_content += table_rows
        pinescript_content += get_template_footer()

        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pinescript_content)

        print(f"\n✅ Dashboard generated successfully: {output_file}")

        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Symbols processed: {len(df)}")
        print(f"Output file: {output_file}")
        print("\nFirst 5 symbols:")
        for i, row in df.head(5).iterrows():
            print(f"  {i+1}. {row['Ticker']}: Trigger={row['Trigger']}, Stop={row['Stop']}")
        print("="*60)

        return True

    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys

    # Allow command-line arguments for input and output files
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'watchlist.csv'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'dashboard.pine'

    print("="*60)
    print("TradingView Dashboard Generator")
    print("="*60)
    print(f"Input CSV: {csv_file}")
    print(f"Output file: {output_file}")
    print("="*60 + "\n")

    success = generate_dashboard(csv_file, output_file)

    if success:
        print("\n🎉 Generation complete! You can now load dashboard.pine into TradingView.")
    else:
        print("\n❌ Generation failed. Please check the errors above.")
        sys.exit(1)
