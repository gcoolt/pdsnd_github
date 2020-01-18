import pandas as pd
import numpy as np
import time

def get_user():
    """
    Asks user for name to use later in program.
    Returns:
        (str) user_name - name of person
    """
    while True:
        user_name = input('Before we get started please enter your name:  ').strip().title()
        if len(user_name) > 0:
            print('-'*40)
            return user_name
        else:
            print('Invalid entry! Name must be greater than one character!')

def get_city(user_name):
    """
    Asks user to specify a city to analyze.
    Args:
        (str) user_name - name of user
    Returns:
        (str) city - name of the city to analyze
    """
    print('Hello ' + user_name + '! Let\'s explore some US bikeshare data!')
    print('-'*40)
    city_list = ['Chicago', 'New York City', 'Washington']
    while True:
        city = input('Please select the city you will like to view. (Chicago, New York City, Washington):  ').strip().title()
        if city in city_list:
            print('You have selected {} as your city.'.format(city))
            print('-'*40)
            return city
        else:
            print(user_name + ', please enter a valid selection!')

def get_month():
    """
    Asks user to specify a month to analyze.
    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    while True:
        month = input('Please select the month would you like to view or view select All. (January up to June):  ')\
            .strip().title()
        if month in months:
            if month != 'All':
                month = months.index(month) + 1
                print('You have selected {} as your month.'.format(months[month -1]))
                print('-'*40)
                return month
            else:
                month = 'All'
                print('You have selected to view all months.')
                print('-'*40)
                return month
        else:
            print('Please make a valid selection!')

def get_day():
    """
    Asks user to specify a day to analyze.
    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    day_of_week = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
    while True:
        day = input('Please select which Day of Week would you like to view or select All. (Sunday, Monday, etc..):  ')\
            .strip().title()
        if day in day_of_week:
            if day != 'All':
                dow = day
                print('You have selected {} as your day of week.'.format(day))
                print('-'*40)
                return day
            else:
                dow = 'All'
                print('You have selected to view all week days.')
                print('-'*40)
                return day
        else:
            print('Please make a valid selection!')

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
    CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'
    }
    # Import data and convert to datetime
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Create columns with additional date variables
    df['DOW'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month

    # Rename first column to User ID
    df.rename(columns={'Unnamed: 0': 'User_ID'}, inplace = True)

    # Filter dataframe to specified month(s)
    if month == 'All':
        df = df
    else:
        df = df[df['Month'] == month]

    # Filter dataframe to specified day(s)
    if day == 'All':
        df = df
    else:
        df = df[df['DOW'] == day]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
       (df) dataframe - dataframe of bikeshare data
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if len(df['Month'].unique()) > 1:
        popular_month = df['Month'].mode()[0]
        print('The most popular month is {}.'.format(months[popular_month -1]))

    # Display the most common day of week
    if len(df['DOW'].unique()) > 1:
        popular_DOW = df['DOW'].mode()[0]
        print('The most popular day of week is {}.'.format(popular_DOW))

    # Display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('The most popular hour of day is {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        (df) dataframe - dataframe of bikeshare data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most used starting station is {}.'.format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most used ending station is {}.'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Combo_Station'] = df['Start Station'] + df['End Station']
    popular_combo_station = df['Combo_Station'].mode()[0]
    print('The most common combination of stations is {}.'.format(popular_combo_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Args:
        (df) dataframe - dataframe of bikeshare data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()
    m, s = divmod(total_travel, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    print('The total trip duration is %d years %02d days %02d hrs %02d min %02d sec.' % (y,d,h,m,s))

    # Display mean travel time
    mean_travel = df['Trip Duration'].mean()
    m, s = divmod(mean_travel, 60)
    h, m = divmod(m, 60)
    print('The average trip duration is %d hrs %02d min %02d sec.' % (h, m, s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
    Args:
        (df) dataframe - dataframe of bikeshare data
        (str) city - name of the city to analyze
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The total count of users for this selection were:  ')
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city in ('Chicago', 'New York City'):
        print('The total count of bike riders by gender are:  ')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    current_year = 2018
    if city in ('Chicago', 'New York City'):
        print('\nThe oldest year of birth was {}, and that person is around {} year(s) old.'.
              format(int(df['Birth Year'].min()), int(current_year- df['Birth Year'].min())))
        print('The most recent year of birth was {}, and that person is is around {} year(s) old.'.
              format(int(df['Birth Year'].max()), int(current_year - df['Birth Year'].max())))
        print('The most common year of birth was {}.'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df, df_line):
    '''
    Displays five lines of data raw data for the user
    Args:
        (df) dataframe - dataframe of bikeshare data
        (int) df_line - current line of raw data
        (str) user_name - name of user
    '''
    while True:
        display = input('\nWould you like to view individual trip details? \nPlease enter Yes or No:  ')
        display = display.strip().title()
        if display == 'Yes':
            print(df.iloc[df_line:df_line + 5])
            df_line += 5
            return raw_data(df, df_line)
        elif display == 'No':
            return
        else:
            print('Please enter a valid selection!')

def main():
    # main function
    while True:
        df_line = 0
        user_name = get_user()
        city = get_city(user_name)
        month = get_month()
        day = get_day()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df, df_line)
        print('-'*40)
        restart = input('\n' + user_name + ' would you like to view data for another city or time frame?'
                        ' \nPlease enter Yes or No:  \n').title()
        if restart != 'Yes':
            break


if __name__ == "__main__":
    main()
