'''
Author: Tianyi Luo
Date: 2014/07/14
'''
import numpy as np
import pandas as pd

# Create a float array from 2 to 1000000 with a step of 1
# These are flood return periods
rp2_1m = np.arange(2,1000000,1,dtype=float)

# Add 1.5 to the array above
rp1p5_1m = np.insert(rp2_1m,0,1.5)

# Convert return periods to probabilities
prob1p5_1m = 1/rp1p5_1m

# Reverse the probability array above in order to make it an
# increasing sequence which could be used as the x-axis 
prob1m_1p5 = prob1p5_1m[::-1]



######## CHART 1 Example 2 in Aqueduct Flood Risk Database Dictionary 072414.xlsx ########


# Load GDP_flood_risk_exposure_by_country.csv
GDP_country_path = r"C:\Users\tianyi.luo\Dropbox\WRI\Aqueduct\Flood Risk Tool\Wiredcraft\Data for Wiredcraft\GDP_flood_risk_exposure_by_country.csv"
GDP_country = pd.DataFrame.from_csv(GDP_country_path)

# We have damage data for return periods of 2, 5, 10, 25, 50, 100, 250, 500, 1000
# in our datasets, but for calculation purposes we need to add two more return periods,
# 1.5 at the beginning, and 1000000 at the end
rp_data_add = np.array([1.5, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 1000000])

# Reverse the probability array above in order to make it an
# increasing sequence which could be used as the x-axis  
rp_data_add_re = rp_data_add[::-1]

# Convert return periods to probabilities
prob_data = 1/rp_data_add_re

# Pick out current GDP damage levels for all 9 return periods for United States
# Data cells: J241:B241
GDP_data = GDP_country.values[239,0:9]

# Assuming a 1.5-year flood has the same damage level as a 2-year flood does. Add to the
# beginning of the array
GDP_data_add_temp = np.insert(GDP_data,0,GDP_country.values[239,0])

# Assuming a 1000000-year flood has the same damage level as a 1000-year flood does. Add
# to the end of the array
GDP_data_add = np.array(np.append(GDP_data_add_temp,GDP_country.values[239,8]),dtype=np.float)[::-1]

# Generate flood damage levels for all return periods using linear interpolation
GDP_interp = np.interp(prob1m_1p5,prob_data,GDP_data_add)

# Estimate total expected value using trapezoidal integration
GDP_trapz = np.trapz(GDP_interp,prob1m_1p5)

# Say an user puts in 10 as the current flood protection level for the United States.
# User inputs should be integers and between 2 to 1500
user_input = 10.0

# Convert return period to probability
user_input_prob = 1/user_input

# Find the index of the input probability in the all-probability array
user_input_prob_index = int(np.where(prob1m_1p5 == user_input_prob)[0])

# Create a new probability array which has probabilities from 0.000001 through the user
# input, in this case, 0.1
prob1m_1p5_new = prob1m_1p5[0:user_input_prob_index+1]

# Generate flood damage levels for new return periods using linear interpolation
GDP_interp_new = GDP_interp[0:user_input_prob_index+1]

# Estimate expected loss using trapezoidal integration
GDP_trapz_new = np.trapz(GDP_interp_new,prob1m_1p5_new)

# Calculate avoided loss by substracting expected loss from total expected value
GDP_loss_avoided = GDP_trapz - GDP_trapz_new

print GDP_trapz
print GDP_trapz_new
print GDP_loss_avoided
