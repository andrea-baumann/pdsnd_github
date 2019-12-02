import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('\nWould you like to see data for Chicago, New York, or Washington?\n')
            if city.lower() not in ['chicago', 'new york', 'washington']:
                print('That\'s not a valid input. Please type Chicago, New York, or Washington')
                continue
            else:
                print('Awesome, let\'s explore the bikeshare data in {}'.format(city.title()))
                break
        finally:
            print()

    # ask user input to add filters to the data (filter = 'no' represents "show all data")
    while True:
        try:
            filter = input('\nWould you like to filter the data? Enter yes or no\n')
            if filter.lower() not in ['yes', 'no']:
                print('That\'s not a valid input. Please type yes or no')
                continue
            else:
                break
        finally:
            print()

    # when filter = 'yes', ask user input for month, day, or both
    if filter.lower() == 'yes':
        while True:
            try:
                filter_date = input('\nWould you like to filter the data by month, day, or both?\n')
                if filter_date.lower() not in ['month', 'day', 'both']:
                    print('That\'s not a valid input. Please type month, day, or both')
                    continue
                else:
                    # get user input for specific filters:
                    # by month (january, february, ... , june)
                    if filter_date.lower() == 'month':
                        day = 'all'
                        while True:
                            try:
                                month = input('\nWhich month? January, February, March, April, May, or June?\n')
                                if month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
                                    print('That\'s not a valid input. Please type January, February, March, April, May, or June')
                                    continue
                                else:
                                    print('Great! We will make sure to filter the data by {}'.format(month.title()))
                                    break
                            finally:
                                print()
                    # by day of week (monday, tuesday, ... sunday)
                    elif filter_date.lower() == 'day':
                        month = 'all'
                        while True:
                            try:
                                day = input('\nWhich day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n')
                                if day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                                    print('That\'s not a valid input. Please type Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday')
                                    continue
                                else:
                                    print('Great! We will make sure to filter the data by {}'.format(day.title()))
                                    break
                            finally:
                                print()
                    # by both (month and day)
                    elif filter_date.lower() == 'both':
                        while True:
                            try:
                                month = input('\nWhich month? January, February, March, April, May, or June?\n')
                                if month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
                                    print('That\'s not a valid input. Please type January, February, March, April, May, or June')
                                    continue
                                else:
                                    #print('Great, we will make sure to filter by the month {}'.format(month.title()))
                                    while True:
                                        try:
                                            day = input('\nWhich day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n')
                                            if day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                                                print('That\'s not a valid input. Please type Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday')
                                                continue
                                            else:
                                                print('Great! We will make sure to filter the data by {} and {}'.format(month.title(), day.title()))
                                                break
                                        finally:
                                            print()
                                break
                            finally:
                                print()
                break
            finally:
                print()
    elif filter.lower() == 'no':
        day = 'all'
        month = 'all'

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # preparing time related data
    # step 1. convert Start Time from object data type to datatime64
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # step 2. extract the month from Start Time and add it to a new column
    df['month'] = df['Start Time'].dt.month # returns 1 for January ... 12 for December

    # step 3. extract the day of week from Start Time and add it to a new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name # returns Monday, ... Friday, etc

    # step 4. extract hour from Start Time and add it to a new column
    df['hour'] = df['Start Time'].dt.hour

    # applying filters
    print('Data loaded. Applying filters...')

    # filtering by month if applicable
    if month != 'all':
        # using the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filtering by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]
    popular_month = months[popular_month -1]
    print('Most popular month: ', popular_month.title())

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most popular day of week: ', popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['comb_station'] = df['Start Station'] + ', ' + df['End Station']
    popular_comb_stations = df['comb_station'].mode()[0]
    print('Most popular start and end stations: ', popular_comb_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total trip duration: {} sec'.format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average trip duration: {} sec'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print('Breakdown of user types: \n', user_types)
    print()

    # Display counts of gender
    if 'Gender' not in df.columns:
        print('Breakdown of gender: \n No data available')
    else:
        gender = df['Gender'].value_counts().to_frame()
        print('Breakdown of gender: \n', gender)
    print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('Breakdown of birth year: \n No data available')
    else:
        print('Earliest year of birth:\n', df['Birth Year'].min())
        print()
        print('Most recent year of birth:\n', df['Birth Year'].max())
        print()
        print('Most common year of birth:\n', df['Birth Year'].mode()[0])

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

        while True:
            try:
                raw_data = input('\nWould you like to see the data per user? Enter yes or no\n')
                if raw_data.lower() not in ['yes', 'no']:
                    print('not a valid answer, please type yes or no')
                    continue
                else:
                    lower_bound = 0
                    upper_bound = 5
                    while True:
                        if raw_data.lower() == 'yes':
                            print(df.iloc[lower_bound:upper_bound,:9])
                            lower_bound += 5
                            upper_bound += 5
                            while True:
                                try:
                                    raw_data = input('Would you like to continue viewing other 5 rows of data? (yes/no)')
                                    if raw_data.lower() not in ['yes', 'no']:
                                        print('not a valid answer, please type yes or no')
                                        continue
                                    else:
                                        break
                                finally:
                                    print()
                            continue
                        else:
                            break
                break
            finally:
                print()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Bye! :)')
            break


if __name__ == "__main__":
	main()
