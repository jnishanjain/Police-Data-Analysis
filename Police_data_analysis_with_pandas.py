# -*- coding: utf-8 -*-
"""
Created on Wed May 12 11:27:48 2021

@author: ishan
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# Defining Print function for headings
def dash(x=''):
    '''
    This function can be used to seprate diffrent types of data on console.
    It take in an String as an input and prints it between multipe dashes
    
    Parameters
    ----------
    x : String
        Name of your heading.

    Returns
    -------
    None.

    '''
    print('')
    print(f"------------{x}------------")
    print('')

 
pd.set_option('Display.max_columns',15)

# Importing the Data set used in analysis
orignal_police_data = pd.read_csv("D:\Python Projects\police.csv")

# Performing deep copy 
police_data = orignal_police_data.copy()



# Checking shape of the data
dash('Shape of the Data')
print(police_data.shape)

'''
 Dropping the columns 'county_name' and 'states' as county name is empty 
 and all the states are same.
'''
police_data.drop(['county_name','state'],inplace=True,axis='columns')

# Examining data after we have dropped the column
dash('Examining Data')
print(police_data.head())
dash('Shape of the Data')
print(police_data.shape)

# Checking for missing values
dash('Missing Values')
print(police_data.isnull().sum())

'''
Now will drop all the missing values in the table based on our drivers_gender
'''
police_data.dropna(subset=['driver_gender'],inplace=True)

'''
Converting The stop_date and stop_time columns to data and time columns and 
concatinating them.
'''
police_data['stop_datetime'] = pd.to_datetime(
    police_data['stop_date'].str.cat(police_data['stop_time'],sep=' ')
    )

'''
Now we are exploring the Violation and driver gender columns  
and analysing if there is a relation between the same 
Many people belive that when a female is stopped for speeding they get off with a warning compared to males 
who get a citiation.
We will see if we can prove if this is true or not, based on the data we have.
'''

violation_female = police_data[(police_data['driver_gender'] =='F') & (police_data['violation']=='Speeding')]
violation_female['stop_outcome'].value_counts(normalize=True).plot(kind='barh')
plt.xlabel('Percentage')
plt.xscale('log')
plt.ylabel('Outcomes')
plt.title('Outcomes of Women Violations')
plt.show()

violation_male = police_data[(police_data['driver_gender'] =='M') & (police_data['violation']=='Speeding')]
violation_male['stop_outcome'].value_counts(normalize=True).plot(kind='barh')
plt.xlabel('Percentage')
plt.xscale('log')
plt.ylabel('Outcomes')
plt.title('Outcomes of Men Violations')
plt.show()
dash()
print("we are here")

'''
From the Plots we can say that women and men are both charged ciation 
regargless of there genders.

Next, we will use the time series columnin our data to see if the number of arrest made 
at night are lower or higher compared to the number of stops made in day.
'''

'''
NOTE : Here we will count time from 6:00 pm - 6:00 am as night and time from 6:00 am - 6:00 pm as day 
'''
day_time_arrests = police_data[(police_data['stop_datetime'].dt.hour >= 6 ) & (police_data['stop_datetime'].dt.hour <= 18 )]
night_time_arrests = police_data[(police_data['stop_datetime'].dt.hour <= 6 ) | (police_data['stop_datetime'].dt.hour >= 18 )]


# Extracting the Date time and gender columns 

day_time_arrests['stop_date']=pd.to_datetime(day_time_arrests['stop_date'])
new_day = day_time_arrests.groupby(day_time_arrests.stop_date.dt.year).is_arrested.sum().reset_index()
night_time_arrests['stop_date']=pd.to_datetime(night_time_arrests['stop_date'])
new_night = night_time_arrests.groupby(night_time_arrests.stop_date.dt.year).is_arrested.sum().reset_index()

# Plotting the no of arrests at night compared to teh numebr of arrest at day 


plt.plot(new_day.stop_date,new_day.is_arrested,label='Arrests at Day ')
plt.plot(new_night.stop_date,new_night.is_arrested,label='Arrests at Night')
plt.legend()
plt.title('Total Arrests')
plt.show()


'''
Now we will compare the arrest rate of Male and Female drivers at day and night.
We are filtiring the data of every year for both day and night , and male and female
'''

day_time_arrests = day_time_arrests.groupby([day_time_arrests.stop_date.dt.year,'driver_gender']).is_arrested.sum().reset_index()
day_time_arrests_female = day_time_arrests.loc[day_time_arrests.driver_gender=='F']
day_time_arrests_male = day_time_arrests.loc[day_time_arrests.driver_gender=='M']

night_time_arrests = night_time_arrests.groupby([night_time_arrests.stop_date.dt.year,'driver_gender']).is_arrested.sum().reset_index()
night_time_arrests_female = night_time_arrests.loc[night_time_arrests.driver_gender=='F']
night_time_arrests_male = night_time_arrests.loc[night_time_arrests.driver_gender=='M']


# PLOTTING THE DATA


fig , ax = plt.subplots(2,1,figsize=(15,15))
ax[0].plot(day_time_arrests_female.stop_date,day_time_arrests_female.is_arrested,label='Female')
ax[0].plot(day_time_arrests_male.stop_date,day_time_arrests_male.is_arrested,label='Male')
ax[0].legend()
ax[0].set_title('Arrests in day time ')

ax[1].plot(night_time_arrests_female.stop_date,night_time_arrests_female.is_arrested,label='Female')
ax[1].plot(night_time_arrests_male.stop_date,night_time_arrests_male.is_arrested,label='Male')
ax[1].legend()
ax[0].set_title('Arrests in night time ')
plt.suptitle('Male and female arrests')
plt.show()

'''
CONCLUSION:
    i. From plot 'Total Arests', the Arrests at night spiked around 2006 then were in a decline till 2008 and 
    have been lower to day's arrests since then.  
    ii.From plot 'Male and female arrests',the male arrest ratio is much higher compared to female 
    and that female arrest has been relatively constant since 2006 compared to male .
'''




