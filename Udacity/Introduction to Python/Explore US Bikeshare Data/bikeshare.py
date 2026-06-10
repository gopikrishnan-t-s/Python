# Import the time module so we can measure how long each stats calculation takes
import time

# Import pandas for loading and analyzing the bikeshare CSV data
import pandas as pd

# Import numpy (not heavily used here, but commonly included in this project)
import numpy as np


# Dictionary that maps each city name to its corresponding CSV file
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """
    Ask the user to specify a city, month, and day for analysis.

    Returns:
        city  (str): selected city
        month (str): selected month or 'all'
        day   (str): selected day or 'all'
    """

    # Greeting shown when the program starts
    print("Hello! Let's explore some US bikeshare data!")

    # Valid options for user input
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # ---------------- CITY INPUT ----------------
    # Keep asking until the user enters a valid city
    while True:
        city = input("Please enter a city (chicago, new york city, washington): ").strip().lower()

        # If input is valid, stop the loop
        if city in valid_cities:
            break

        # Otherwise show error and ask again
        print("Invalid city. Please try again.")

    # ---------------- MONTH INPUT ----------------
    # Keep asking until the user enters a valid month
    while True:
        month = input("Please enter a month (all, january, february, march, april, may, june): ").strip().lower()

        if month in valid_months:
            break

        print("Invalid month. Please try again.")

    # ---------------- DAY INPUT ----------------
    # Keep asking until the user enters a valid day
    while True:
        day = input("Please enter a day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ").strip().lower()

        if day in valid_days:
            break

        print("Invalid day. Please try again.")

    # Divider line for cleaner output
    print('-' * 40)

    # Return the validated user inputs
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and filter by month/day if needed.

    Args:
        city  (str): selected city
        month (str): selected month or 'all'
        day   (str): selected day or 'all'

    Returns:
        df (DataFrame): filtered pandas DataFrame
    """

    # Read the correct city CSV file into a pandas DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column from string to datetime
    # This allows us to extract month, day, and hour easily
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create a new column for month number (January=1, February=2, etc.)
    df['month'] = df['Start Time'].dt.month

    # Create a new column for day of week in lowercase
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Create a new column for the hour when the trip started
    df['hour'] = df['Start Time'].dt.hour

    # ---------------- FILTER BY MONTH ----------------
    # Only apply filtering if the user didn't choose 'all'
    if month != 'all':
        # Convert the month name into its corresponding month number
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1

        # Keep only rows where the month matches
        df = df[df['month'] == month_num]

    # ---------------- FILTER BY DAY ----------------
    # Only apply filtering if the user didn't choose 'all'
    if day != 'all':
        # Keep only rows where the day_of_week matches
        df = df[df['day_of_week'] == day]

    # Return the filtered DataFrame
    return df


def time_stats(df):
    """
    Display statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # Store the current time to measure how long this function takes
    start_time = time.time()

    # If the filtered DataFrame has no rows, avoid errors
    if df.empty:
        print("No data available for the selected filters.")
    else:
        # ---------------- MOST COMMON MONTH ----------------
        # mode()[0] returns the most frequent value in the 'month' column
        common_month_num = df['month'].mode()[0]

        # Convert month number back to readable month name
        month_name = ['January', 'February', 'March', 'April', 'May', 'June'][common_month_num - 1]
        print("Most Common Month:", month_name)

        # ---------------- MOST COMMON DAY OF WEEK ----------------
        common_day = df['day_of_week'].mode()[0].title()
        print("Most Common Day of Week:", common_day)

        # ---------------- MOST COMMON START HOUR ----------------
        common_hour = df['hour'].mode()[0]
        print("Most Common Start Hour:", common_hour)

    # Print elapsed time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """
    Display statistics on the most popular stations and trip combination.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
    else:
        # ---------------- MOST COMMON START STATION ----------------
        print("Most Common Start Station:", df['Start Station'].mode()[0])

        # ---------------- MOST COMMON END STATION ----------------
        print("Most Common End Station:", df['End Station'].mode()[0])

        # ---------------- MOST FREQUENT TRIP COMBINATION ----------------
        # Create a helper column combining start and end station
        df['Trip Combination'] = df['Start Station'] + " -> " + df['End Station']

        # Identify the most common combined trip
        print("Most Frequent Trip Combination:", df['Trip Combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """
    Display statistics on total and average trip duration.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
    else:
        # ---------------- TOTAL TRAVEL TIME ----------------
        total_travel_time = df['Trip Duration'].sum()
        print("Total Travel Time:", total_travel_time)

        # ---------------- MEAN TRAVEL TIME ----------------
        mean_travel_time = df['Trip Duration'].mean()
        print("Mean Travel Time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """
    Display statistics on bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
    else:
        # ---------------- USER TYPE COUNTS ----------------
        print("User Type Counts:")
        print(df['User Type'].value_counts())
        print()

        # ---------------- GENDER COUNTS ----------------
        # Washington usually does not contain Gender column
        if 'Gender' in df.columns:
            print("Gender Counts:")
            print(df['Gender'].value_counts())
            print()
        else:
            print("Gender data not available for this city.\n")

        # ---------------- BIRTH YEAR STATS ----------------
        # Washington usually does not contain Birth Year column
        if 'Birth Year' in df.columns:
            earliest_year = int(df['Birth Year'].min())
            most_recent_year = int(df['Birth Year'].max())
            most_common_year = int(df['Birth Year'].mode()[0])

            print("Earliest Birth Year:", earliest_year)
            print("Most Recent Birth Year:", most_recent_year)
            print("Most Common Birth Year:", most_common_year)
        else:
            print("Birth Year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """
    Display raw trip data in chunks of 5 rows if the user requests it.
    Stops when the user says 'no' or when all rows have been displayed.
    """

    # Start from the first row
    row_index = 0

    # Continue while there are still rows left to show
    while row_index < len(df):
        view_data = input('\nWould you like to view 5 lines of raw data? Enter yes or no:\n').strip().lower()

        # If user wants to see raw data
        if view_data == 'yes':
            # Display 5 rows starting from row_index
            print(df.iloc[row_index:row_index + 5].to_string())

            # Move to the next chunk of 5 rows
            row_index += 5

            # If there is no more data left after this chunk, notify user
            if row_index >= len(df):
                print('\nNo more raw data to display.')

        # If user says no, stop the raw data loop
        elif view_data == 'no':
            break

        # Handle invalid input
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def main():
    """
    Main control loop of the program.
    Runs repeatedly until the user chooses not to restart.
    """

    while True:
        # Step 1: get filter choices from user
        city, month, day = get_filters()

        # Step 2: load and filter the data
        df = load_data(city, month, day)

        # Step 3: show all required statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Step 4: optionally show raw data
        display_raw_data(df)

        # Step 5: ask if user wants to restart
        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()

        # If the user does not type yes, end the program
        if restart != 'yes':
            break


# This ensures that main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
