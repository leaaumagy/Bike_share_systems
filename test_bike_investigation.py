import unittest
import pandas as pd
from bike_investigation import time_stats, station_stats, trip_duration_stats, user_stats, count_null_values

class TestBikeShareData(unittest.TestCase):

    def test_time_stats(self):
        """
        Test the time_stats function with valid data.
        """
        data = {
            'Start Time': ['2017-01-01 09:07:57', '2017-01-02 09:07:57', '2017-01-03 00:07:57'],
            'End Time': ['2017-01-01 09:20:53', '2017-01-02 09:20:53', '2017-01-03 00:20:53'],
        }
        df = pd.DataFrame(data)
        df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

        # Extract month, day of the week, and hour from Start Time
        df['month'] = df['Start Time'].dt.strftime('%B')
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour.astype('Int64')

        result = time_stats(df)

        # Check the most common month, day, and hour
        self.assertEqual(result['most_common_month'], 'January')
        self.assertEqual(result['most_common_day'], 'Monday')
        self.assertEqual(result['most_common_hour'], 9)

    def test_station_stats(self):
        """
        Test the station_stats function with valid data.
        """
        data = {
            'Start Station': ['Station A', 'Station B', 'Station A'],
            'End Station': ['Station B', 'Station C', 'Station B'],
        }
        df = pd.DataFrame(data)

        result = station_stats(df)

        # Check the most common start station, end station, and trip
        self.assertEqual(result['most_common_start_station'], 'Station A')
        self.assertEqual(result['most_common_end_station'], 'Station B')
        self.assertEqual(result['most_common_trip'], ('Station A', 'Station B'))

    def test_trip_duration_stats(self):
        """
        Test the trip_duration_stats function with valid data.
        """
        data = {
            'Trip Duration': [300, 200, 150, 86400],
        }
        df = pd.DataFrame(data)

        result = trip_duration_stats(df)

        # Check the total and mean travel time
        self.assertEqual(result['total_travel_time'], "10 minutes 50 seconds")
        self.assertEqual(result['mean_travel_time'], "3 minutes 36 seconds")
        
    def test_user_stats(self):
        """
        Test the user_stats function with valid data.
        """
        data = {
            'User Type': ['Subscriber', 'Customer', 'subscriber', 'Unknown'],
            'Gender': ['Male', 'Female', 'male', 'non-binary'],
            'Birth Year': [1985, 1992, 1985, 2030],
        }
        df = pd.DataFrame(data)

        result = user_stats(df)

        # Check user types, gender counts, and birth year statistics
        self.assertEqual(result['user_types']['subscriber'], 2)
        self.assertEqual(result['user_types']['customer'], 1)

        self.assertEqual(result['gender_counts']['male'], 2)
        self.assertEqual(result['gender_counts']['female'], 1)

        self.assertEqual(result['earliest_year'], 1985)
        self.assertEqual(result['most_recent_year'], 1992)
        self.assertEqual(result['most_common_year'], 1985)

        # Check for null values
        null_values = count_null_values(df)
        self.assertEqual(null_values['Gender'], 1) # 'Unknown' is a null value
        self.assertEqual(null_values['User Type'], 1) # 'non-binary' is a null value
        self.assertEqual(null_values['Birth Year'], 1) # '2030' is a null value because is does not possible
        
    def test_time_stats_missing_data(self):
        """
        Test the time_stats function with missing data.
        """
        data = {
            'Start Time': ['2017-01-01 09:07:57', '2017-01-02 09:07:57', None],
            'End Time': ['2017-01-01 09:20:53', None, '2017-01-03 00:20:53'],
        }
        df = pd.DataFrame(data)
        df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

        # Extract month, day of the week, and hour from Start Time
        df['month'] = df['Start Time'].dt.strftime('%B')
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour.astype('Int64')

        result = time_stats(df)

        # Check the most common month, day, and hour
        self.assertEqual(result['most_common_month'], 'January')
        self.assertEqual(result['most_common_day'], 'Monday')
        self.assertEqual(result['most_common_hour'], 9)
        
    def test_station_stats_missing_data(self):
        """
        Test the station_stats function with missing data.
        """
        data = {
            'Start Station': ['Station A', 'Station B', None],
            'End Station': ['Station B', 'Station C', None],
        }
        df = pd.DataFrame(data)

        result = station_stats(df)

        # Check the most common start station, end station, and trip
        self.assertEqual(result['most_common_start_station'], 'Station A')
        self.assertEqual(result['most_common_end_station'], 'Station B')
        self.assertEqual(result['most_common_trip'], ('Station A', 'Station B'))

    def test_trip_duration_stats_missing_data(self):
        """
        Test the trip_duration_stats function with missing data.
        """
        data = {
            'Trip Duration': [300, None, 150, 'test'],
        }
        df = pd.DataFrame(data)

        result = trip_duration_stats(df)

        # Check the total and mean travel time
        self.assertEqual(result['total_travel_time'], "7 minutes 30 seconds")
        self.assertEqual(result['mean_travel_time'], "3 minutes 45 seconds")

    def test_trip_duration_minute(self):
        """
        Test the trip_duration_stats function with durations exactly one minute.
        """
        data = {
            'Trip Duration': [60, 60],
        }
        df = pd.DataFrame(data)

        result = trip_duration_stats(df)

        # Check the total and mean travel time
        self.assertEqual(result['total_travel_time'], "2 minutes")
        self.assertEqual(result['mean_travel_time'], "1 minute")    
        
    def test_user_stats_missing_data(self):
        """
        Test the user_stats function with missing data.
        """
        data = {
            'User Type': ['Subscriber', 'Customer', None, 'cutomer'],
            'Gender': ['Male', 'Female', None, 'Mle'],
            'Birth Year': [1985, None, 1985, 1850],
        }
        df = pd.DataFrame(data)

        result = user_stats(df)

        # Check user types, gender counts, and birth year statistics
        self.assertEqual(result['user_types']['subscriber'], 1)
        self.assertEqual(result['user_types']['customer'], 1)
        
        self.assertEqual(result['gender_counts']['male'], 1)
        self.assertEqual(result['gender_counts']['female'], 1)

        self.assertEqual(result['earliest_year'], 1985) # Because 1850 it is too early to be possible in this context
        self.assertEqual(result['most_recent_year'], 1985)
        self.assertEqual(result['most_common_year'], 1985)

if __name__ == '__main__':
    unittest.main()
