import requests
import sys
from datetime import datetime, timedelta, timezone


class SunPosition:
    """Handles the calculation of sun's position (sunrise and sunset times) and the time of day."""
    
    # This dictionary maps the time of day to the image file name.
    IMAGE_MAP = {
        'morning': 'morning.png',
        'noon': 'noon.png',
        'sunrise': 'sunrise.png',
        'sunset': 'sunset.png',
        'evening': 'evening.png',
        'night': 'night.png',
    }

    def __init__(self, latitude, longitude):
        # Initialize with the latitude and longitude of the location
        self.latitude = latitude
        self.longitude = longitude
        self.sunrise = None
        self.sunset = None

    def get_sun_times(self):
        """Fetches the sunrise and sunset times from an API and converts them to datetime objects."""
        try:
            # API URL to get sunrise and sunset times in UTC
            url = f"https://api.sunrise-sunset.org/json?lat={self.latitude}&lng={self.longitude}&formatted=0"
            response = requests.get(url)
            data = response.json()
            
            # If the API call is successful and returns valid data
            if response.status_code == 200 and "results" in data:
                sunrise_utc = data['results']['sunrise']
                sunset_utc = data['results']['sunset']
                
                # Convert the sunrise and sunset times from strings to datetime objects in UTC
                self.sunrise = datetime.fromisoformat(sunrise_utc.replace("Z", "+00:00"))
                self.sunset = datetime.fromisoformat(sunset_utc.replace("Z", "+00:00"))
                return self.sunrise, self.sunset
            else:
                raise ValueError("Could not fetch valid sunrise and sunset times from the API.")
        
        except requests.RequestException as e:
            raise ConnectionError(f"Problem connecting to the API: {e}")

    def get_current_time_utc(self):
        """Returns the current UTC time as a datetime object."""
        return datetime.now(timezone.utc)

    def get_time_of_day(self, current_time):
        """
        Determines the time of day based on the current time and the sunrise and sunset times.
        It returns a category such as 'morning', 'noon', 'sunrise', etc.
        """
        # Before sunrise, consider it night time
        if current_time < self.sunrise:
            return 'night'
        
        # Between sunrise and noon, it's morning
        elif self.sunrise <= current_time < self.sunrise + timedelta(hours=6):
            return 'morning'
        
        # Around noon
        elif self.sunrise + timedelta(hours=6) <= current_time < self.sunrise + timedelta(hours=12):
            return 'noon'
        
        # After noon but before sunset, consider it evening
        elif self.sunset - timedelta(hours=6) <= current_time < self.sunset:
            return 'evening'
        
        # After sunset, consider it night time
        elif current_time >= self.sunset:
            return 'night'
        
        # If it's exactly sunrise, consider it 'sunrise'
        elif current_time == self.sunrise:
            return 'sunrise'
        
        # If it's exactly sunset, consider it 'sunset'
        elif current_time == self.sunset:
            return 'sunset'


def print_image_for_time_of_day(sun_position):
    """Fetches and prints the image file name based on the time of day for the given sun position."""
    try:
        # Get the sunrise and sunset times
        sunrise, sunset = sun_position.get_sun_times()
    except (ValueError, ConnectionError) as e:
        # If something goes wrong, show the error and exit
        print(f"Error: {e}")
        sys.exit(1)

    # Get the current UTC time
    current_time = sun_position.get_current_time_utc()

    # Determine the time of day based on current time and sun's position
    time_of_day = sun_position.get_time_of_day(current_time)

    # Output the correct image file name based on the time of day
    print(sun_position.IMAGE_MAP.get(time_of_day, 'night.png'))


def main():
    """Main function to run the program, which takes latitude and longitude from the command-line."""
    # Make sure there are enough arguments (latitude and longitude)
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <latitude> <longitude>")
        sys.exit(1)

    try:
        # Convert latitude and longitude from command-line arguments to floats
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
    except ValueError:
        # If they are not valid numbers, show an error and exit
        print("Latitude and longitude must be valid numbers.")
        sys.exit(1)

    # Create an instance of SunPosition with the given coordinates
    sun_position = SunPosition(latitude, longitude)

    # Determine and print the correct image based on the time of day
    print_image_for_time_of_day(sun_position)


if __name__ == "__main__":
    main()
