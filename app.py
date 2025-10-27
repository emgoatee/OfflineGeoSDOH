import os
import glob
import pandas as pd
import geopandas as gpd
from flask import Flask, render_template, request
from shapely.geometry import Point
import re
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ----------- File paths
CSV_PATH = resource_path("data/geodata.csv")
SVI_PATH = resource_path("data/SVI_2022_US.csv")
ADI_PATH = resource_path("data/adi.csv")
ACS_PATH = resource_path("data/ACS_deprivation_index.csv")
BROKAMP_PATH = resource_path("data/ACS_deprivation_index_by_zipcode.csv")
COI_PATH = resource_path("data/COI_subdomin_data.xlsx")

# ----------- State setup
STATE_FIPS = {
    '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA', '08': 'CO', '09': 'CT',
    '10': 'DE', '11': 'DC', '12': 'FL', '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL',
    '18': 'IN', '19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME', '24': 'MD',
    '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS', '29': 'MO', '30': 'MT', '31': 'NE',
    '32': 'NV', '33': 'NH', '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND',
    '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI', '45': 'SC', '46': 'SD',
    '47': 'TN', '48': 'TX', '49': 'UT', '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV',
    '55': 'WI', '56': 'WY', '60': 'AS', '66': 'GU', '69': 'MP', '72': 'PR', '78': 'VI'
}
STATE_ABBR_TO_FIPS = {v: k for k, v in STATE_FIPS.items()}
STATE_NAMES = [(v, n) for k, v in STATE_FIPS.items() for n in [v]]

# ----------- Utility Functions
def clean_street_name(name):
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    for long, short in [
        ('street', 'st'), ('avenue', 'ave'), ('road', 'rd'), ('boulevard', 'blvd'),
        ('drive', 'dr'), ('lane', 'ln'), ('place', 'pl'), ('terrace', 'ter'),
        ('court', 'ct'), ('north', 'n'), ('south', 's'), ('east', 'e'), ('west', 'w')
    ]:
        name = re.sub(r'\b'+long+r'\b', short, name)
    return name.strip()

def parse_street(address):
    parts = address.strip().split(" ", 1)
    if len(parts) < 2: return None, None
    try: number = int(parts[0])
    except Exception: return None, None
    name = clean_street_name(parts[1])
    return number, name

def get_addr_range_cols(addr_gdf):
    # Support both major TIGER variants
    if 'LFROMADD' in addr_gdf.columns: return 'LFROMADD','LTOADD','RFROMADD','RTOADD'
    elif 'LFROMHN' in addr_gdf.columns: return 'LFROMHN','LTOHN','RFROMHN','RTOHN'
    else: raise Exception("No expected address range columns in addrfeat file")

# ----------- Data Loading
def fips_column(df, colname='FIPS'):
    if 'TRACT' in df.columns and colname not in df.columns:
        df.rename(columns={'TRACT': colname}, inplace=True)
    df[colname] = df[colname].astype(str).str.zfill(11)
    return df

sdi_df = fips_column(pd.read_csv(CSV_PATH, dtype=str))
svi_df = fips_column(pd.read_csv(SVI_PATH, dtype=str))
adi_df = fips_column(pd.read_csv(ADI_PATH, dtype=str))
acs_df = fips_column(pd.read_csv(ACS_PATH, dtype=str))

# Load Brokamp by ZIP
brokamp_df = pd.read_csv(BROKAMP_PATH, dtype=str)
brokamp_df['Zip code'] = brokamp_df['Zip code'].astype(str).str.zfill(5)

# Load COI Excel, GEOID as string and zero-padded
coi_df = pd.read_excel(COI_PATH, dtype=str)
coi_df['GEOID'] = coi_df['GEOID'].astype(str).str.zfill(11)

# ----------- Tract files (state-level)
app = Flask(__name__)
print("Loading all state and territory tract shapefiles. This may take a while...")
gdfs_tracts = {}
for fips, abbr in STATE_FIPS.items():
    shape_base = f"tl_2022_{fips}_tract"
    shp_path = resource_path(f"data/{shape_base}.shp")
    if os.path.exists(shp_path):
        print(f"  Loading tracts for {abbr}...")
        gdf = gpd.read_file(shp_path)
        gdf['GEOID'] = gdf['GEOID'].astype(str)
        gdfs_tracts[abbr] = gdf
    else:
        print(f"  {abbr} tract shapefile not found, skipping.")
