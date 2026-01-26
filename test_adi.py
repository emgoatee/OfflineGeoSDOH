#!/usr/bin/env python3
"""Test script to verify ADI lookup fix with Decimal"""

import pandas as pd
from decimal import Decimal

# Load ADI data with the Decimal fix
print("Loading ADI data with Decimal for precision...")
def parse_fips(val):
    try:
        return str(int(Decimal(str(val))))
    except:
        return str(val)

adi_df = pd.read_csv("data/adi.csv", converters={'FIPS': parse_fips}, dtype={'ADI_NATRANK': str, 'ADI_STATERNK': str})
adi_df['FIPS'] = adi_df['FIPS'].astype(str).str.zfill(12)

print(f"ADI data loaded: {len(adi_df)} rows")
print(f"Sample FIPS codes: {adi_df['FIPS'].head().tolist()}")

# Test with DC tract FIPS
test_tract_fips = "11001006202"
print(f"\nTesting with tract FIPS: {test_tract_fips}")

prefix_match = adi_df[adi_df['FIPS'].str.startswith(test_tract_fips)]
print(f"Prefix match result: {len(prefix_match)} rows")

if not prefix_match.empty:
    print("\nSUCCESS! Found matching rows:")
    for _, row in prefix_match.head(3).iterrows():
        print(f"  FIPS: {row['FIPS']}, ADI_NATRANK: {row['ADI_NATRANK']}, ADI_STATERNK: {row['ADI_STATERNK']}")
else:
    print("\nNo matches found. Checking DC FIPS codes in data:")
    dc_codes = adi_df[adi_df['FIPS'].str.startswith('11')]['FIPS'].head(10).tolist()
    print(f"  Found {len(dc_codes)} DC codes")
    if dc_codes:
        print(f"  Samples: {dc_codes}")
