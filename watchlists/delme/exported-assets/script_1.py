import pandas as pd
import io

data = """
Symbol,Description
ITA,Aerospace Defense
AAA,Aluminum
AIRR,Industrial Machinery
AIRR,Industrial Specialties
AIRR,Miscellaneous Manufacturing
AMLP,Oil Gas Pipelines
BJK,CasinosGaming
CARZ,Auto Parts OEM
CARZ,Automotive Aftermarket
CARZ,Motor Vehicles
CIBR,Cybersecurity
COAL,Coal
CRAK,Oil RefiningMarketing
CRAK,Oil Refiners
DBA,Agricultural CommoditiesMilling
EATZ,Restaurants
EMET,Cooper and Green Metals
FDN,Internet SoftwareServices
FIW,Water Utilities
FSTA,Tobacco
GDXJ,Junior Goldmines
GLD,Precious Metals
HACK,Computer Communications
HACK,Computer Peripherals
IAK,LifeHealth Insurance
IBB,Biotechnology
IBB,Pharmaceuticals Other
IBOT,Robotics ETF
IBRN,Neuroscience Heathcare Demographic
IBUY,Internet Retail
IGM,Electronic EquipmentInstruments
IGM,Electronic Production Equipment
IGV,Packaged Software
IHF,Financial PublishingServices
IHF,HospitalNursing Management
IHF,Managed Health Care
IHF,Medical Distributors
IHF,MedicalNursing Services
IHF,Services to the Health Industry
IHI,Medical Devices
ITA,General Government
ITB,Home Furnishings
ITB,Homebuilding
IYF,Investment Managers
IYT,Railroads
IYZ,Specialty Telecommunications
IYZ,Telecommunications Equipment
IYZ,Wireless Telecommunications
JEDIS,Space Innovators
JETS,Airlines
KBE,Savings Banks
KBWB,Major Banks
KIE,Insurance BrokersServices
KIE,Multi-Line Insurance
KIE,PropertyCasualty Insurance
KIE,Specialty Insurance
KRE,Regional Banks
MOO,Chemicals Agricultural
NLR,Uranium and Nuclear Energy
NUKZ,Range Nuclear Renaissance ETF
OIH,Contract Drilling
OIH,Oilfield ServicesEquipment
PAVE,Electrical Components
PBJ,Beverages Alcoholic
PBJ,Beverages Non-Alcoholic
PBJ,Food Distributors
PBJ,Food Retail
PBJ,Food Major Diversified
PBJ,Food MeatFishDairy
PBJ,Food SpecialtyCandy
PBS,AdvertisingMarketing Services
PBS,Broadcasting
PBS,CableSatellite TV
PBW,Clean Energy
PEJ,HotelsResortsCruise lines
PEJ,MoviesEntertainment
PEJ,Recreational Products
PHO,Environmental Services
PICK,Other MetalsMinerals
PJP,Pharmaceuticals Generic
PKB,Construction Materials
PKB,Engineering Construction
PKB,Tools Hardware
PPH,Pharmaceuticals Major
PSCI,Commercial PrintingForms
PSCI,ElectronicsAppliances
PSCI,Miscellaneous Commercial Services
QTUM,Quantum
REMX,Rare Earth and Strategic Metals
RTH,Discount Stores
RTH,Personnel Services
SEA,Marine Shipping
SLV,Silver Miners
SLX,Metal Fabrication Steel
SLX,Steel
SMH,Semis
SMHX,Fabless Semis
SOXX,Semiconductors
SPY,Investment TrustsMutual Funds
TAN,Alternative Power Generation Solar
TAN,Solar
UGA,Gas Distributors
URA,Uranium
VEGI,Agriculture
VGT,Data Processing Services
VGT,Information Technology Services
VNQ,Real Estate Development
VNQ,Real Estate Investment Trusts
VOX,Major Telecommunications
WOOD,Building Products
WOOD,Forest Products
WOOD,Pulp Paper
XHB,Home Improvement Chains
XLB,Chemicals Major Diversified
XLB,Chemicals Specialty
XLB,ContainersPackaging
XLF,FinanceRentalLeasing
XLF,Financial Conglomerates
XLF,Investment BanksBrokers
XLI,Electrical Products
XLI,Industrial Conglomerates
XLI,TrucksConstructionFarm Machinery
XLP,HouseholdPersonal Care
XLU,Electric Utilities
XLV,Healthcare
XLV,Medical Specialties
XLY,Miscellaneous
XLY,Other Consumer Services
XLY,Other Consumer Specialties
XLY,Wholesale Distributors
XOP,Integrated Oil
XOP,Oil Gas Production
XRT,ApparelFootwear
XRT,ApparelFootwear Retail
XRT,CatalogSpecialty Distribution
XRT,Consumer Sundries
XRT,Department Stores
XRT,Drugstore Chains
XRT,ElectronicsAppliance Stores
XRT,Specialty Stores
XRT,Textiles
XRX,Office EquipmentSupplies
XSD,Computer Processing Hardware
XSD,Electronic Components
XSD,Electronics Distributors
XTN,Air FreightCouriers
XTN,Other Transportation
XTN,Trucking
"""

df = pd.read_csv(io.StringIO(data), header=0)

print("Data shape:", df.shape)
print(df.head(10))

def get_group(desc):
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

df['Group'] = df['Description'].apply(get_group)

group_counts = df.groupby('Group').agg({
    'Symbol': 'nunique',
    'Description': 'count'
}).rename(columns={'Description': 'Total Associations'}).sort_values('Symbol', ascending=False)

print("\nUnique symbols per group:")
print(group_counts.to_csv())

print("\nSample symbols per group:")
for group in group_counts.index:
    symbols = df[df['Group'] == group]['Symbol'].unique()[:5]
    print(f"{group}: {list(symbols)}")