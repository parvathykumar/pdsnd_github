import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    try:
        city = input('Enter the city name: ')
        assert(city in CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)
        valid_months = ['january', 'february', 'march', 'april', 'may',
                        'june', 'july', 'august', 'september', 'october',
                        'november', 'december', 'all']
        month = input('Enter the month: ')
        assert month.lower() in valid_months

    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Enter the day of the week: ')
        if day != 'all':
            assert 1 < int(day) <= 7

        print('-'*40)
        return city, month, day
    except AssertionError:
        return


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
    file_name = f'data/{city}.csv'
    df = pd.read_csv(file_name)
    if month != 'all':
        df = df.loc[(pd.to_datetime(df['Start Time']).dt.strftime('%B').apply(lambda x: x.lower()) == month)]
    if day != 'all':
        day = int(day) - 1
        df = df.loc[(pd.to_datetime(df['Start Time']).dt.strftime('%w') == str(day))]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    print(f"The most common month is: {df['Start Time'].dt.strftime('%B').value_counts().index[0]}")

    # display the most common day of week
    print(f"The most common day of the week is: {df['Start Time'].dt.strftime('%A').value_counts().index[0]}")

    # display the most common start hour
    print(f"The most common start hour is: {df['Start Time'].dt.strftime('%H').value_counts().index[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().index[0]
    print(f'The most commonly used start station is {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().index[0]
    print(f'The most commonly used end station is {common_end_station}')

    # display most frequent combination of start station and end station trip
    (comb_start, comb_end) = df.groupby(['Start Station', 'End Station']).size().nlargest(1).index[0]
    print(f'The most frequent combination of start & end stations is {comb_start} & {comb_end}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Time Taken'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    total_travel_time = df['Time Taken'].sum()
    print(f'The Total Travel Time is {total_travel_time.days} days, '
          f'{total_travel_time.seconds // 3600} hours, '
          f'{(total_travel_time.seconds//60)%60} minutes & '
          f'{round(((total_travel_time.seconds / 60) % 60 - (total_travel_time.seconds // 60) % 60) * 60)} seconds'
          )

    # display mean travel time
    mean_travel_time = df['Time Taken'].mean()
    print(f'The Mean Travel Time is {mean_travel_time.days} days, '
          f'{mean_travel_time.seconds // 3600} hours, '
          f'{(mean_travel_time.seconds//60)%60} minutes & '
          f'{round(((mean_travel_time.seconds/60)%60 - (mean_travel_time.seconds//60)%60)*60)} seconds'
          )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"The counts of User Types is: \n{df['User Type'].value_counts()}")

    # Display counts of gender
    print(f"The counts of Gender is: \n{df['Gender'].value_counts()}")

    # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
    Function that is invoked in the main block.
    The function accepts user-input, performs the necessary computation and prints the data.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
