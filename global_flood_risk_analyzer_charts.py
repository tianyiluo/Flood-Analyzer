'''
Author: Tianyi Luo
Date: 2014/08/12
'''
import numpy as np
import pandas as pd

# Pick a country
input_country = 'UNITED STATES'

# Enter your current flood protection level (integer between 1.5 and 1000)
input_CFPL = 10.0



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
print "Chart 1"

# Load GDP_flood_risk_exposure_by_country.csv
GDP_country_path = r"C:\Users\tianyi.luo\Dropbox\WRI\Aqueduct\Flood Risk Tool\Wiredcraft\Data for Wiredcraft\GDP_flood_risk_exposure_by_country.csv"
GDP_country = pd.DataFrame.from_csv(GDP_country_path)
# Get country ID
countryID = int(np.where(GDP_country['spatial_unit_name'].values == input_country)[0])
# We have damage data for return periods of 2, 5, 10, 25, 50, 100, 250, 500, 1000
# in our datasets, but for calculation purposes we need to add two more return periods,
# 1.5 at the beginning, and 1000000 at the end
rp_data_add = np.array([1.5, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 1000000])

# Reverse the probability array above in order to make it an
# increasing sequence which could be used as the x-axis  
rp_data_add_re = rp_data_add[::-1]

# Convert return periods to probabilities
prob_data = 1/rp_data_add_re

# Pick out current GDP damage levels for all 9 return periods for the country
GDP_data = GDP_country.values[countryID,0:9]

# Assuming a 1.5-year flood has the same damage level as a 2-year flood does. Add to the
# beginning of the array
GDP_data_add_temp = np.insert(GDP_data,0,GDP_country.values[countryID,0])

# Assuming a 1000000-year flood has the same damage level as a 1000-year flood does. Add
# to the end of the array
GDP_data_add = np.array(np.append(GDP_data_add_temp,GDP_country.values[countryID,8]),dtype=np.float)[::-1]

# Generate flood damage levels for all return periods using linear interpolation
GDP_interp = np.interp(prob1m_1p5,prob_data,GDP_data_add)

# Estimate total expected value using trapezoidal integration
GDP_trapz = np.trapz(GDP_interp,prob1m_1p5)

# Convert return period to probability
input_CFPL_prob = 1/input_CFPL

# Find the index of the input probability in the all-probability array
input_CFPL_prob_index = int(np.where(prob1m_1p5 == input_CFPL_prob)[0])

# Create a new probability array which has probabilities from 0.000001 through the user
# input, in this case, 0.1
prob1m_1p5_new = prob1m_1p5[0:input_CFPL_prob_index+1]

# Generate flood damage levels for new return periods using linear interpolation
GDP_interp_new = GDP_interp[0:input_CFPL_prob_index+1]

# Estimate expected loss using trapezoidal integration
GDP_trapz_new = np.trapz(GDP_interp_new,prob1m_1p5_new)

# Calculate avoided loss by substracting expected loss from total expected value
GDP_loss_avoided = GDP_trapz - GDP_trapz_new

#print "Natural annual expected affected GDP", GDP_trapz
print "Annual Expected Affected GDP", GDP_trapz_new
print "Annual Avoided Affected GDP", GDP_loss_avoided

###################################### CHART 2 #########################################
print "Chart 2"
# "Optimistic (OPT)" (rcp45 + ssp2) 1
# "Business as Usual(BAU)" (rcp85 + ssp2) 2
# "Pessimistic (PES)" (rcp85 + ssp3) 3

# Say user chooses "Business as Usual(BAU)" Scenario (rcp8p5 + ssp2) 2
FutureScenario = 2

if FutureScenario == 1:
    Fcolstart = 9
    Fcolend = 18
    Ccolstart = 36
    Ccolend = 45
    Scolstart = 54
    Scolend = 63
    print "Future Scenario: Optimistic"
elif FutureScenario == 2:
    Fcolstart = 18
    Fcolend = 27
    Ccolstart = 45
    Ccolend = 54
    Scolstart = 54
    Scolend = 63
    print "Future Scenario: Business as Usual"