print(f"Loaded {len(gdfs_tracts)} states/territories.")

# ----------- Offline Address Geocoder (county-based addrfeat search)
def offline_geocode(street, zip_code, state_abbr):
    state_fips = STATE_ABBR_TO_FIPS[state_abbr]
    pattern = resource_path(f"data/tl_2022_{state_fips}*_addrfeat.shp")
    files = glob.glob(pattern)
    if not files:
        print(f"No addrfeat files found for {state_abbr} (pattern: {pattern})")
        return None, None
    number, name = parse_street(street)
    for f in files:
        addr_gdf = gpd.read_file(f)
        addr_gdf["NAME_clean"] = addr_gdf["FULLNAME"].apply(clean_street_name)
        LFROM, LTO, RFROM, RTO = get_addr_range_cols(addr_gdf)
        candidates = addr_gdf[addr_gdf["NAME_clean"] == name]
        if zip_code:
            zip_candidates = candidates[
                (candidates["ZIPL"].astype(str) == str(zip_code)) |
                (candidates["ZIPR"].astype(str) == str(zip_code))
            ]
        else:
            zip_candidates = candidates
        if not zip_candidates.empty:
            for idx, row in zip_candidates.iterrows():
                for side, from_col, to_col in [('L', LFROM, LTO), ('R', RFROM, RTO)]:
                    try:
                        from_num = int(row[from_col]) if row[from_col] else None
                        to_num = int(row[to_col]) if row[to_col] else None
                    except Exception:
                        from_num, to_num = None, None
                    if from_num and to_num and min(from_num, to_num) <= number <= max(from_num, to_num):
                        frac = (number - from_num) / (to_num - from_num) if from_num != to_num else 0.5
                        point = row['geometry'].interpolate(frac, normalized=True)
                        print(f"Success! {row['FULLNAME']} ({from_num}-{to_num}), {row['ZIPL']}/{row['ZIPR']}, {point.x},{point.y}")
                        return point.x, point.y
    return None, None

def latlon_to_geoid(lon, lat, gdfs, state_abbr=None):
    pt = Point(lon, lat)
    if state_abbr and state_abbr in gdfs:
        gdf = gdfs[state_abbr]
        match = gdf[gdf.contains(pt)]
        if not match.empty:
            return match.iloc[0]['GEOID'], state_abbr
    for abbr, gdf in gdfs.items():
        match = gdf[gdf.contains(pt)]
        if not match.empty:
            return match.iloc[0]['GEOID'], abbr
    return None, None

# ----------- Lookup functions (try FIPS of 11, 10, 9 digits)
def lookup_any_fips(fips, df, fips_col="FIPS"):
    fips_list = [fips[:11].zfill(11), fips[:10].zfill(10), fips[:9].zfill(9)]
    for f in fips_list:
        row = df[df[fips_col] == f]
        if not row.empty:
            return row.iloc[0].to_dict()
    return None

def lookup_sdi(tract_fips, df):
    data = lookup_any_fips(tract_fips, df, "FIPS")
    if not data: return None
    return {
        "FIPS": data.get("FIPS", ""),
        "SDI_score": data.get("SDI_score", ""),
        "sdi": data.get("sdi", "")
    }

def lookup_svi(tract_fips, df):
    data = lookup_any_fips(tract_fips, df, "FIPS")
    if not data: return None
    return {
        "EPL_POV150": data.get("EPL_POV150", ""),
        "EPL_MINRTY": data.get("EPL_MINRTY", ""),
        "SPL_THEMES": data.get("SPL_THEMES", ""),
        "RPL_THEMES": data.get("RPL_THEMES", "")
    }

def lookup_adi(tract_fips, df):
    data = lookup_any_fips(tract_fips, df, "FIPS")
    if not data: return None
    return {
        "ADI_NATRANK": data.get("ADI_NATRANK", ""),
        "ADI_STATERNK": data.get("ADI_STATERNK", "")
    }

