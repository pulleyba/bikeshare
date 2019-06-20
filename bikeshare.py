#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:43:02 2018

@author: bpulley
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input("Choose Chicago, Washington D.C. (type washington) or New York City: ").lower()
        cities = ['chicago', 'new york city', 'washington']
        if city in cities:
            print('\nGood Choice')
            break
        else:
            print('\nNot a Valid Entry\nTry Again')
    while True:
        month = input("Enter Month: ").lower()
        months = ['january', 'february', 'march', 'april',
                  'may', 'june']
        if month in months:
            print('\nGood Choice')
            break
        else:
            print('\nNot a Valid Entry\nTry Again')
    while True:
        day = input("Enter Day of Week: ").lower()
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday']
        if day in days_of_week:
            print('\nGood Choice')
            break
        else:
            print('\nNot a Valid Entry\nTry Again')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day'] == day.title()]
    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]
    pop_month = df['month'].mode()[0]
    pop_day = df['day'].mode()[0]
    print("Popular Hour: {}\nPopular Month: {}\nPopular Day: {}.\n".format(
            pop_hour, pop_month, pop_day))
    print("\nThis took %0.4fs seconds." % (time.time() - start_time))
    print('-'*40)

    return pop_hour, pop_month, pop_day


def conv_trav_time(seconds):
    minutes = seconds//60
    remainder = seconds%60
    return ('{} minutes and {:0.2f} seconds').format(minutes,remainder)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    comm_start_stat = df['Start Station'].value_counts()
    comm_end_stat = df['End Station'].value_counts()
    print(comm_start_stat.idxmax())
    print("\nTop Five Most Popular Stations are:\n{}\n".format(comm_start_stat.head()))
    print(comm_end_stat.idxmax())
    print("\nTop Five Most Popular End Stations are:\n{}".format(comm_end_stat.head()))
    print("\nThis took %0.4fs seconds." % (time.time() - start_time))
    print('-'*40)

    return comm_start_stat, comm_end_stat


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    mean_travel_time = df['Trip Duration'].mean()
    total_travel_time = df['Trip Duration'].sum()
    print("Mean Travel Time is: {}\nTotal Travel Time is {}.".format(
            conv_trav_time(mean_travel_time),
          conv_trav_time(total_travel_time)))
    print("\nThis took %0.4fs seconds." % (time.time() - start_time))
    print('-'*40)

    return mean_travel_time, total_travel_time

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    while True:
        try:
            count_user_types = df['User Type'].value_counts()
        except KeyError:
            print("Sorry, no information available for select City")
        else:
             print("\nUser Types\nSubscribers: {}\nCustomers: {}".format(
            count_user_types[0], count_user_types[1]))
        try:
            count_gender = df['Gender'].value_counts()
        except KeyError:
            print("Sorry, no information available for select City")
        else:
            print("\nGender\nMale: {}\nFemale: {}".format(count_gender[0], count_gender[1]))
        try:
            birth_years = df['Birth Year'].value_counts()
        except KeyError:
            print("Sorry, no information available for select City")
        else:
            print("\nMost Common Birth Year is {:0.0f}".format(birth_years.idxmax()))
            print("\nMax Birth Year is {:0.0f}\nMinimum Birth Year is {:0.0f}".format(birth_years.index.max(),
                                                                            birth_years.index.min()))
        finally:
            print("\nThis took %0.4fs seconds." % (time.time() - start_time))
            print('-'*40)
            break

def display_data(df):
    while True:
        data_inquiry = input('\nWould you like to view raw data? Enter yes or no.\n')
        if data_inquiry.lower() != 'yes':
            break
        num = 5
        raw_data = df.head(num)
        print(raw_data)
        break
    while True:
        data_inquiry2 = input('\nWould you like to view more? Enter yes or no.\n')
        if data_inquiry2.lower() != 'yes':
            break
        num += 5
        raw_data = df.head(num)
        print(raw_data)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
