import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago':
              '/Users/ammarsaad/Desktop/Project1/bikeshare-2/chicago.csv',
              'new york city':
              '/Users/ammarsaad/Desktop/Project1/bikeshare-2/new_york_city.csv',
              'washington':
              '/Users/ammarsaad/Desktop/Project1/bikeshare-2/washington.csv' }
MONTHS = np.array(['january', 'february', 'march', 'april', 'may', 'june',
                       'july', 'august', 'september', 'october', 'november',
                       'december'])
DAYS = np.array(['Sunday','Monday','Tuesday','Wednesday', 'Thursday','Friday','Saturday'])

def __get_valid_value(arr_options):
    """    get values which depends on array and needs validation """ 
    input_val = input().lower()
    while input_val not in arr_options:
        print("wrong input, try again")
        input_val = input().lower()

    return input_val    

def __get_day_filter():
    """    Asks user to specify a day to analyze. """
    print("which day? Please type your response as an integer (e.g. \
    1=Sunday)")
    day = int(input())
    while day > 7:  
        print("wrong input, try again")
        day = int(input())
                
    return day                  

def __get_month_filter():
    """    Asks user to specify a month to analyze. """
    print("which month? January ,February ,March, April, ..")
    month = __get_valid_value(MONTHS)
    return month    

def __get_date_filter():
    """    Asks user to specify a date filtration to analyze. """
    choices = np.array(["both", "month", "day", "none"])  
    print('Would you like to filter the data by month, day, both or \
not at all, Type "none" for no time filter ')      
    choice = __get_valid_value(choices)    
    return choice

def __get_city_filter():
    """    Asks user to specify a city to analyze. """
    cities = np.array(['chicago', 'new york city', 'washington'])
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    print('Whould you like to see data for chicago, new york city or\
 washington?')
    # get user input for city (chicago, new york city, washington). 
    city = __get_valid_value(cities)
    return city

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
              month filter
        (str) day - name of the day of week to filter by, or "all" to apply 
              no day filter
    """
    month = day = "all"
    city = __get_city_filter()
    date_filter = __get_date_filter()            

    if date_filter != "none":        

        if date_filter == "month" or "both":
            month = __get_month_filter()

        if date_filter == "day" or "both":
            day = __get_day_filter()

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
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day'] == DAYS[day-1].title()]
        
    return df


def time_stats(month, day, df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # display the most common month  
    if month == "all":
        df['month'] = df['Start Time'].dt.month
        popular_month = np.bincount(df['month']).argmax()
        print("most common month: ")
        print(popular_month)
    

    # display the most common day of week
    if day == "all":
        df['day'] = df['Start Time'].dt.day
        popular_day = np.bincount(df['day']).argmax()
        print("most common day of week: ")
        print(popular_day)
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    popular_hour = np.bincount(df['hour']).argmax()
    print("most common hour of day: ")
    print(popular_hour)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("most common used start station: ")
    print(popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("most common used end station: ")
    print(popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print("most frequent combination of start station and end station trip: ")
    print(popular_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time   
    print("total travel time: ")
    print(df["Trip Duration"].sum())

    # display mean travel time
    print("average travel time: ")
    print(df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()
    print(counts_user_types)

    # Display counts of gender
    try:
        counts_gender_types = df['Gender'].value_counts()
        print(counts_gender_types)

        # Display earliest, most recent, and most common year of birth
        print("earliest birthday: ")
        print(df['Birth Year'].min())
        print("most recent birthday: ")
        print(df['Birth Year'].max())
        print("most common birthday: ")
        print(df['Birth Year'].mode()[0])
    except KeyError:
        print("Sorry there's no gender or birth day year for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(month, day,df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        look_for_rows = input('\nWould you like to have a look on row data?\
 Enter yes or no.\n').lower()
        j = 0
        df = df.sort_values()
        while look_for_rows == "yes":
            print("\n", df.iloc[j:j+4])
            j += 4
            look_for_rows = input('\nWould you like to have a look on more row\
 data? Enter yes or no.\n').lower()
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

