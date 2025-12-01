# Stock vs Industry Indicator - Improvement Ideas

**Original idea from** [url=https://de.tradingview.com/script/EO9DkXLk-Stock-versus-Industry/]Stock versus Industry[/url] **by** [url=https://de.tradingview.com/u/Tr33man/]Tr33man[/url].

---

## 📂 Code Availability

Since this improvement may not be accepted as an update to the original TradingView script, the **complete Pine Script code and supporting data pipeline** are available on GitHub:

**GitHub Repository:** https://github.com/simsisim/tradingview_indicators

The repository includes:
- ✅ Complete improved Pine Script indicator code
- ✅ CSV data file with 361 NQUSB industry hierarchies
- ✅ Industry-to-NQUSB mapping documentation
- ✅ Setup and usage instructions

---

## 🎯 Primary Innovations

### **Innovation 1: Dual Display Mode (v9) - Stock vs Industry AND Industry vs SPY**

Version 9 introduces a **game-changing display mode selector** that transforms one indicator into TWO complementary analysis tools:

#### **Two Display Modes:**
1. **"Stock vs Industry"** - Shows how the stock performs against its industry (original functionality)
2. **"Industry vs SPY"** - Shows how the industry performs against the broader market (NEW!)

#### **Why This Matters:**
You can now add the **same indicator twice** to your chart in separate panels to simultaneously view:
- **Panel 1**: Stock vs Industry strength (e.g., MSFT vs NASDAQ Software)
- **Panel 2**: Industry vs Market strength (e.g., NASDAQ Software vs SPY)

#### **Example: Analyzing MSFT**
- **Instance 1 (Stock vs Industry mode)**:
  - Comparison: `MSFT / NQUSB10101015` (Microsoft vs NASDAQ Software Index)
  - Insight: Is MSFT outperforming its software peers?

- **Instance 2 (Industry vs SPY mode)**:
  - Comparison: `NQUSB10101015 / SPY` (Software Index vs S&P 500)
  - Insight: Is the entire software sector outperforming the market?

#### **The Power of Dual Display:**
By viewing both modes simultaneously, you can answer critical questions:
- ✅ **Is my stock strong because it's beating peers, or because the entire industry is hot?**
- ✅ **Is my stock weak because it's underperforming peers, or because the industry is in decline?**
- ✅ **Should I hold the stock or rotate to a sector ETF?**
- ✅ **Is this a stock-specific opportunity or a sector rotation signal?**

#### **Trading Scenarios:**

| **Stock vs Industry** | **Industry vs SPY** | **Interpretation** | **Action** |
|----------------------|---------------------|-------------------|-----------|
| ⬆️ Outperforming | ⬆️ Outperforming | Stock AND sector both strong | ✅ Strong buy signal |
| ⬆️ Outperforming | ⬇️ Underperforming | Stock strong, sector weak | ⚠️ Stock-specific strength - monitor closely |
| ⬇️ Underperforming | ⬆️ Outperforming | Stock weak, sector strong | 🔄 Consider sector ETF instead |
| ⬇️ Underperforming | ⬇️ Underperforming | Stock AND sector both weak | ❌ Avoid or exit position |

**Default Settings (v9):**
- Display Mode: "Stock vs Industry"
- Compare Against: "Index Benchmark" (NQUSB indices)
- Index Selection: "Primary" (most specific level)

---

### **Innovation 2: NQUSB Hierarchical Index Benchmarks**

#### **Main Improvement: Multi-Level Industry Granularity**

The KEY improvement is replacing generic ETF comparisons with **NASDAQ's official NQUSB industry hierarchy**, enabling drill-down/drill-up analysis across **4 levels of industry classification**:

#### **From**: Simple ETF Comparison (1 Level)
```
Stock → Industry ETF (e.g., "SOXX" for all semiconductors)
```

#### **To**: NQUSB Hierarchical Comparison (4 Levels)
```
Level 4 (Primary):    NQUSB10102010 → Semiconductors (most specific)
Level 3 (Secondary):  NQUSB101020   → Technology Hardware and Equipment  
Level 2 (Tertiary):   NQUSB10       → Technology
Level 1 (Quaternary): NQUSB10       → Technology (broadest sector)
```

**Users can now drill up and down the industry hierarchy** to see how their stock performs against:
- Most specific peers (Level 4)
- Broader industry group (Level 3)
- Sector (Level 2)
- Economic super-sector (Level 1)

---

## Why This Matters

### **Original Limitations:**
- ❌ **Single comparison level** - ETF only
- ❌ **No drill-down capability** - Can't zoom in to more specific industries
- ❌ **No drill-up capability** - Can't zoom out to broader sectors
- ❌ **ETF limitations** - Not all industries have dedicated ETFs
- ❌ **Arbitrary mappings** - Manual ETF selection may not represent true industry

### **Improved Capabilities:**

#### **1. Hierarchical Navigation (Drill-Down & Drill-Up)**

**Example: Analyzing NVDA (Semiconductors)**

| **Level** | **Code** | **Industry Name** | **What You See** |
|-----------|----------|-------------------|------------------|
| **Primary (L4)** | `NQUSB10102010` | Semiconductors | NVDA vs. AMD, AVGO, QCOM, TXN, etc. (most specific) |
| **Secondary (L3)** | `NQUSB101020` | Tech Hardware & Equipment | NVDA vs. AAPL, CSCO + semiconductors (broader) |
| **Tertiary (L2)** | `NQUSB101010` | Software and Computer Services | NVDA vs. all tech hardware (even broader) |
| **Quaternary (L1)** | `NQUSB10` | Technology Sector | NVDA vs. entire technology sector (broadest) |

**Benefit:** **You can now zoom in to see direct competitors or zoom out to understand macro sector trends** - all in one indicator!

---

#### **2. Official NASDAQ Classification**
- ✅ Uses **NASDAQ US Benchmark (NQUSB) Index** structure
- ✅ **361 industry classifications** from official NASDAQ data
- ✅ Systematically maintained by NASDAQ
- ✅ Industry-standard taxonomy

**Comparison:**
| Feature | Original (ETF) | Improved (NQUSB) |
|---------|----------------|------------------|
| **Classification Source** | Manual ETF mapping | NASDAQ official taxonomy |
| **Total Industries** | ~140 ETF mappings | **361 NQUSB indices** |
| **Hierarchy Levels** | 1 (flat) | **4 (hierarchical)** |
| **Drill-Down** | ❌ No | ✅ **Yes - 4 levels** |
| **Drill-Up** | ❌ No | ✅ **Yes - 4 levels** |
| **Coverage** | Limited by ETF availability | **Comprehensive - all industries** |

---

#### **3. Large Mid Cap (LM) Variant Option**
- ✅ Toggle between standard and "LM" (Large Mid Cap) indices
- ✅ Focus on larger companies only when needed
- ✅ Reduces small-cap noise in comparisons

---

#### **4. Enhanced User Interface**

**Original version:**
- Basic table showing industry name
- Single comparison ticker

**Improved version:**
- **4-row information table:**
  1. Industry name (from TradingView)
  2. Stock vs Comparison ticker
  3. Full NQUSB index description (e.g., "Nasdaq US Semiconductors Large Mid Cap Index")
  4. Comparison type indicator `[ETF]`, `[Index-L1]`, `[Index-L2]`, `[Index-L3]`, `[Index-L4]`, or `[Custom]`

**Benefit:** Instantly know **which level of the hierarchy** you're viewing!

---

## Implementation Details

### **Data Pipeline Architecture**

The improved version uses **NASDAQ's official NQUSB classification data**:

```
NASDAQ NQUSB Data
    ↓
NQUSB_filtered_no_TR_grouping_v2.csv (361 indices with 4-level hierarchy)
    ↓
Pine Script Mapping (130 TradingView industries → NQUSB hierarchies)
    ↓
Dynamic Level Selection (Primary/Secondary/Tertiary/Quaternary)
```

###  **Key Data Sources:**

1. **`NQUSB_filtered_no_TR_grouping_v2.csv`** - 361 NQUSB industry indices with full 4-level hierarchy
   - Format: `Symbol,Name,Belonging_To_Sector,Key_Name,included_in_industries`
   - Example: `NQUSB10102010,Nasdaq US Semiconductors Index,NQUSB10,Semiconductors,"NQUSB10,NQUSB101020,NQUSB10102010"`

2. **Pine Script Hierarchy Mapping** - 130 explicit TradingView industry → NQUSB mappings
   - Format: `"Industry" => "Level1,Level2,Level3,Level4"` (comma-separated hierarchy)
   - Example: `"Semiconductors" => "NQUSB10,NQUSB101020,NQUSB10102010"`

### **Smart Index Selection Logic**

```pine
selectIndex(string indexString, string choice) =>
    // Parse comma-separated hierarchy
    hierarchyArray = str.split(indexString, ",")
    
    // Select level based on user choice
    levelPosition = switch choice
        "Primary" => arraySize - 1      // Most specific (L4)
        "Secondary" => arraySize - 2     // L3
        "Tertiary" => arraySize - 3      // L2  
        "Quaternary" => 0                // Broadest sector (L1)
```

**Benefit:** One indicator, **infinite perspectives** on industry performance!

---

## Real-World Use Cases

### **For Day Traders:**
- **Start with Primary (L4)** → See how NVDA compares to direct semiconductor competitors today
- **If sector is weak overall** → Drill up to **Tertiary (L2)** to see if all tech is down

### **For Swing Traders:**
- **Monitor at Secondary (L3)** → Track NVDA vs broader tech hardware group
- **Identify divergences** → If NVDA outperforms at L4 but underperforms at L2, it signals sector rotation

### **For Position Traders/Investors:**
- **Analyze all 4 levels** → Understand if stock strength is industry-specific or sector-wide
- **Sector rotation signals** → Outperformance at L1 (sector) but underperformance at L4 (industry) = consider sector ETFs

### **For Sector Rotation Strategies:**
- **Compare L1 (Quaternary)** across different stocks → Identify strongest/weakest sectors
- **Drill down to L4** → Find best stocks within winning sectors

---

## Comparison Summary Table

| **Feature** | **Original Version** | **Improved Version (v9)** |
|-------------|---------------------|---------------------|
| **Display Modes** | Stock vs Industry only | ✅ **Stock vs Industry + Industry vs SPY** |
| **Dual Panel Support** | ❌ No | ✅ **Add indicator twice for simultaneous views** |
| **Comparison System** | Industry ETFs | NQUSB Official Indices |
| **Industry Levels** | 1 (flat ETF mapping) | **4 (hierarchical drill-down/up)** |
| **Total Classifications** | ~140 industries | **361 NQUSB indices** |
| **Hierarchy Navigation** | ❌ No | ✅ **4-level drill navigation** |
| **Data Source** | Manual ETF curation | **NASDAQ official taxonomy** |
| **Large/Mid Cap Option** | ❌ No | ✅ **LM variant toggle** |
| **Index Description** | Generic ETF ticker | **Full NQUSB index name** |
| **Level Indicator** | ❌ No | ✅ **[Index-L1] to [Index-L4] labels** |
| **Fallback ETF** | Default ETF only | **ETF fallback + NQUSB priority** |
| **Industry Coverage** | Limited by ETF availability | **Comprehensive (all TradingView industries)** |
| **Default Comparison** | ETF | **Index Benchmark (Primary level)** |

---

## Technical Innovation: Hierarchical Index String Parsing

### **Data Structure Design**

Instead of storing 4 separate fields, the improved version uses **comma-separated hierarchy strings**:

```pine
// Efficient hierarchical storage
industryIndexBenchmark = switch (industry)
    "Semiconductors" => "NQUSB10,NQUSB101020,NQUSB10102010"
    "Biotechnology" => "NQUSB20,NQUSB201030,NQUSB20103010"
    // 130 total mappings...
```

### **Dynamic Level Selection**

The `selectIndex()` function intelligently selects the appropriate hierarchy level:

1. **Splits** comma-separated string into array
2. **Calculates** position based on user selection (Primary = last element, Quaternary = first)
3. **Fallback handling** - Uses `math.max(0, position)` to prevent errors on short hierarchies
4. **LM suffix** - Appends "LM" for Large Mid Cap variant if selected

**Benefit:** Single data structure supports **all 4 levels** + **LM variants** with minimal code!

---

## NQUSB Hierarchy Structure

The improved version maps **130 TradingView industries** to **NASDAQ's official 4-level taxonomy**:

### **Hierarchy Levels:**

**Level 1 (Quaternary) - Economic Sectors (10 total)**
- Technology (`NQUSB10`)
- Health Care (`NQUSB20`)
- Financials (`NQUSB30`)
- Consumer Discretionary (`NQUSB40`)
- Consumer Staples (`NQUSB45`)
- Industrials (`NQUSB50`)
- Basic Materials (`NQUSB55`)
- Energy (`NQUSB60`)
- Utilities (`NQUSB65`)
- Real Estate (`NQUSB35`)

**Level 2 (Tertiary) - Industry Groups (~25 total)**
- Example: `NQUSB101020` = Technology Hardware and Equipment

**Level 3 (Secondary) - Industries (~70 total)**
- Example: `NQUSB10102010` = Semiconductors

**Level 4 (Primary) - Sub-Industries (~256 total)**
- Example: `NQUSB10102010` = Semiconductors (most granular)

**Total: 361 unique NQUSB classifications!**

---

## Example Industry Mappings

### **Technology Sector Examples:**

| **TradingView Industry** | **NQUSB Hierarchy** | **Levels** |
|--------------------------|---------------------|------------|
| Semiconductors | `NQUSB10,NQUSB101020,NQUSB10102010` | 3 levels (L1→L2→L4) |
| Internet Software/Services | `NQUSB10,NQUSB101010,NQUSB10101020` | 3 levels |
| Data Processing Services | `NQUSB10,NQUSB101010,NQUSB10101010` | 3 levels |
| Computer Processing Hardware | `NQUSB10,NQUSB101020,NQUSB10102030` | 3 levels |

### **Finance Sector Examples:**

| **TradingView Industry** | **NQUSB Hierarchy** | **Levels** |
|--------------------------|---------------------|------------|
| Major Banks | `NQUSB30,NQUSB3010` | 2 levels (L1→L2) |
| Investment Banks/Brokers | `NQUSB30,NQUSB3020,NQUSB302020` | 3 levels |
| Property/Casualty Insurance | `NQUSB30,NQUSB3030,NQUSB303020,NQUSB30302025` | 4 levels (L1→L2→L3→L4) |
| Life/Health Insurance | `NQUSB30,NQUSB3030,NQUSB303010` | 3 levels |

### **Health Care Sector Examples:**

| **TradingView Industry** | **NQUSB Hierarchy** | **Levels** |
|--------------------------|---------------------|------------|
| Biotechnology | `NQUSB20,NQUSB201030,NQUSB20103010` | 3 levels |
| Pharmaceuticals: Major | `NQUSB20,NQUSB201030,NQUSB20103015` | 3 levels |
| Medical Specialties | `NQUSB20,NQUSB201020,NQUSB20102010` | 3 levels |
| Managed Health Care | `NQUSB20,NQUSB201010,NQUSB20101020` | 3 levels |

---

## Additional Improvements

### **1. Dual Comparison System**
- **ETF Mode** (original) - Still available as fallback
- **Index Benchmark Mode** (new) - NQUSB hierarchy with level selection
- User can toggle between both or use **manual override** for custom tickers

### **2. Better Fallback Logic**
```pine
// Priority: Manual Override > NQUSB Index > ETF > SPY default
if manual override enabled
    Use custom ticker
else if NQUSB mapping exists
    Parse hierarchy and select level
    Apply LM suffix if requested
else
    Fallback to industry ETF mapping
```

### **3. Enhanced Display Information**
- Shows **full NQUSB index description** (e.g., "Nasdaq US Semiconductors Large Mid Cap Index")
- Displays **comparison type** with level indicator: `[Index-L4]`, `[Index-L3]`, `[Index-L2]`, `[Index-L1]`
- 4-row information table for complete context

### **4. Maintained Backward Compatibility**
- ✅ All original ETF mappings **still work**
- ✅ Original visual style and coloring logic **preserved**
- ✅ Can still override with custom ticker
- ✅ Existing charts won't break

---

## Data Files Used

### **Primary Data Source:**
- **`NQUSB_filtered_no_TR_grouping_v2.csv`**
  - 361 rows (NQUSB indices)
  - Columns: `Symbol, Name, Belonging_To_Sector, Key_Name, included_in_industries`
  - Contains complete 4-level hierarchy mappings
  - Includes both standard and LM (Large Mid Cap) variants

### **Supporting Python Scripts:**
- `generate_v13_lookup_functions.py` - Generates Pine Script hierarchy lookup code
- `fix_sectorArr_hierarchy.py` - Validates parent-child relationships
- `analyze_children_approach.py` - Analyzes hierarchy drilling logic

---

## Conclusion

Version 9 delivers **TWO game-changing innovations**:

### **Key Advantages:**
1. ✅ **Dual Display Mode (v9)** - Stock vs Industry AND Industry vs SPY in one indicator
2. ✅ **Simultaneous dual-panel analysis** - Add indicator twice to see both comparisons at once
3. ✅ **4-level drill-down/drill-up navigation** - Zoom in to specific industries or zoom out to broad sectors
4. ✅ **361 official NQUSB classifications** - Comprehensive industry coverage
5. ✅ **NASDAQ-official taxonomy** - Industry-standard classification system
6. ✅ **Large Mid Cap variants** - Optional focus on larger companies
7. ✅ **Smart level selection** - Automatic hierarchy parsing with fallback logic
8. ✅ **Enhanced UI** - Clear level indicators and full index descriptions
9. ✅ **Default to Index Benchmark** - Primary level NQUSB comparison out of the box

### **The Result:**

**More accurate, more flexible, and more comprehensive industry strength analysis** - enabling traders to:
- Understand **exactly where their stock's performance comes from** by drilling through multiple levels of industry classification
- Separate **stock-specific strength from sector-wide trends** using dual display mode
- Make **better trading decisions** by viewing both Stock vs Industry AND Industry vs Market simultaneously

---

## BBCode Version for TradingView

```
[b]Original idea from[/b] [url=https://de.tradingview.com/script/EO9DkXLk-Stock-versus-Industry/]Stock versus Industry[/url] [b]by[/b] [url=https://de.tradingview.com/u/Tr33man/]Tr33man[/url].

[b]GitHub Repository:[/b] [url=https://github.com/simsisim/tradingview_indicators]https://github.com/simsisim/tradingview_indicators[/url]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[b][size=large]VERSION 9: TWO GAME-CHANGING INNOVATIONS[/size][/b]

[b]═══ INNOVATION 1: DUAL DISPLAY MODE ═══[/b]

[b]One indicator, TWO complementary analysis views:[/b]

[list]
[*] [b]Display Mode 1:[/b] Stock vs Industry (e.g., MSFT vs NASDAQ Software)
[*] [b]Display Mode 2:[/b] Industry vs SPY (e.g., NASDAQ Software vs SPY)
[/list]

[b]Add the indicator TWICE to your chart for simultaneous dual-panel analysis![/b]

[b]Trading Decision Matrix:[/b]
[list]
[*] [b]Stock ⬆️ + Industry ⬆️:[/b] Strong buy signal (both stock AND sector strong)
[*] [b]Stock ⬆️ + Industry ⬇️:[/b] Stock-specific strength (monitor closely)
[*] [b]Stock ⬇️ + Industry ⬆️:[/b] Consider sector ETF instead
[*] [b]Stock ⬇️ + Industry ⬇️:[/b] Avoid or exit (both weak)
[/list]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[b]═══ INNOVATION 2: NQUSB Hierarchical Index Benchmarks ═══[/b]

[b]Multi-Level Industry Granularity:[/b]

[list]
[*] [b]4 hierarchy levels:[/b] Primary (L4) → Secondary (L3) → Tertiary (L2) → Quaternary (L1)
[*] [b]361 NQUSB classifications:[/b] NASDAQ official industry taxonomy
[*] [b]Drill-down/drill-up navigation:[/b] Zoom in to specific industries or out to broad sectors
[*] [b]Large Mid Cap variant:[/b] Optional LM suffix for larger companies only
[*] [b]Default settings:[/b] Index Benchmark (Primary level) - most specific comparison out of the box
[/list]

[b]Example: Analyzing NVDA (Semiconductors)[/b]
[list]
[*] [b]Primary (L4):[/b] NQUSB10102010 → Semiconductors (most specific peers)
[*] [b]Secondary (L3):[/b] NQUSB101020 → Tech Hardware & Equipment (broader group)
[*] [b]Tertiary (L2):[/b] NQUSB101010 → Software and Computer Services (even broader)
[*] [b]Quaternary (L1):[/b] NQUSB10 → Technology Sector (broadest view)
[/list]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[b]Why This Matters:[/b]

[list]
[*] [b]Original:[/b] Single ETF comparison, single view mode
[*] [b]Version 9:[/b] Dual display modes + 4-level hierarchical navigation across 361 industry classifications
[*] [b]Use Cases:[/b] Separate stock-specific strength from sector-wide trends
[*] [b]Official Data:[/b] NASDAQ US Benchmark Index taxonomy (industry standard)
[/list]

[b]For complete documentation, data files, and technical details, visit the GitHub repository.[/b]
```
