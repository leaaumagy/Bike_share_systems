import time
import numpy as np
import pandas as pd

# Dictionary mapping city names to their corresponding CSV file paths
CITY_DATA = {
    "chicago": "Bike_raw_data/chicago.csv",
    "new york city": "Bike_raw_data/new_york_city.csv",
    "washington": "Bike_raw_data/washington.csv",
}

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - Name of the city to analyze
        (str) month - Name of the month to filter by, or "all" to apply no month filter
        (str) day - Name of the day of the week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some bikeshare data!")

    # Define available cities
    cities = ["chicago", "new york city", "washington"]
    city = ""
    
    # Prompt user for city selection until a valid city is provided
    while city not in cities:
        city = input("Select a city from Chicago, New York City, or Washington: ").lower()
        if city not in cities:
            print("Invalid input. Please choose from Chicago, New York City, or Washington.")
    
    # Define available months
    months = ["january", "february", "march", "april", "may", "june", "all"]
    month = ""
    
    # Prompt user for month selection until a valid month is provided
    while month not in months:
        month = input("Select a month between January, February, March, April, May, and June, or 'all' to apply no month filter: ").lower()
        if month not in months:
            print("Invalid input. Please choose a valid month or 'all'.")
    
    # Define available days
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
    day = ""
    
    # Prompt user for day selection until a valid day is provided
    while day not in days:
        day = input("Select a day of the week between Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday, or 'all' to apply no day filter: ").lower()
        if day not in days:
            print("Invalid input. Please choose a valid day or 'all'.")
    
    print("-" * 40)  # Print a separator line for better readability
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - Name of the city to analyze
        (str) month - Name of the month to filter by, or "all" to apply no month filter
        (str) day - Name of the day of the week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        # Load data from the CSV file corresponding to the selected city
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print(f"Error: The file for {city} does not exist.")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found

    # Check if the DataFrame contains the required columns for temporal analysis
    if 'Start Time' in df.columns and 'End Time' in df.columns: 
        # Convert 'Start Time' and 'End Time' to datetime objects
        df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

        # Extract month, day of the week, and hour from 'Start Time'
        df['month'] = df['Start Time'].dt.strftime('%B')
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour.astype('Int64')

        # Filter by month if not 'all'
        if month.lower() != 'all':
            df = df[df['month'].str.lower() == month.lower()]

        # Filter by day if not 'all'
        if day != 'all':
            df = df[df['day_of_week'].str.lower() == day.lower()]
    else:
        print('The dataframe does not have temporal columns. Temporal filters are not applied.')
            
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (DataFrame) - Pandas DataFrame containing trip data with 'Start Time' column

    Displays:
        The most common month for bike trips
        The most common day of the week for bike trips
        The most common hour of the day for bike trips

    Returns:
        dict - A dictionary with the most common month, day, and hour
    """

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()  # Record start time for performance measurement

    # Initialize variables to store the most common month, day, and hour
    most_common_month, most_common_day, most_common_hour = [None] * 3
    
    # Check if the DataFrame contains the 'Start Time' column
    if 'Start Time' in df.columns: 
        # Calculate the most common month, day of the week, and start hour
        most_common_month = df['Start Time'].dt.strftime('%B').mode()[0]
        most_common_day = df['Start Time'].dt.day_name().mode()[0]
        most_common_hour = df['Start Time'].dt.hour.astype('Int64').mode()[0]
        print(f"The most common month is: {most_common_month}")
        print(f"The most common day of the week is: {most_common_day}")
        print(f"The most common start hour is: {most_common_hour}")
    else:
        print("`Start Time` column does not exist.")

    # Print time taken to calculate statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    
    return {
        'most_common_month': most_common_month,
        'most_common_day': most_common_day,
        'most_common_hour': most_common_hour
    }

def station_stats(df):
    """
    Displays statistics on the most popular stations and trips.

    Args:
        df (DataFrame) - Pandas DataFrame containing trip data with 'Start Station' and 'End Station' columns

    Displays:
        The most common start station
        The most common end station
        The most frequent trip (start station to end station)

    Returns:
        dict - A dictionary with the most common start station, end station, and trip
    """
    
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()  # Record start time for performance measurement
    
    # Initialize variables to store the most common start station, end station, and trip
    most_common_start_station, most_common_end_station, most_common_trip = [None] * 3

    # Check if the DataFrame contains 'Start Station' and 'End Station' columns
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        # Calculate the most common start station, end station, and most frequent trip
        most_common_start_station = df['Start Station'].mode()[0]
        most_common_end_station = df['End Station'].mode()[0]
        most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
        print(f"The most commonly used start station is: {most_common_start_station}")
        print(f"The most commonly used end station is: {most_common_end_station}")
        print(f"The most frequent combination of start station and end station trip is: {most_common_trip[0]} to {most_common_trip[1]}")
    else:
        print("`Start Station` or `End Station` column does not exist.")
    
    # Print time taken to calculate statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return {
        'most_common_start_station': most_common_start_station,
        'most_common_end_station': most_common_end_station,
        'most_common_trip': most_common_trip
    }

def format_time(seconds):
    """
    Formats time given in seconds into a readable string in hours, minutes, and seconds.

    Args:
        seconds (int or float) - Time duration in seconds

    Returns:
        (str) time_str - A formatted string representing the time in hours, minutes, and seconds
    """
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    # Build a formatted time string
    time_str = ""
    if hours > 0:
        time_str += f"{hours} hour{'s' if hours > 1 else ''} "
    if minutes > 0:
        time_str += f"{minutes} minute{'s' if minutes > 1 else ''} "
    if seconds > 0 or not time_str:
        time_str += f"{seconds} second{'s' if seconds > 1 else ''}"
    
    return time_str.strip()

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (DataFrame) - Pandas DataFrame containing trip data

    Displays:
        Total travel time in a readable format
        Mean travel time in a readable format

    Returns:
        dict - A dictionary with total and mean travel times formatted as strings
    """
    
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()  # Record start time for performance measurement
 
    # Initialize variables to store total and mean travel time
    total_travel_time, mean_travel_time = [None] * 2

    # Check if the DataFrame contains the 'Trip Duration' column
    if 'Trip Duration' in df.columns:
        # Ensure 'Trip Duration' is numeric and replace unrealistic values with NaN
        df['Trip Duration'] = pd.to_numeric(df['Trip Duration'], errors='coerce')
        df.loc[df['Trip Duration'] >= 86400, 'Trip Duration'] = None

        # Calculate total and mean travel time in seconds
        total_travel_time = df['Trip Duration'].sum()
        mean_travel_time = df['Trip Duration'].mean()

        # Format the travel times 
        total_travel_time = format_time(total_travel_time)
        mean_travel_time = format_time(mean_travel_time)
        
        # Display the results
        print(f"Total travel time: {total_travel_time}")
        print(f"Mean travel time: {mean_travel_time}")
    else:
        print("`Trip Duration` column does not exist.")

    # Print time taken to calculate statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return {
        'total_travel_time': total_travel_time,
        'mean_travel_time': mean_travel_time
    }

