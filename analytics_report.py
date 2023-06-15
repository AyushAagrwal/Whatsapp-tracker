from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import datetime
from db import con


def highlight_time_period(time_periods,title_string):
    angles = np.linspace(0, 2*pi, 1000)
    period_values = np.full(1000, np.nan)

    # set the values in the time periods to 0.9
    for x in time_periods:
        start_time = x[0]
        end_time = x[1]
        start_angle = 2*pi*(int(start_time[0:2])%12*3600 + int(start_time[3:5])*60 + int(start_time[6:]))/43200
        end_angle = 2*pi*(int(end_time[0:2])%12*3600 + int(end_time[3:5])*60 + int(end_time[6:]))/43200

        period_values[(angles >= start_angle) & (angles <= end_angle)] = 0.9

    ax = plt.subplot(111, polar=True)

    # plot the values as an area plot
    ax.fill_between(angles, 0, period_values, color='b', alpha=0.5)

    # suppress the radial labels
    plt.setp(ax.get_yticklabels(), visible=False)

    # set the circumference labels
    ax.set_xticks(np.linspace(0, 2*pi, 12, endpoint=False))
    ax.set_xticklabels(['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

    # make the labels go clockwise
    ax.set_theta_direction(-1)

    # place 12 at the top
    ax.set_theta_offset(pi/2.0)    

    # set the y-axis limit
    plt.ylim(0,1)
    
    plt.title(title_string)
    
    # remove circular gridlines
    ax.grid(False)
    
    plt.savefig('analytics.png',dpi=500)

def convert_to_12_hour(time):
    hours = int(time[:2])
    minutes = time[3:5]
    meridian = "AM"
    if hours >= 12:
        meridian = "PM"
    if hours == 0:
        hours = 12
    elif hours > 12:
        hours -= 12
    return f"{hours}:{minutes} {meridian}"


def format_date(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%B %d, %Y')


def generate_analytics():
    df = pd.read_sql("select * from info",con)

    data =[]
    for index in range(len(df)-1, -1, -1):
        if (df.iloc[index]['name']) == df.tail(1)['name'].reset_index()['name'][0]:
            data.append((df.iloc[index]['from_time'].split(' ')[-1],df.iloc[index]['to_time'].split(' ')[-1]))
        else:
            break

    title_string =  (df.tail(1)['name'].reset_index()['name'][0]).upper() + " for " + format_date(df.tail(1).reset_index()['from_time'][0].split(" ")[0]) +" Timing " + convert_to_12_hour(data[-1][-1]) + " from " + convert_to_12_hour(data[0][0])

    highlight_time_period(list(data),title_string)

    return title_string