elif FutureScenario == 3:
    Fcolstart = 27
    Fcolend = 36
    Ccolstart = 45
    Ccolend = 54
    Scolstart = 63
    Scolend = 72
    print "Future Scenario: Pessimistic"

# BAU flood risk (similar naming convention and same methodology as current flood risk)
GDP_data_BAU = GDP_country.values[countryID,Fcolstart:Fcolend]
GDP_data_BAU_add_temp = np.insert(GDP_data_BAU,0,GDP_country.values[countryID,Fcolstart])
GDP_data_BAU_add = np.array(np.append(GDP_data_BAU_add_temp,GDP_country.values[countryID,(Fcolend-1)]),dtype=np.float)[::-1]
GDP_BAU_interp = np.interp(prob1m_1p5,prob_data,GDP_data_BAU_add)


# Climate change only flood risk (similar naming convention and same methodology as current flood risk)
# Note: because user chose BAU which consists of rcp8p5 and ssp2, so here we are using columns of -
# climate_change_only_XXyearflood_base_rcp8p5 
GDP_data_CC = GDP_country.values[countryID,Ccolstart:Ccolend]
GDP_data_CC_add_temp = np.insert(GDP_data_CC,0,GDP_country.values[countryID,Ccolstart])
GDP_data_CC_add = np.array(np.append(GDP_data_CC_add_temp,GDP_country.values[countryID,(Ccolend-1)]),dtype=np.float)[::-1]
GDP_CC_interp = np.interp(prob1m_1p5,prob_data,GDP_data_CC_add)


# Socio-economic change only flood risk (similar naming convention and same methodology as current flood risk)
# Note: because user chose BAU which consists of rcp8p5 and ssp2, so here we are using columns of
# socio_econ_change_only_XXyearflood_ssp2_historical 
GDP_data_SEC = GDP_country.values[countryID,Scolstart:Scolend]
GDP_data_SEC_add_temp = np.insert(GDP_data_SEC,0,GDP_country.values[countryID,Scolstart])
GDP_data_SEC_add = np.array(np.append(GDP_data_SEC_add_temp,GDP_country.values[countryID,(Scolend-1)]),dtype=np.float)[::-1]
GDP_SEC_interp = np.interp(prob1m_1p5,prob_data,GDP_data_SEC_add)

# Essentially, what I wanted to do from line 156 through 183 is to, 1) find the damage of the magnitude of flood
# that is currently protected (use current flood protection level as the x-value and the current loss - probability curve
# to locate the y-value which is the damage), 2) find what the magnitude of flood that will cause the same damage is in
# the future (use the damage as the y-value and the BAU loss - probability curve to locate the x-value which is the
# magnitude of the future flood event), and 3) calculate estimated 2030 expected annual affected GDP.

# define a initial value of the difference
num_comp = long(100000000000000000)
# define a initial value of the index of the found future flood magnitude
input_FFPL_prob_index = int(100000000000000000)
# I am simply doing enumeration here with the for loop, trying to find the closest match by comparing all the differences
# between magnitude of future flood damage and magnitude of the current.
# I know that this method is NOT computationally efficient, feel free to optimize the algorithm
for i in range(999999):
    if abs(GDP_BAU_interp[i] - GDP_interp[input_CFPL_prob_index]) <= num_comp:
        num_comp = abs(GDP_BAU_interp[i] - GDP_interp[input_CFPL_prob_index])
        input_FFPL_prob_index = i
# New probability array which has probabilities from 0.000001 through the future flood protection level
prob1m_1p5_BAU_new = prob1m_1p5[0:input_FFPL_prob_index+1]
# BAU flood damage levels for new return periods using linear interpolation
GDP_BAU_interp_new = GDP_BAU_interp[0:input_FFPL_prob_index+1]
# Estimate BAU expected affected gdp using trapezoidal integration
GDP_BAU_trapz_new = np.trapz(GDP_BAU_interp_new,prob1m_1p5_BAU_new)

