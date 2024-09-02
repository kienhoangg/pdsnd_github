import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

VALID_MONTHS = [ 'january', 'february', 'march', 'april', 'may','june']
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
   
    city = month = day = ''
    while city.lower() not in CITY_DATA.keys():
       city = input('Input city (chicago, new york city, washington): ')
    
    # Get user input for month (all, january, february, ... , june) using a while loop to handle invalid inputs
    while month.lower() not in VALID_MONTHS:
       month = input('Input month: ')

    # Get user input for day of week (all, monday, tuesday, ... sunday) using a while loop to handle invalid inputs
    while day.lower() not in VALID_DAYS:
       day = input('Input day: ')

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        df['month'] = df['Start Time'].dt.month
        valid_month = VALID_MONTHS.index(month) + 1
        df = df[df['month'] == valid_month]
    if day != 'all':
        df['day'] = df['Start Time'].dt.day_name()
        df = df[df['day'] == day.title()]
    
    return df

def calculate_most_common(df, column_name):
    """
        Calculates the most common value of a column
        Args:
            (df)  Pandas DataFrame
            (str) column_name - name of the column need to be calculated
         Returns:
            (number) - Number of the most common value
    """
    return df[column_name].mode()[0]

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print(f"\nMost commonly used month: {calculate_most_common(df, 'month')}")

    # Display the most common day of week
    print(f"\nMost common day of week: {calculate_most_common(df, 'day')}")

    # Display the most common start hour
    print(f"\nMost common start hour: {calculate_most_common(df, 'hour')}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
   
    # Display most commonly used start station
    print(f"\n Most commonly used start station: {calculate_most_common(df, 'Start Station')}")

    # Display most commonly used end station
    print(f"\n Most commonly used end station: {calculate_most_common(df, 'End Station')}")

    # Display most frequent combination of start station and end station trip
    print(f"\n Most frequent combination of start station and end station trip: {df.groupby(['Start Station','End Station']).size().idxmax()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    # Display total travel time
    print(f"\nTotal travel time: {df['Trip Duration'].sum()}")

    # Display mean travel time
    print(f"\nMean travel time: {df['Trip Duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"\nCounts of user types: {df['User Type'].value_counts()}")

    try:
        # Display counts of gender
        print(f"\nCounts of gender: {df['Gender'].value_counts()}")
        
        # Display earliest, most recent, and most common year of birth
        print(f"\nEarliest year of birth: {df['Birth Year'].min()}")
        print(f"\nMost recent year of birth: {df['Birth Year'].max()}")
        print(f"\nMost common year of birth: {calculate_most_common(df, 'Birth Year')}")
    except KeyError:
        pass
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    # This loop will help user input choice if they want to see more raw data
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        index_row = 0
        size_data = 5
        # This loop will help user input choice if they want to see more raw data
        while True:
            see_raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')
            if index_row == 0:
                print(df.head(size_data))
                index_row += 1
                continue
            if see_raw_data != 'yes':
                break
            
            start_index = index_row * size_data
            end_index = (index_row + 1) * size_data
            if df.shape[0] - end_index > size_data:
                print(df.iloc[start_index : end_index])
                index_row += 1
            else:
                print(df.tail(df.shape[0] - end_index))
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