def lookup_acs(tract_fips, df):
    data = lookup_any_fips(tract_fips, df, "FIPS")
    if not data: return None
    return {
        "median_income": data.get("median_income", ""),
        "ACS_deprivation_index": data.get("ACS_deprivation_index", "")
    }

def lookup_brokamp(zip_code, df):
    row = df[df["Zip code"] == str(zip_code).zfill(5)]
    if not row.empty:
        return {
            "Brokamp_ADI": row.iloc[0].get("Brokamp Area Deprivation Index (ADI)", "")
        }
    return None

def lookup_coi(tract_fips, df):
    # GEOID in Excel
    fips_list = [tract_fips[:11].zfill(11), tract_fips[:10].zfill(10), tract_fips[:9].zfill(9)]
    for f in fips_list:
        row = df[df["GEOID"] == f]
        if not row.empty:
            data = row.iloc[0]
            return {
                "COI_national": data.get("COI nationally normed", ""),
                "z_COI_national": data.get("z score COI nationally normed", ""),
                "COI_education": data.get("COI education domain, nationally normed", ""),
                "z_COI_education": data.get("z score COI education domain, nationally normed", ""),
                "COI_health": data.get("COI health and environment domain, nationally normed", ""),
                "z_COI_health": data.get("z score COI health and environment domain, nationally normed", ""),
                "COI_social": data.get("COI social and economic domain, nationally normed", ""),
                "z_COI_social": data.get("z score COI social and economic domain, nationally normed", "")
            }
    return None

# ----------- Flask route
@app.route('/', methods=["GET", "POST"])
def index():
    result = error = geoid = state_abbr = None
    svi_data = adi_data = acs_data = acs_zip_data = coi_data = None

    if request.method == "POST":
        street = request.form.get("street", "").strip()
        city = request.form.get("city", "").strip()  # not currently used but available
        state = request.form.get("state", "").strip()
        zip_code = request.form.get("zip", "").strip()
        if not state or state not in STATE_ABBR_TO_FIPS:
            error = "Please select a valid state or territory."
        elif not street or not zip_code:
            error = "Please enter both a street address and ZIP code."
        else:
            lon, lat = offline_geocode(street, zip_code, state)
            if lon is None or lat is None:
                error = "Could not match that address. Please check the spelling and number."
            else:
                geoid, matched_state = latlon_to_geoid(lon, lat, gdfs_tracts, state)
                if not geoid:
                    error = f"Could not find a census tract for that address (lat/lon: {lat}, {lon})."
                else:
                    tract_fips = str(geoid).zfill(11)
                    print(f"Full GEOID: {geoid}, will try tract FIPS for lookup: {[tract_fips[:11], tract_fips[:10], tract_fips[:9]]}")

                    result = lookup_sdi(tract_fips, sdi_df)
                    svi_data = lookup_svi(tract_fips, svi_df)
                    adi_data = lookup_adi(tract_fips, adi_df)
                    acs_data = lookup_acs(tract_fips, acs_df)
                    acs_zip_data = lookup_brokamp(zip_code, brokamp_df)
                    coi_data = lookup_coi(tract_fips, coi_df)

                    print(f"SDI lookup: {result if result else 'No match'}")
                    print(f"SVI lookup: {svi_data if svi_data else 'No match'}")
                    print(f"ADI lookup: {adi_data if adi_data else 'No match'}")
                    print(f"ACS lookup: {acs_data if acs_data else 'No match'}")
                    print(f"Brokamp lookup: {acs_zip_data if acs_zip_data else 'No match'}")
                    print(f"COI lookup: {coi_data if coi_data else 'No match'}")

                    state_abbr = matched_state

    return render_template(
        "index.html",
        result=result,
        error=error,
        geoid=geoid,
        state_abbr=state_abbr,
        states=STATE_NAMES,
        svi_data=svi_data,
        adi_data=adi_data,
        acs_data=acs_data,
        acs_zip_data=acs_zip_data,
        coi_data=coi_data
    )

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        app.run(debug=False, port=5001)
    else:
        app.run(debug=True, port=5001)
