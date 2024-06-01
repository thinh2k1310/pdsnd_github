import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_data = ['january', 'february', 'march', 'april', 'may', 'june']
day_data = ['monday', 'tuesday', 'wednesday', 'thursday',  'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city, month, day = '', '', ''
    while True:
        input_city = input('Which city do you want to analyze Chicago, New York, Washington ?\n').strip().lower()
        if input_city in CITY_DATA.keys():
            city = input_city
            break
        else:
            print('Wrong input! Please try again.')
    
    while True:
        input_month = input('Which month do you want to analyze: january, february, ... , june or all ?\n').strip().lower()
        months = month_data + ['all']
        if input_month in months:
            month = input_month
            break
        else:
            print('Wrong input! Please try again.')

    while True:
        input_day = input('Which day do you want to analyze: monday, tuesday, ... , sunday or all ?\n').strip().lower()
        days = day_data + ['all']
        if input_day in days:
            day = input_day
            break
        else:
            print('Wrong input! Please try again.')

    print('-'*40)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = month_data.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df

def display_five_rows(df):

    is_display = input("\nDo you want to see the first five raws of data? Yes or No:\n").strip().lower()
    if  is_display == 'yes':
        r = 0
        while True:
            print(df.iloc[r: r+5])
            r += 5
            more_row = input("\nDo you want to see more? Yes or No:\n").strip().lower()
            if more_row != 'yes':
                break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(common_month)
    print(f"The most common month is: {month_data[common_month-1]}.")

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"The most common day is: {common_day}.")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour  #create hour column by extracting it from start time
    common_hour = df['hour'].mode()[0]
    print("The most common hour is: {common_hour}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(f"The most common start station is: {common_start}.")

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(f"The most common end station is: {common_end}.")


    #  display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_path = df['combination'].mode()[0]
    print(f"The most frequent combination of start station and end station trip is: {common_path}.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {travel_time}.")

    #  display mean travel time
    avg_time = df['Trip Duration'].mean()
    print(f"The average travel time is: {avg_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("\nThe count of each user type: \n",user_type_count)

    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print("\nThe count of each gender :\n",gender_count)
    else:
        print("Gender feature is not available in this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        print(f"The most earliest year of birth is: {earliest_year}.")
        recent_year = df['Birth Year'].max()
        print(f"The most recent year of birth is: {recent_year}.")
        common_year = df['Birth Year'].mode()[0]
        print(f"The most common year of birth is: {common_year}.")
    else:
        print("Birth year information not available in this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_five_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
   main()
