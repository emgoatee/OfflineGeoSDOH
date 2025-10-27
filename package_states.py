#!/usr/bin/env python3
"""
Script to package individual state data into separate ZIP files.
This allows users to download only the states they need.
"""

import os
import zipfile
import glob
from pathlib import Path

# State FIPS codes
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

def package_state(fips, abbr, data_dir='data', output_dir='state_packages'):
    """Package all files for a specific state into a ZIP file."""

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all files for this state
    pattern = f"tl_2022_{fips}*"
    files = glob.glob(os.path.join(data_dir, pattern))

    if not files:
        print(f"  No files found for {abbr} (FIPS: {fips})")
        return None

    # Create ZIP file
    zip_path = os.path.join(output_dir, f"state_{abbr}.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files:
            # Add file to zip with just the filename (no path)
            zipf.write(file_path, os.path.basename(file_path))

    # Get size
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"  ✓ {abbr}: {len(files)} files, {size_mb:.1f} MB")

    return zip_path

def package_core_data(data_dir='data', output_dir='state_packages'):
    """Package core CSV/Excel files (not state-specific)."""

    os.makedirs(output_dir, exist_ok=True)

    # Core data files (not state-specific shapefiles)
    core_files = [
        'ACS_deprivation_index.csv',
        'ACS_deprivation_index_by_zipcode.csv',
        'COI_subdomin_data.csv',
        'COI_subdomin_data.xlsx',
        'SVI_2022_US.csv',
        'adi.csv',
        'geodata.csv',
        'hud_zip_tract.csv'
    ]

    zip_path = os.path.join(output_dir, 'core_data.zip')

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in core_files:
            file_path = os.path.join(data_dir, filename)
            if os.path.exists(file_path):
                zipf.write(file_path, filename)

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"Core data: {size_mb:.1f} MB")

    return zip_path

def main():
    print("Packaging state data files...\n")

    # Package core data first
    print("Packaging core data files...")
    package_core_data()
    print()

    # Package each state
    print("Packaging individual states:")
    total_size = 0

    for fips, abbr in sorted(STATE_FIPS.items()):
        zip_path = package_state(fips, abbr)
        if zip_path:
            total_size += os.path.getsize(zip_path)

    print(f"\nTotal size of all state packages: {total_size / (1024**3):.2f} GB")
    print(f"State packages saved to: state_packages/")
    print("\nUsers can download:")
    print("  1. Core app executable")
    print("  2. core_data.zip (required)")
    print("  3. Individual state ZIP files they need")

if __name__ == '__main__':
    main()