def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df (DataFrame) - Pandas DataFrame containing user data with 'User Type', 'Gender', and 'Birth Year' columns

    Displays:
        Counts of user types (e.g., Subscriber, Customer)
        Counts of gender (e.g., Male, Female)
        Earliest year of birth
        Most recent year of birth
        Most common year of birth

    Returns:
        dict - A dictionary with user type counts, gender counts, and birth year statistics
    """
    
    print("\nCalculating User Stats...\n")
    start_time = time.time()  # Record start time for performance measurement
    
    # Initialize variables to store user statistics
    user_types, gender_counts, earliest_year, most_recent_year, most_common_year = [None] * 5

    # Check if the DataFrame contains the 'User Type' column
    if 'User Type' in df.columns:
        # Standardize user types to lowercase and filter valid types
        df['User Type'] = df['User Type'].str.lower()
        valid_user_types = ['subscriber', 'customer']
        df['User Type'] = df['User Type'].apply(lambda x: x if x in valid_user_types else None)
        user_types = df['User Type'].value_counts()
        print(f"Counts of user types:\n{user_types}")
    else:
        print("\n`User Type` column does not exist.")
        
    # Check if the DataFrame contains the 'Gender' column
    if 'Gender' in df.columns:
        # Standardize gender values to lowercase and filter valid genders
        df['Gender'] = df['Gender'].str.lower()
        valid_genders = ['male', 'female']
        df['Gender'] = df['Gender'].apply(lambda x: x if x in valid_genders else None)
        gender_counts = df['Gender'].value_counts()
        print(f"\nCounts of gender:\n{gender_counts}")
    else:
        print("\n`Gender` column does not exist.")
        
    # Check if the DataFrame contains the 'Birth Year' column
    if 'Birth Year' in df.columns:
        # Convert 'Birth Year' to numeric and filter valid years
        df['Birth Year'] = pd.to_numeric(df['Birth Year'], errors='coerce')
        current_year = time.localtime().tm_year
        df['Birth Year'] = df['Birth Year'].apply(lambda x: x if 1900 <= x <= current_year else None)
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {most_recent_year}")
        print(f"Most common year of birth: {most_common_year}")
    else:
        print("\n`Birth Year` column does not exist.")
    
    # Print time taken to calculate statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    
    return {
        'user_types': user_types,
        'gender_counts': gender_counts,
        'earliest_year': earliest_year,
        'most_recent_year': most_recent_year,
        'most_common_year': most_common_year
    }

def count_null_values(df):
    """
    Counts and displays the number of null values in each column of the DataFrame.

    Args:
        df (DataFrame) - Pandas DataFrame to check for null values

    Returns:
        null_counts (Series) - Series with the count of null values for each column
    """
    
    print("\nCalculating null values in each column...\n")
    start_time = time.time()  # Record start time for performance measurement

    # Count null values in each column
    null_counts = df.isnull().sum()
    if null_counts[null_counts > 0].empty:
        print("No null values found in any column.")
    else:
        print(null_counts[null_counts > 0])
    
    # Print time taken to calculate null values
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    
    return null_counts

def main():
    """Main function to run the bikeshare data analysis."""
    while True:
        # Get user input for city, month, and day
        city, month, day = get_filters()
        # Load data based on user input
        df = load_data(city, month, day)

        # Check if the DataFrame is empty
        if df.empty:
            print("No data to analyze for the selected filters.")
            break
        else:
            # Perform and display analysis
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            count_null_values(df)
 
            # Ask user if they want to restart
            restart = input("\nWould you like to restart? Enter yes or no: ").lower()
            if restart != "yes":
                break  

if __name__ == "__main__":
    main()