# Similar as above, calculating climate change only expected affected gdp
num_comp = long(100000000000000000)
input_FFPL_prob_index = int(100000000000000000)
for i in range(999999):
    if abs(GDP_CC_interp[i] - GDP_interp[input_CFPL_prob_index]) <= num_comp:
        num_comp = abs(GDP_CC_interp[i] - GDP_interp[input_CFPL_prob_index])
        input_FFPL_prob_index = i
prob1m_1p5_CC_new = prob1m_1p5[0:input_FFPL_prob_index+1]
GDP_CC_interp_new = GDP_CC_interp[0:input_FFPL_prob_index+1]
GDP_CC_trapz_new = np.trapz(GDP_CC_interp_new,prob1m_1p5_CC_new)

# Similar as above, calculating socio-econonic change only expected affected gdp
num_comp = long(100000000000000000)
input_FFPL_prob_index = int(100000000000000000)
for i in range(999999):
    if abs(GDP_SEC_interp[i] - GDP_interp[input_CFPL_prob_index]) <= num_comp:
        num_comp = abs(GDP_SEC_interp[i] - GDP_interp[input_CFPL_prob_index])
        input_FFPL_prob_index = i
prob1m_1p5_SEC_new = prob1m_1p5[0:input_FFPL_prob_index+1]
GDP_SEC_interp_new = GDP_SEC_interp[0:input_FFPL_prob_index+1]
GDP_SEC_trapz_new = np.trapz(GDP_SEC_interp_new,prob1m_1p5_SEC_new)


# Theoretically, there are 8 possible results (2 options * 2 options * 2 options). Below works as the
# switch-case function.
# For example, BAU risk is greater than current risk, socio-econ change only risk is greater than current risk,
# but climate change only risk is less than current risk. In this case, we assume that climate change contributes
# nothing to the overall increase of risk, and socio-econ change is responsible for all the increase.
if GDP_BAU_trapz_new > GDP_trapz_new:
    if GDP_SEC_trapz_new > GDP_trapz_new:
        if GDP_CC_trapz_new > GDP_trapz_new:
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Increase due to socio-economic change", (GDP_SEC_trapz_new/(GDP_CC_trapz_new+GDP_SEC_trapz_new))*(GDP_BAU_trapz_new - GDP_trapz_new)
            print "Increase due to climate change", (GDP_CC_trapz_new/(GDP_CC_trapz_new+GDP_SEC_trapz_new))*(GDP_BAU_trapz_new - GDP_trapz_new)
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new
        else:
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Increase due to socio-economic change", (GDP_BAU_trapz_new - GDP_trapz_new)
            print "Increase due to climate change", 0
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new
    else:
        if GDP_CC_trapz_new > GDP_trapz_new:
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Increase due to socio-economic change", 0
            print "Increase due to climate change", (GDP_BAU_trapz_new - GDP_trapz_new)
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new
        else:
            print "Warning"
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Increase due to socio-economic change", 0
            print "Increase due to climate change", 0
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new
else:
    if GDP_SEC_trapz_new > GDP_trapz_new:
        if GDP_CC_trapz_new > GDP_trapz_new:
            print "Warning"
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Decrease due to socio-economic change", 0
            print "Decrease due to climate change", 0
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new
        else:
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Decrease due to socio-economic change", 0
            print "Decrease due to climate change", (GDP_trapz_new - GDP_BAU_trapz_new)
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new
    else:
        if GDP_CC_trapz_new > GDP_trapz_new:
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Decrease due to socio-economic change", (GDP_trapz_new - GDP_BAU_trapz_new)
            print "Decrease due to climate change", 0
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new
        else:
            print "Current Annual Expected Affected GDP", GDP_trapz_new
            print "Decrease due to socio-economic change", (GDP_SEC_trapz_new/(GDP_CC_trapz_new+GDP_SEC_trapz_new))*(GDP_trapz_new - GDP_BAU_trapz_new)
            print "Decrease due to climate change", (GDP_CC_trapz_new/(GDP_CC_trapz_new+GDP_SEC_trapz_new))*(GDP_trapz_new - GDP_BAU_trapz_new)
            print "2030 Annual Expected Affected GDP", GDP_BAU_trapz_new



