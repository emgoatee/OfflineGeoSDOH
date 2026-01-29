import pandas as pd
import os
from decimal import Decimal

def parse_fips_adi(val):
    try:
        s_val = str(val).strip().upper()
        if 'E+' in s_val:
            return "CORRUPTED"
        return str(int(Decimal(s_val)))
    except:
        return str(val)

ADI_PATH = 'data/adi.csv'

if os.path.exists(ADI_PATH):
    print(f"Reading {ADI_PATH}...")
    adi_df = pd.read_csv(ADI_PATH, converters={'FIPS': parse_fips_adi}, dtype={'ADI_NATRANK': str, 'ADI_STATERNK': str})
    
    corrupted_count = (adi_df['FIPS'] == "CORRUPTED").sum()
    duplicate_count = adi_df['FIPS'].duplicated().sum()
    
    print(f"Corrupted count (scientific notation): {corrupted_count}")
    print(f"Duplicate FIPS count: {duplicate_count}")
    
    if corrupted_count > 0 or duplicate_count > 100:
        print("RESULT: Corruption DETECTED (Success)")
    else:
        print("RESULT: No corruption detected (Failure - we expect corruption in this file)")
else:
    print(f"File not found: {ADI_PATH}")
