#!/usr/bin/env python3
"""
State Downloader Utility
Users can run this to download additional state data packages.
"""

import os
import sys
import zipfile
import urllib.request
from pathlib import Path

# Replace with your actual GitHub release URL
GITHUB_RELEASE_URL = "https://github.com/emgoatee/OfflineGeoSDOH/releases/download"
DEFAULT_VERSION = "v1.0.3"

STATE_FIPS = {
    '01': 'AL - Alabama',
    '02': 'AK - Alaska',
    '04': 'AZ - Arizona',
    '05': 'AR - Arkansas',
    '06': 'CA - California',
    '08': 'CO - Colorado',
    '09': 'CT - Connecticut',
    '10': 'DE - Delaware',
    '11': 'DC - District of Columbia',
    '12': 'FL - Florida',
    '13': 'GA - Georgia',
    '15': 'HI - Hawaii',
    '16': 'ID - Idaho',
    '17': 'IL - Illinois',
    '18': 'IN - Indiana',
    '19': 'IA - Iowa',
    '20': 'KS - Kansas',
    '21': 'KY - Kentucky',
    '22': 'LA - Louisiana',
    '23': 'ME - Maine',
    '24': 'MD - Maryland',
    '25': 'MA - Massachusetts',
    '26': 'MI - Michigan',
    '27': 'MN - Minnesota',
    '28': 'MS - Mississippi',
    '29': 'MO - Missouri',
    '30': 'MT - Montana',
    '31': 'NE - Nebraska',
    '32': 'NV - Nevada',
    '33': 'NH - New Hampshire',
    '34': 'NJ - New Jersey',
    '35': 'NM - New Mexico',
    '36': 'NY - New York',
    '37': 'NC - North Carolina',
    '38': 'ND - North Dakota',
    '39': 'OH - Ohio',
    '40': 'OK - Oklahoma',
    '41': 'OR - Oregon',
    '42': 'PA - Pennsylvania',
    '44': 'RI - Rhode Island',
    '45': 'SC - South Carolina',
    '46': 'SD - South Dakota',
    '47': 'TN - Tennessee',
    '48': 'TX - Texas',
    '49': 'UT - Utah',
    '50': 'VT - Vermont',
    '51': 'VA - Virginia',
    '53': 'WA - Washington',
    '54': 'WV - West Virginia',
    '55': 'WI - Wisconsin',
    '56': 'WY - Wyoming',
    '60': 'AS - American Samoa',
    '66': 'GU - Guam',
    '69': 'MP - Northern Mariana Islands',
    '72': 'PR - Puerto Rico',
    '78': 'VI - U.S. Virgin Islands'
}

def get_data_dir():
    """Get the data directory path (handles both dev and frozen app)."""
    # When running from installed .app, use the Resources/data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')

    # Make sure it exists
    os.makedirs(data_dir, exist_ok=True)

    return data_dir

def check_installed_states():
    """Check which states are already installed."""
    data_dir = get_data_dir()
    installed = []

    for fips, name in STATE_FIPS.items():
        abbr = name.split(' - ')[0]
        tract_file = f"tl_2022_{fips}_tract.shp"
        if os.path.exists(os.path.join(data_dir, tract_file)):
            installed.append(abbr)

    return installed

def download_state(state_abbr, version=DEFAULT_VERSION):
    """Download a state package from GitHub releases."""

    url = f"{GITHUB_RELEASE_URL}/{version}/state_{state_abbr}.zip"
    data_dir = get_data_dir()

    # Ensure data directory exists and is writable
    os.makedirs(data_dir, exist_ok=True)

    print(f"\nDownloading {state_abbr}...")
    print(f"URL: {url}")

    try:
        # Download to temp directory to avoid permission issues
        import tempfile
        temp_dir = tempfile.gettempdir()
        zip_path = os.path.join(temp_dir, f"state_{state_abbr}.zip")

        urllib.request.urlretrieve(url, zip_path)

        # Extract to data directory
        print(f"Extracting to {data_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)

        # Clean up ZIP file
        os.remove(zip_path)

        print(f"✓ {state_abbr} installed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error downloading {state_abbr}: {e}")
        return False

def interactive_mode():
    """Interactive mode for downloading states."""

    print("=" * 60)
    print("OfflineGeoLocator - State Downloader")
    print("=" * 60)
    print()

    # Check installed states
    installed = check_installed_states()
    print(f"Currently installed states ({len(installed)}): {', '.join(sorted(installed))}")
    print()

    # Show available states
    print("Available states to download:")
    print()

    for fips, name in sorted(STATE_FIPS.items()):
        abbr = name.split(' - ')[0]
        status = "✓ Installed" if abbr in installed else "  Available"
        print(f"  {abbr:3s} - {name:30s} {status}")

    print()
    print("Enter state codes separated by spaces (e.g., 'OH PA NY')")
    print("Or enter 'ALL' to download all states")
    print("Or enter 'QUIT' to exit")
    print()

    while True:
        choice = input("States to download: ").strip().upper()

        if choice == 'QUIT':
            break

        if choice == 'ALL':
            states_to_download = [name.split(' - ')[0] for name in STATE_FIPS.values()]
        else:
            states_to_download = choice.split()

        # Validate states
        valid_states = [s for s in states_to_download if any(name.startswith(s + ' - ') for name in STATE_FIPS.values())]

        if not valid_states:
            print("No valid states entered. Please try again.")
            continue

        # Download states
        for state in valid_states:
            if state in installed:
                print(f"\n{state} is already installed. Skipping...")
                continue

            download_state(state)

        print("\nDownload complete!")
        print("Please restart the application for changes to take effect.")
        break

def main():
    if len(sys.argv) > 1:
        # Command line mode
        states = [s.upper() for s in sys.argv[1:]]
        for state in states:
            download_state(state)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == '__main__':
    main()
