# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:35:56 2023

@author: tn93101
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = list(CITY_DATA.keys())
months = {'jan','feb','mar','apr','may','jun','all'} 
days = {'mon','tue','wed','thu','fri','sat','sun','all'}

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
    city = input("what city would you like to analyse: " + str(cities)+ " ?")
    city = city.lower()
    while city not in cities:
        print("This is not an opton, please try again")
        city = input("Please select one of these cities: chicago - new york city - washington?")        
        city = city.lower()
    print("Thanks you for selecting: " + city)             

#     # TO DO: get user input for month (all, january, february, ... , june)
       
    month = input("For what month would you like to analyse " + city + "jan - feb - mar - apr - may - jun - all? ")
    month = month.lower()
    while month not in months:
        month = input("Please select one of the available options: jan - feb - mar - apr - may - jun - (type: all for all months :")
        month = month.lower()
    print("You have selected : " + month)
        
#     # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    day = input("What day of the week is of your interest? mon - tue - wed - thu - fri - sat - sun - all :")
    day = day.lower()
    while day not in days:
        day = input("Please select a valid option, for all days of the week type all : ")
        day = day.lower()
    print("You have chosen : "+ day)
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
    df[['Start Time','End Time']] = df[['Start Time','End Time']].apply(pd.to_datetime, errors='coerce')
    df['month'] = df['Start Time'].dt.month_name().str.lower().str[:3]
    df['day']= df['Start Time'].dt.day_name().str.lower().str[:3]
    df['shour'] = df['Start Time'].dt.hour

    # adding the city name to the dataframe   
    df['city'] = city
    #adding missing columns to the dataset of washington to secure all sources and df's have same columns    
    if city == 'washington':
        df['Gender'] = "Not provided"
        df['Birth Year']= np.NaN
    df
    
    # assigning the filter values
    if month == "all":
        monthfilter = months
    else:
        monthfilter = month.split()
        
    if day == "all":
        dayfilter = days
    else:
        dayfilter = day.split()
    #applying the filters on the df       
    df = df[(df['month'].isin(monthfilter)) & (df['day'].isin(dayfilter))]   
    df   
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].value_counts().idxmax()
    print("Most common month is : " + common_month)
    # TO DO: display the most common day of week
    common_day = df['day'].value_counts().idxmax()
    print("Most common day is : " + common_day)
    # TO DO: display the most common start hour
    common_shour = df['shour'].value_counts().idxmax()
    print("Most comm start hour is : " + str(common_shour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_sstation = df['Start Station'].value_counts().idxmax()
    print("Most common Start Sation is :\n    " + common_sstation)

    # TO DO: display most commonly used end station
    common_estation = df['End Station'].value_counts().idxmax()
    print("Most common End Station is :\n    " + common_estation)
    # TO DO: display most frequent combination of start station and end station trip
    df['sestation']= df['Start Station']+ "_AND_"+df['End Station']
    common_sestation = df['sestation'].value_counts().idxmax()
    print("Most common Start-End station combination is :\n    " + common_sestation)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    t_traveltime = np.sum(df['Trip Duration'])
    converted_t_traveltime = time.strftime("%H:%M:%S", time.gmtime(t_traveltime))
    print("Total travel time is : "+ str(converted_t_traveltime))

    # TO DO: display mean travel time
    mean_traveltime = np.mean(df['Trip Duration'])
    converted_mean_traveltime = time.strftime("%H:%M:%S", time.gmtime(mean_traveltime))
    print("The mean of the travel time is :" + str(converted_mean_traveltime))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usertypes = df['User Type'].value_counts()
    print ("This is an overview of the user types : \n" + usertypes.to_string())
    # TO DO: Display counts of gender
    
    genders = df['Gender'].value_counts()
    print("\nThe gendersplit is : \n" + genders.to_string())
    # TO DO: Display earliest, most recent, and most common year of birth
    earliesty = df['Birth Year'].min().astype('int')
    #earliesty = earliesty.astype('int')
    print("\nEarliest birth year is :" + str(earliesty))
    recenty =df['Birth Year'].max().astype('int')
    print("Most recent Birth Year is : " + str(recenty))
    commony = df['Birth Year'].value_counts().idxmax().astype('int')
    print("Most common birth year is :"+ str(commony))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def stats(df):
    view_data = input("\nWould you like to view 5 rows of individual trip data? Enter yes or no\n").lower()
    start_loc = 0
    start_loc_to = 5
    while view_data == 'yes' and start_loc_to <= len(df) :
        dtset = df.iloc[start_loc:start_loc_to]
        print(dtset[['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year']])
        start_loc += 5
        start_loc_to += 5
        view_data = input("Do you wish to continue viewing more rows? Enter yes or no\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        time.sleep(3.0)
        station_stats(df)
        time.sleep(3.0)
        trip_duration_stats(df)
        time.sleep(3.0)
        if city =="washington":
            print("\nPlease note ! \nNo gender and Birth Year data available for washington")
            df['Birth Year'] = df['Birth Year'].fillna(0.0).astype(int) 
        user_stats(df)
        stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
 	main()
