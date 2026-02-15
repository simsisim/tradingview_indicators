import pandas as pd
import io

# Full CSV data from file:3
csv_data = """Symbol;Description
ITA;Aerospace & Defense
AA;Aluminum
AIRR;Industrial Machinery
AIRR;Industrial Specialties
AIRR;Miscellaneous Manufacturing
AMLP;Oil & Gas Pipelines
BJK;Casinos/Gaming
CARZ;Auto Parts: OEM
CARZ;Automotive Aftermarket
CARZ;Motor Vehicles
CIBR;Cybersecurity
COAL;Coal
CRAK;Oil Refining/Marketing
CRAK;Oil Refiners
DBA;Agricultural Commodities/Milling
EATZ;Restaurants
EMET;Cooper and Green Metals
FDN;Internet Software/Services
FIW;Water Utilities
FSTA;Tobacco
GDXJ;Junior Goldmines
GLD;Precious Metals
HACK;Computer Communications
HACK;Computer Peripherals
IAK;Life/Health Insurance
IBB;Biotechnology
IBB;Pharmaceuticals: Other
IBOT;Robotics ETF
IBRN;Neuroscience Heathcare Demographic
IBUY;Internet Retail
IGM;Electronic Equipment/Instruments
IGM;Electronic Production Equipment
IGV;Packaged Software
IHF;Financial Publishing/Services
IHF;Hospital/Nursing Management
IHF;Managed Health Care
IHF;Medical Distributors
IHF;Medical/Nursing Services
IHF;Services to the Health Industry
IHI;Medical Devices
ITA;General Government
ITB;Home Furnishings
ITB;Homebuilding
IYF;Investment Managers
IYT;Railroads
IYZ;Specialty Telecommunications
IYZ;Telecommunications Equipment
IYZ;Wireless Telecommunications
JEDI;Space Innovators
JETS;Airlines
KBE;Savings Banks
KBWB;Major Banks
KIE;Insurance Brokers/Services
KIE;Multi-Line Insurance
KIE;Property/Casualty Insurance
KIE;Specialty Insurance
KRE;Regional Banks
MOO;Chemicals: Agricultural
NLR;Uranium and Nuclear Energy
NUKZ;Range Nuclear Renaissance ETF
OIH;Contract Drilling
OIH;Oilfield Services/Equipment
PAVE;Electrical Components
PBJ;Beverages: Alcoholic
PBJ;Beverages: Non-Alcoholic
PBJ;Food Distributors
PBJ;Food Retail
PBJ;Food: Major Diversified
PBJ;Food: Meat/Fish/Dairy
PBJ;Food: Specialty/Candy
PBS;Advertising/Marketing Services
PBS;Broadcasting
PBS;Cable/Satellite TV
PBS;Media Conglomerates
PBS;Publishing: Books/Magazines
PBS;Publishing: Newspapers
PBW;Clean Energy
PEJ;Hotels/Resorts/Cruise lines
PEJ;Movies/Entertainment
PEJ;Recreational Products
PHO;Environmental Services
PICK;Other Metals/Minerals
PJP;Pharmaceuticals: Generic
PKB;Construction Materials
PKB;Engineering & Construction
PKB;Tools & Hardware
PPH;Pharmaceuticals: Major
PSCI;Commercial Printing/Forms
PSCI;Electronics/Appliances
PSCI;Miscellaneous Commercial Services
QTUM;Quantum
REMX;Rare Earth and Strategic Metals
RTH;Discount Stores
RTH;Personnel Services
SEA;Marine Shipping
SLV;Silver Miners
SLX;Metal Fabrication/ Steel
SLX;Steel
SMH;Semis
SMHX;Fabless Semis
SOXX;Semiconductors
SPY;Investment Trusts/Mutual Funds
TAN;Alternative Power Generation/ Solar
TAN;Solar
UGA;Gas Distributors
URA;Uranium
VEGI;Agriculture
VGT;Data Processing Services
VGT;Information Technology Services
VNQ;Real Estate Development
VNQ;Real Estate Investment Trusts
VOX;Major Telecommunications
WOOD;Building Products
WOOD;Forest Products
WOOD;Pulp & Paper
XHB;Home Improvement Chains
XLB;Chemicals: Major Diversified
XLB;Chemicals: Specialty
XLB;Containers/Packaging
XLF;Finance/Rental/Leasing
XLF;Financial Conglomerates
XLF;Investment Banks/Brokers
XLI;Electrical Products
XLI;Industrial Conglomerates
XLI;Trucks/Construction/Farm Machinery
XLP;Household/Personal Care
XLU;Electric Utilities
XLV;Healthcare
XLV;Medical Specialties
XLY;Miscellaneous
XLY;Other Consumer Services
XLY;Other Consumer Specialties
XLY;Wholesale Distributors
XOP;Integrated Oil
XOP;Oil & Gas Production
XRT;Apparel/Footwear
XRT;Apparel/Footwear Retail
XRT;Catalog/Specialty Distribution
XRT;Consumer Sundries
XRT;Department Stores
XRT;Drugstore Chains
XRT;Electronics/Appliance Stores
XRT;Specialty Stores
XRT;Textiles
XRX;Office Equipment/Supplies
XSD;Computer Processing Hardware
XSD;Electronic Components
XSD;Electronics Distributors
XTN;Air Freight/Couriers
XTN;Other Transportation
XTN;Trucking"""

df = pd.read_csv(io.StringIO(csv_data), sep=';')

def get_cluster(desc: str) -> str:
    if pd.isna(desc):
        return 'Other'
    desc_lower = str(desc).lower()
    if any(word in desc_lower for word in ['oil', 'gas', 'energy', 'uranium', 'nuclear', 'coal']):
        return 'Energy'
    elif any(word in desc_lower for word in ['health', 'medical', 'pharma', 'bio', 'hospital']):
        return 'Healthcare'
    elif any(word in desc_lower for word in ['tech', 'software', 'internet', 'computer', 'semi', 'electronic', 'cyber']):
        return 'Technology'
    elif any(word in desc_lower for word in ['finance', 'bank', 'insurance', 'investment']):
        return 'Financials'
    elif any(word in desc_lower for word in ['industrial', 'machinery', 'construction', 'transport', 'rail', 'air']):
        return 'Industrials'
    elif any(word in desc_lower for word in ['food', 'retail', 'apparel', 'consumer']):
        return 'Consumer'
    elif any(word in desc_lower for word in ['metal', 'mining', 'gold', 'silver']):
        return 'Materials'
    elif 'real estate' in desc_lower:
        return 'Real Estate'
    elif any(word in desc_lower for word in ['utility', 'water']):
        return 'Utilities'
    else:
        return 'Other'

df['Cluster'] = df['Description'].apply(get_cluster)

# Unique per symbol, first cluster
df_final = df.drop_duplicates('Symbol').sort_values('Symbol')[['Symbol', 'Description', 'Cluster']]

# Output complete CSV
print(df_final.to_csv(index=False))