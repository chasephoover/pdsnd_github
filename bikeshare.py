"""V1.0
Created by: Chase Hoover
Updated: 8/9/2021 to push to Github
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("Input the city to analyze: Chicago, New York City, or Washington ").lower())
            if city not in ('chicago','new york city','washington'):
                print("City was input incorrectly, please retry")
            else:
                break
        except Exception as e:
            raise
            print('That\'s not a valid city!')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Input the month to analyze: Jan, Feb...Jun (or all to analyze all months) ")).lower()
            if month not in ('jan','feb','mar','apr','may','jun','all'):
                print("Month was input incorrectly, please retry")
            else:
                break
        except Exception as e:
            raise
            print('That\'s not a valid month!')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("Input the day to analyze: Mon, Tue, ... Sun (or all to analyze all days) ")).lower()
            if day not in ('mon','tue','wed','thu','fri','sat','sun','all'):
                print('Day was input incorrectly, please retry')
            else:
                break
        except Exception as e:
            raise
            print('That\'s not a valid day!')

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
    df = pd.read_csv(CITY_DATA[city])

    #convert start time col to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #creating month col
    df['Month'] = df['Start Time'].dt.month

    #creating day of week col
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #creating hour col
    df['Hour'] = df['Start Time'].dt.hour

    #apply filters if not set to "all" month or "all" day
    #convert int month to text month for check (e.g. jan == 1, feb == 2...)
    #creating a month dictionary to convert jan to 1, etc through june
    month_dict = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6}

    #if month is not set to all, then filter based on month using month_dict
    if month != "all":
        df = df[df['Month'] == month_dict[month]]

    #creating a day dictionary to convert mon to Monday, etc
    day_dict = {'mon':'Monday','tue':'Tuesday','wed':'Wednesday','thu':'Thursday',
        'fri':'Friday','sat':'Saturday','sun':'Sunday'}

    if day != "all":
        df = df[df['day_of_week'] == day_dict[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['Month'].mode()[0]

    #convert month number to month name
    month_dict_rev = {1:'January',2:'February',3:'March',4:'April',
        5:'May',6:'June'}

    print('Most common month from this dataset is {}.'.format(month_dict_rev[popular_month]))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most common day of week from this dataset is {}.'.format(popular_day))

    # TO DO: display the most common start hour
    popular_hour = df['Hour'].mode()[0]

    print('Most common hour from this dataset is {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('The most popular start station for this dataset is {}.'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('The most popular end station for this dataset is {}.'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_station_concat = (df['Start Station']+', '+df['End Station']).mode()[0]
    print('The most popular start-end station combo for this data set is {}.'.format(popular_station_concat))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_time_total = df['Trip Duration'].sum()
    print('Total travel time in seconds for this data set is {}.'.format(travel_time_total))

    # TO DO: display mean travel time
    travel_time_average = df['Trip Duration'].mean()
    print('Average travel time in seconds for this data set is {}.'.format(travel_time_average))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df.groupby(['User Type'])['User Type'].count()

    print('Below is the user type count for this dataset:\n{}'.format(user_type_count))

    # TO DO: Display counts of gender if city is not washington
    if city != 'washington':
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print('\nBelow is the gender count for this dataset:\n{}'.format(gender_count))
        # TO DO: Display earliest, most recent, and most common year of birth if city is not washington
        earliest_dob = df['Birth Year'].min()
        latest_dob = df['Birth Year'].max()
        common_dob = df['Birth Year'].mode()

        print('\nThe earliest birth year is {}.\nThe most recent birth year is {}.\nThe most common birth year is {}.'
            .format(int(earliest_dob), int(latest_dob), int(common_dob)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        #if city == Washington then no gender or birth city
        user_stats(df, city)

        raw = input('\nWould you like to see the raw data? Enter yes or no.\n')
        start = 0
        end = 5
        while raw.lower() == 'yes':
            print(df[start:end])
            raw = input('\nWould you like to see more raw data? Enter yes or no.\n')
            start += 5
            end += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
