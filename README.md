# Wallpaper-selector

This program selects a desktop wallpaper based on the current time of day for a given geographical location (latitude and longitude). The wallpaper is selected based on the position of the sun (sunrise, sunset, etc.) retrieved from the Sunrise-Sunset API.

## Requirements

- Python 3.x
- Requests library (`pip install requests`)

## Usage

Run the script from the command line with the following command:

```bash
python3 script.py <latitude> <longitude>
