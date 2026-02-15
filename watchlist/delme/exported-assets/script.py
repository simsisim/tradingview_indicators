import pandas as pd
import io
import ast

# The data is in snippet format, but to get full content, since it's CSV, I'll read it directly
data = """
Symbol,Description
ITAAerospace Defense
AAAluminum
AIRRIndustrial Machinery
AIRRIndustrial Specialties
AIRRMiscellaneous Manufacturing
AMLPOil Gas Pipelines
BJKCasinosGaming
CARZAuto Parts OEM
CARZAutomotive Aftermarket
CARZMotor Vehicles
CIBRCybersecurity
COALCoal
CRAKOil RefiningMarketing
CRAKOil Refiners
DBAAgricultural CommoditiesMilling
EATZRestaurants
EMETCooper and Green Metals
FDNInternet SoftwareServices
FIWWater Utilities
FSTATobacco
GDXJJunior Goldmines
GLDPrecious Metals
HACKComputer Communications
HACKComputer Peripherals
IAKLifeHealth Insurance
IBBBiotechnology
IBBPharmaceuticals Other
IBOTRobotics ETF
IBRNNeuroscience Heathcare Demographic
IBUYInternet Retail
IGMElectronic EquipmentInstruments
IGMElectronic Production Equipment
IGVPackaged Software
IHFFinancial PublishingServices
IHFHospitalNursing Management
IHFManaged Health Care
IHFMedical Distributors
IHFMedicalNursing Services
IHFServices to the Health Industry
IHIMedical Devices
ITAGeneral Government
ITBHome Furnishings
ITBHomebuilding
IYFInvestment Managers
IYTRailroads
IYZSpecialty Telecommunications
IYZTelecommunications Equipment
IYZWireless Telecommunications
JEDISpace Innovators
JETSAirlines
KBESavings Banks
KBWBMajor Banks
KIEInsurance BrokersServices
KIEMulti-Line Insurance
KIEPropertyCasualty Insurance
KIESpecialty Insurance
KRERegional Banks
MOOChemicals Agricultural
NLRUranium and Nuclear Energy
NUKZRANGE Nuclear Renaissance ETF
OIHContract Drilling
OIHOilfield ServicesEquipment
PAVEElectrical Components
PBJBeverages Alcoholic
PBJBeverages Non-Alcoholic
PBJFood Distributors
PBJFood Retail
PBJFood Major Diversified
PBJFood MeatFishDairy
PBJFood SpecialtyCandy
PBSAdvertisingMarketing Services
PBSBroadcasting
PBSCableSatellite TV
PBSClean Energy
PEJHotelsResortsCruise lines
PEJMoviesEntertainment
PEJRecreational Products
PHOEnvironmental Services
PICKOther MetalsMinerals
PJPPharmaceuticals Generic
PKBConstruction Materials
PKBEngineering Construction
PKBTools Hardware
PPHPharmaceuticals Major
PSCICommercial PrintingForms
PSCIElectronicsAppliances
PSCIMiscellaneous Commercial Services
QTUMQuantum
REMXRare Earth and Strategic Metals
RTHDiscount Stores
RTHPersonnel Services
SEAMarine Shipping
SLVSilver Miners
SLXMetal Fabrication Steel
SLXSteel
SMHSemis
SMHXFabless Semis
SOXXSemiconductors
SPYInvestment TrustsMutual Funds
TANAlternative Power Generation Solar
TANSolar
UGAGas Distributors
URAUranium
VEGIAgriculture
VGTData Processing Services
VGTInformation Technology Services
VNQReal Estate Development
VNQReal Estate Investment Trusts
VOXMajor Telecommunications
WOODBuilding Products
WOODForest Products
WOODPulp Paper
XHBHome Improvement Chains
XLBChemicals Major Diversified
XLBChemicals Specialty
XLBContainersPackaging
XLFFinanceRentalLeasing
XLFFinancial Conglomerates
XLFInvestment BanksBrokers
XLIElectrical Products
XLIIndustrial Conglomerates
XLITrucksConstructionFarm Machinery
XLPHouseholdPersonal Care
XLUElectric Utilities
XLVHealthcare
XLVMedical Specialties
XLYMiscellaneous
XLYOther Consumer Services
XLYOther Consumer Specialties
XLYWholesale Distributors
XOPIntegrated Oil
XOPOil Gas Production
XRTApparelFootwear
XRTApparelFootwear Retail
XRTCatalogSpecialty Distribution
XRTConsumer Sundries
XRTDepartment Stores
XRTDrugstore Chains
XRTElectronicsAppliance Stores
XRTSpecialty Stores
XRTTextiles
XRXOffice EquipmentSupplies
XSDComputer Processing Hardware
XSDElectronic Components
XSDElectronics Distributors
XTNAir FreightCouriers
XTNOther Transportation
XTNTrucking
"""

# Load the data
df = pd.read_csv(io.StringIO(data))

print("Full data shape:", df.shape)
print(df.head())

# Clean descriptions: split concatenated words if possible, but for clustering, use as is or simple grouping
# For visual clustering, group by main industry themes

# Simple grouping based on keywords in description
def get_group(desc):
    desc_lower = desc.lower()
    if any(word in desc_lower for word in ['oil', 'gas', 'energy', 'uranium', 'nuclear', 'coal']):
        return 'Energy'
    elif any(word in desc_lower for word in ['health', 'medical', 'pharma', 'biotech', 'hospital']):
        return 'Healthcare'
    elif any(word in desc_lower for word in ['tech', 'software', 'internet', 'computer', 'semi', 'electronic']):
        return 'Technology'
    elif any(word in desc_lower for word in ['finance', 'bank', 'insurance', 'investment']):
        return 'Financials'
    elif any(word in desc_lower for word in ['industrial', 'machinery', 'construction', 'transport']):
        return 'Industrials'
    elif any(word in desc_lower for word in ['consumer', 'food', 'retail', 'apparel']):
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

# Count symbols per group
group_counts = df.groupby('Group')['Symbol'].count().sort_values(ascending=False)

print("\nGroup counts:")
print(group_counts.to_csv())

# List symbols per group
groups = df.groupby('Group')['Symbol'].apply(list).to_dict()
print("\nGroups:")
print(str(groups))

# Save grouped data for chart
grouped_df = df.groupby('Group').agg({
    'Symbol': lambda x: ', '.join(x.unique()),  # unique symbols
    'Description': 'count'  # count
}).rename(columns={'Description': 'Count'}).reset_index()

print("\nGrouped data:")
print(grouped_df.to_csv(index=False))