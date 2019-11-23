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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    isValid = False
    city_list= ['chicago', 'new york city', 'washington']
    month_list= ['all','january', 'february', 'march','april','may','june']
    days_list= ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while isValid == False:
        city=input("Hello enter a valid city name(Chicago,New York city or Washington): ")
        response=input("Would you like to filter the data by month, day,both or not at all type none for not at all: ")
        if response.lower() == 'month':
            month=input("Enter the name of the month to filter by (January, February, March, April, May, or June), or 'all' to apply no month filter : ")
            day='all'

        elif response.lower() == 'day':
            day=input("Enter the name of the day of week to filter by (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday), or 'all' to apply no day filter: ")
            month = 'all'

        elif response.lower() == 'both':
            month=input("Enter the name of the month to filter by (January, February, March, April, May, or June), or 'all' to apply no month filter : ")
            day=input("Enter the name of the day of week to filter by (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday), or 'all' to apply no day filter: ")
        elif response.lower()=='none':
            month,day ='all','all'
        else:
            print("invalid input")

        if (city.lower() in city_list and month.lower() in month_list) or (city.lower() in city_list and day.lower() in days_list):
            isValid = True
        else:
            print('One or more of the inputs is not a valid entry. Please give valid inputs')

    # get user input for month (all, january, february, ... , june)


    # get user input for day of week (all, monday, tuesday, ... sunday)


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
     #remember to change this
    df= pd.read_csv('bikeshare-2/'+CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #making a month column and a day of the week column
    df['month']=df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filterning for the months
    if month.lower() != 'all':
        month_list= ['january', 'february', 'march','april','may','june']
        month=month_list.index(month.lower()) + 1
        df = df[df['month'] == month]
    #Filtering for the day
    if day.lower() != 'all':
        df= df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    month_list= ['january', 'february', 'march','april','may','june']

    # display the most common month
    most_common_month= df['month'].mode()[0]
    most_common_month=month_list[most_common_month-1]
    print("The most common month is {}".format(most_common_month.title()))
    
    # display the most common day of week
    most_common_day= df['day_of_week'].mode()[0]
    print("The most common day of the week is {}".format(most_common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most common hour is {}".format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startStation=df['Start Station'].mode()[0]
    print("The most commonly used Start Station is: {}".format(common_startStation))

    # display most commonly used end station
    common_EndStation=df['End Station'].mode()[0]
    print("The most commonly used End Station is: {}".format(common_EndStation))
    # display most frequent combination of start station and end station trip
    StationsDF=df[df.columns[4:6]]
    StationsDF=StationsDF.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print("The most freqeuent combination of Start station and End station trip is {} and {} ".format(StationsDF.index[0][0],StationsDF.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time was {}".format(float(df['Trip Duration'].sum())))


    # display mean travel time
    print("The average travel time was {}".format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts=df.groupby(['User Type']).size().sort_values(ascending=False)
    print("Here are the different types of users:")
    if 'Subscriber' in user_counts:
        print("For Subscriber users there are {} people".format(user_counts[0]))
    if 'Customer' in user_counts:
        print("For Customer users there are {} people".format(user_counts[1]))
    if 'Dependent' in user_counts:
        print("For Dependent users there are {} people".format(user_counts[2]))
    print('\n')
    # Display counts of gender
    gender_count=df.groupby(['Gender']).size().sort_values(ascending=False)
    print('"Here is the gender count: ')
    print("There is a total of {} people that are {}".format(gender_count[0],gender_count.index[0]))
    print("There is a total of {} people that are {}".format(gender_count[1],gender_count.index[1]))
    print('\n')
    # Display earliest, most recent, and most common year of birth
    print("The oldest person was born in {}".format(int(df['Birth Year'].min())))
    print("The youngest person was born in {}".format(int(df['Birth Year'].max())))
    print("The most common birth year was {}".format(int(df['Birth Year'].mean())))


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
            print(df.head().values)
            iterate=input("Would you like to see more individual trip data? Type yes or no: ")
            df.drop(df.index[:5], inplace=True)
            if iterate.lower() !='yes':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
