from google.protobuf import symbol_database
from pydeck.bindings import map_styles
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import altair as alt
import numpy as np
import folium
import csv
import pydeck as pdk
#image = Image.open('logo.png')
#st.image(image, width=300)
#st.image('logo.png', width=150)

st.set_page_config(
        page_title="Earth AI",
)

st.title("EarthAI's CLIMATE CHANGE HOME TRACKER")
st.markdown("""
A Webapp that every Household could use to get an idea of what will happen
to climate change if everyone on earth lives like you. 

""")
st.markdown("""
Open the side panel and change Criterion to see the effect on Climate Change and CO2 emissions.

""")

st.sidebar.header('Personal Details')

file_country = open('country_names.csv', 'r')
country_list=[]
reader = csv.reader(file_country)
for i in reader:
    i =str(i)
    i = i[2:]
    i = i[:-2]
    country_list.append(i)
file_country.close()

file_us_city = open('us_city_names.csv', 'r')
us_city_list=[]
reader = csv.reader(file_us_city)
for i in reader:
    i =str(i)
    i = i[2:]
    i = i[:-2]
    us_city_list.append(i)

file_us_city.close()

country = st.sidebar.selectbox('Select Your Country', country_list)
if country == 'United States':
    city = st.sidebar.selectbox('Select your State in US',us_city_list)
    country = city

col1, mid, col2 = st.beta_columns([1,10,20])
with col1:
    st.write('')
with col2:
    st.write("""
    Made by Arnav Suman
    """)

#'''st.markdown(
#    """<a style='display: block; text-align: center;' href="https://github.com/arnavcool123/CLIMATE-CHANGE-HOME-TRACKER.git">Click to see Code on Github</a>
#    """,
#    unsafe_allow_html=True,
#)

st.sidebar.header('ENERGY SUPPLY')

#base_unit = st.sidebar.selectbox('Select base currency', currency_list)
#given_value = st.sidebar.slider('Enter value', 50,100,75)
#symbol_unit = st.sidebar.selectbox('Select target Currency', currency_list)


coal = st.sidebar.selectbox('Taxation on use of Coal Sources',['Status Quo','Very Highly Taxed', 'Highly Taxed', 'Taxed', 'Subsidized'])
renewables = st.sidebar.selectbox('Taxation on Renewable Sources', [ 'Status Quo', 'Taxed', 'Subsidized', 'Highly Subsidized'])
nuclear = st.sidebar.selectbox('Taxation on Nuclear Sources', [ 'Status Quo', 'Highly Taxed', 'Taxed', 'Subsidized', 'Highly Subsidized'])
oil = st.sidebar.selectbox('Taxation on Oil Sources', [ 'Status Quo', 'Very Highly Taxed', 'Highly Taxed', 'Taxed', 'Subsidized'])
natural_gas = st.sidebar.selectbox('Taxation on Natural Gas Sources', [ 'Status Quo', 'Very Highly Taxed', 'Highly Taxed', 'Taxed', 'Subsidized'])
new_zero_carbon = st.sidebar.selectbox('No Emission Power Supply Technology', ['Status Quo','Breakthrough', 'Huge Breakthrough'])
bioenergy =  st.sidebar.selectbox('Taxation on Biological Sources like Food Waste, Agricultural Waste, etc', [ 'Status Quo', 'Highly Taxed', 'Taxed', 'Subsidized', 'Highly Subsidized'])
carbon_price = st.sidebar.selectbox('Global Carbon Price', ['Status Quo','Medium', 'High', 'Very High'])



st.sidebar.header('TRANSPORT')

energy_efficiency_transport = st.sidebar.selectbox('Energy Efficiency of Transport vehicles', ['Status Quo', 'Discouraged', 'Increased', 'Highly Increased'])
electrification_transport = st.sidebar.selectbox('Electrification of Transport vehicles', ['Status Quo', 'Incentivized', 'Highly Incentivized'])


st.sidebar.header('BUILDINGS AND INDUSTRY')

energy_efficiency = st.sidebar.selectbox('Efficiency of Home and Industrial Appliances', ['Status Quo', 'Discouraged', 'Increased', 'Highly Increased'])
electrification = st.sidebar.selectbox('Use of Electricity', ['Status Quo', 'Incentivized', 'Highly Incentivized'])


st.sidebar.header('PERSONAL HABITS')

vegan = st.sidebar.selectbox('Veganism', ['Status Quo', 'Highly Promoted', 'Negatively Promoted'])
cars = st.sidebar.selectbox('No. of Cars in Family', [2,1,3,0])
public_transport = st.sidebar.selectbox('Public Transport Use', ['Status Quo', 'Used oftenly', 'Never Used'])
politics = st.sidebar.selectbox('Political Attitude on Climate Change', ['Status Quo', 'Negative', 'Positive'])
awareness = st.sidebar.selectbox('Public Awareness on Climate Change', ['Status Quo', 'Negative', 'Positive'])


st.sidebar.header('GROWTH')

population = st.sidebar.selectbox('Population Growth', ['Status Quo', 'Lowest Growth', "Low Growth", "High growth", "Highest Growth"])
economic_growth = st.sidebar.selectbox('Economic growth', ['Status Quo', "Low growth", "High Growth"])

st.sidebar.header('LAND AND INDUSTRY EMISSIONS')

deforestation = st.sidebar.selectbox('Deforestation', ['Status Quo', 'highly Reduced', 'Moderately Reduced', 'Increased'])
methane = st.sidebar.selectbox('Methane & Other Gases', ['Status Quo', 'highly Reduced', 'Moderately Reduced', 'Increased'])

st.sidebar.header('CARBON REMOVAL')

afforestation = st.sidebar.selectbox('Aforestation', ['Status Quo', 'low growth', 'medium growth', 'high growth'])
technological = st.sidebar.selectbox('Technological Advances to remove carbon', ['Status Quo', 'Low Growth', 'Medium Growth', 'High Growth'])

co2_emission_gigatons = {
    2000 : 43.53,     2001:	44.31,    2002:	45.27,    2003:	45.64,    2004:	46.53,	
    2005:	47.39,	  2006:	48.75,    2007:	48.89,    2008:	50.00,	
    2009:	51.10,    2010:	51.36,	    2011:	51.96,	    2012:	52.63,	
    2013:	53.06,    2014:	53.88,    2015:	54.75,    2016:	55.30,	
    2017:	55.83,    2018:	56.38,    2019:	56.90,    2020:	57.38,
    2021:	57.32,	  2022:	57.05,    2023:	57.55,    2024:	58.16,
    2025:	58.76,    2026:	59.35,    2027:	59.91,    2028:	60.47,
    2029:	61.02,    2030:	61.57,    2031:	62.11,    2032:	62.64,    2033:	63.17,    2034:	63.69,	    2035:	64.20,	
    2036:	64.71,    2037:	65.21,	    2038:	65.70,	
    2039:	66.19,	  2040:	66.68,	    2041:	67.17,	    2042:   67.66,
    2043:	68.15,    2044:	68.65,    2045:	69.14,    2046:	69.63,
    2047:	70.12,    2048:	70.61,	    2049:	71.10,	    2050:	71.59,	
    2051:	72.08,	  2052:	72.57,    2053:	73.06,    2054:	73.54,   2055:	74.02,    2056:	74.49,    2057:	74.97,	
    2058:	75.44,    2059:	75.90,	    2060:	76.36,	    2061:	76.82,	
    2062:	77.28,	  2063:	77.73,    2064:	78.18,	    2065:	78.63,	
    2066:	79.07,	  2067:	79.51,    2068:	79.95,	    2069:	80.39,	
    2070:	80.82,	  2071:	81.25,	    2072:	81.68,    2073:	82.11,	
    2074:	82.53,	  2075:	82.95,    2076:	83.38,	    2077:	83.80,	
    2078:	84.21,	  2079:	84.63,	    2080:	85.05,	
    2081:	85.46,	    2082:	85.88,    2083:	86.29,
    2084:	86.70,    2085:	87.12,	    2086:	87.54,	
    2087:	87.95,	    2088:	88.37,	    2089:	88.79,	
    2090:	89.21,	    2091:	89.64,	    2092:	90.07,	    2093:	90.50,	
    2094:	90.93,	    2095:	91.37,    2096:	91.81,	    2097:	92.25,	    2098:	92.69,	
    2099:	93.13,	    2100:	93.58,	
    }

year = list(co2_emission_gigatons.keys())
co2_baseline = list(co2_emission_gigatons.values())
co2_new = co2_baseline

temp = 3.6


if coal =='Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
elif coal == 'Very Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (0.8788)
        x.append(i)
    co2_new = x 
    temp += -0.2

elif coal == 'Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9430)
        x.append(i)
    co2_new = x 
    temp += -0.1 

elif coal == 'Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9765)
        x.append(i)
    co2_new = x 
    temp += -0.05

elif coal == 'Subsidized':
    x = []
    for i in co2_new:
        i = i * (1.0333)
        x.append(i)
    co2_new = x 
    temp += 0.1

# RENEWABLES       

if renewables =='Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif renewables =='Taxed':
    x = []
    for i in co2_new:
        i = i * (1.0684)
        x.append(i)
    co2_new = x
    temp += 0.1

  
elif renewables =='Subsidized':
    x = []
    for i in co2_new:
        i = i * (0.9346)
        x.append(i)
    co2_new = x
    temp += -0.1

   
elif renewables =='Highly Subsidized':
    x = []
    for i in co2_new:
        i = i * (0.8900)
        x.append(i)
    co2_new = x
    temp += -0.2
   


if nuclear =='Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif nuclear =='Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (1.0102)
        x.append(i)
    co2_new = x
    temp += 0.0

elif nuclear =='Taxed':
    x = []
    for i in co2_new:
        i = i * (1.0050)
        x.append(i)
    co2_new = x
    temp += 0.0

elif nuclear =='Subsidized':
    x = []
    for i in co2_new:
        i = i * (0.9900)
        x.append(i)
    co2_new = x
    temp += 0.0

elif nuclear =='Highly Subsidized':
    x = []
    for i in co2_new:
        i = i * (0.9318)
        x.append(i)
    co2_new = x
    temp += -0.1



if oil =='Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0

elif oil =='Very Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9247)
        x.append(i)
    co2_new = x
    temp += -0.1
    
elif oil =='Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9596)
        x.append(i)
    co2_new = x
    temp += -0.1
    
elif oil =='Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9950)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif oil =='Subsidized':
    x = []
    for i in co2_new:
        i = i * (1.0090)
        x.append(i)
    co2_new = x
    temp += 0.005
    
  
 


if natural_gas =='Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0 
    
elif natural_gas =='Very Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9411)
        x.append(i)
    co2_new = x
    temp += -0.1
    
elif natural_gas =='Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9677)
        x.append(i)
    co2_new = x
    temp += -0.1
    
elif natural_gas =='Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9899)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif natural_gas =='Subsidized':
    x = []
    for i in co2_new:
        i = i * (1.0080)
        x.append(i)
    co2_new = x 
    temp += 0.0
    
if new_zero_carbon =='Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif new_zero_carbon =='Breakthrough':
    x = []
    for i in co2_new:
        i = i * (0.8783)
        x.append(i)
    co2_new = x 
    temp += -0.1
    
elif new_zero_carbon =='Huge Breakthrough':
    x = []
    for i in co2_new:
        i = i * (0.8411)
        x.append(i)
    co2_new = x 
    temp += -0.2
    

if bioenergy =='Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif bioenergy =='Highly Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9600)
        x.append(i)
    co2_new = x
    temp += -0.005
    
elif bioenergy =='Taxed':
    x = []
    for i in co2_new:
        i = i * (0.9899)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif bioenergy =='Subsidized':
    x = []
    for i in co2_new:
        i = i * (1.0108)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif bioenergy =='Highly Subsidized':
    x = []
    for i in co2_new:
        i = i * (1.0199)
        x.append(i)
    co2_new = x 
    temp += 0.005
    
if carbon_price  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif carbon_price  == 'Low':
    x = []
    for i in co2_new:
        i = i * (0.9122)
        x.append(i)
    co2_new = x  
    temp += -0.005

elif carbon_price  == 'Medium':
    x = []
    for i in co2_new:
        i = i * (0.7393)
        x.append(i)
    co2_new = x  
    temp += -0.1
     
elif carbon_price  == 'High':
    x = []
    for i in co2_new:
        i = i * (0.6232)
        x.append(i)
    co2_new = x 
    temp += -0.3
     
elif carbon_price  == 'Very High':
    x = []
    for i in co2_new:
        i = i * (0.4567)
        x.append(i)
    co2_new = x 
    temp += -0.5


if energy_efficiency  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      
elif energy_efficiency  == 'Discouraged':
    x = []
    for i in co2_new:
        i = i * (1.2674)
        x.append(i)
    co2_new = x  
    temp += 0.1
     
elif energy_efficiency  == 'Increased':
    x = []
    for i in co2_new:
        i = i * (0.8698)
        x.append(i)
    co2_new = x 
    temp += -0.1
     
elif energy_efficiency  == 'Highly Increased':
    x = []
    for i in co2_new:
        i = i * (0.8365)
        x.append(i)
    co2_new = x  
    temp += -0.15
     
 


if electrification_transport  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x  
    temp += 0.0
     
elif electrification_transport  == 'Incentivized':
    x = []
    for i in co2_new:
        i = i * (0.9722)
        x.append(i)
    co2_new = x  
    temp += 0.0
     
elif electrification_transport  == 'Highly Incentivized':
    x = []
    for i in co2_new:
        i = i * (0.9091)
        x.append(i)
    co2_new = x 
    temp += -0.1
     
 

if electrification  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      
elif electrification  == 'Incentivized':
    x = []
    for i in co2_new:
        i = i * (0.9358)
        x.append(i)
    co2_new = x
    temp += -0.1
       
elif electrification  == 'Highly Incentivized':
    x = []
    for i in co2_new:
        i = i * (0.7956)
        x.append(i)
    co2_new = x 
    temp += -0.2
     
if energy_efficiency  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      
elif energy_efficiency  == 'Discouraged':
    x = []
    for i in co2_new:
        i = i * (1.7236)
        x.append(i)
    co2_new = x 
    temp += 0.2
      
elif energy_efficiency  == 'Increased':
    x = []
    for i in co2_new:
        i = i * (0.7905)
        x.append(i)
    co2_new = x
    temp += -0.1
      
elif energy_efficiency  == 'Highly Increased':
    x = []
    for i in co2_new:
        i = i * (0.6585)
        x.append(i)
    co2_new = x  
    temp += -0.2
     


if vegan  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      
elif vegan  == 'Highly Promoted':
    x = []
    for i in co2_new:
        i = i * (0.6999)
        x.append(i)
    co2_new = x
    temp += -0.2
       
elif vegan  == 'Negatively Promoted':
    x = []
    for i in co2_new:
        i = i * (1.2050)
        x.append(i)
    co2_new = x 
    temp += 0.1
     

if cars  == 1:
    x = []
    for i in co2_new:
        i = i * (0.8888)
        x.append(i)
    co2_new = x 
    temp += -0.07
      
elif cars  == 2:
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0 
       
elif cars  == 3:
    x = []
    for i in co2_new:
        i = i * (1.1950)
        x.append(i)
    co2_new = x
    temp += 0.15
       
elif cars  == 0:
    x = []
    for i in co2_new:
        i = i * (0.8500)
        x.append(i)
    co2_new = x  
    temp += -0.2
     

if public_transport  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      
elif public_transport  == 'Used oftenly':
    x = []
    for i in co2_new:
        i = i * (0.8000)
        x.append(i)
    co2_new = x 
    temp += -0.12
      
elif public_transport  == 'Never Used':
    x = []
    for i in co2_new:
        i = i * (1.2)
        x.append(i)
    co2_new = x 
    temp += 0.19
     
 
if politics  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      
elif politics  == 'Negative':
    x = []
    for i in co2_new:
        i = i * (1.1508)
        x.append(i)
    co2_new = x  
    temp += 0.1
     
elif politics  == 'Positive':
    x = []
    for i in co2_new:
        i = i * (0.9850)
        x.append(i)
    co2_new = x 
    temp += -0.1
     
if awareness  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0
       
elif awareness  == 'Negative':
    x = []
    for i in co2_new:
        i = i * (1.0500)
        x.append(i)
    co2_new = x 
    temp += 0.1
      
elif awareness  == 'Positive':
    x = []
    for i in co2_new:
        i = i * (0.8999)
        x.append(i)
    co2_new = x 
    temp += -0.2
     
 
 
if population  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      
elif population  == 'Lowest Growth':
    x = []
    for i in co2_new:
        i = i * (0.8509)
        x.append(i)
    co2_new = x 
    temp += -0.2
      
elif population  == 'Low Growth':
    x = []
    for i in co2_new:
        i = i * (0.9091)
        x.append(i)
    co2_new = x 
    temp += -0.1
     
elif population  == 'High Growth':
    x = []
    for i in co2_new:
        i = i * (1.0845)
        x.append(i)
    co2_new = x 
    temp += 0.1
     
elif population  == 'Highest Growth':
    x = []
    for i in co2_new:
        i = i * (1.1144)
        x.append(i)
    co2_new = x 
    temp += 0.2
     

if economic_growth  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
      

elif economic_growth  == 'Low Growth':
    x = []
    for i in co2_new:
        i = i * (0.7588)
        x.append(i)
    co2_new = x 
    temp += -0.2
     
elif economic_growth  == 'High Growth':
    x = []
    for i in co2_new:
        i = i * (1.3421)
        x.append(i)
    co2_new = x 
    temp += 0.3
     
 
if deforestation  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x  
    temp += 0.0
     
elif deforestation  == 'highly Reduced':
    x = []
    for i in co2_new:
        i = i * (0.9400)
        x.append(i)
    co2_new = x 
    temp += -0.1
     
elif deforestation  == 'Moderately Reduced':
    x = []
    for i in co2_new:
        i = i * (0.9677)
        x.append(i)
    co2_new = x 
    temp += -0.15
     
    
elif deforestation  == 'Increased':
    x = []
    for i in co2_new:
        i = i * (1.0430)
        x.append(i)
    co2_new = x 
    temp += 0.0
     


if methane  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x  
    temp += 0.0
     
elif methane  == 'highly Reduced':
    x = []
    for i in co2_new:
        i = i * (0.8056)
        x.append(i)
    co2_new = x 
    temp += -0.3
    
elif methane  == 'Moderately Reduced':
    x = []
    for i in co2_new:
        i = i * (0.8935)
        x.append(i)
    co2_new = x
    temp += -0.08
     
    
elif methane  == 'Increased':
    x = []
    for i in co2_new:
        i = i * (1.0430)
        x.append(i)
    co2_new = x 
    temp += 0.1
    

if afforestation  == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x 
    temp += 0.0
     

elif afforestation  == 'low growth':
    x = []
    for i in co2_new:
        i = i * (0.9784)
        x.append(i)
    co2_new = x 
    temp += 0.0
    
elif afforestation  == 'medium growth':
    x = []
    for i in co2_new:
        i = i * (0.9555)
        x.append(i)
    co2_new = x 
    temp += -0.1
    
elif afforestation  == 'high growth':
    x = []
    for i in co2_new:
        i = i * (0.9316)
        x.append(i)
    co2_new = x  
    temp += -0.1
    
if technological == 'Status Quo':
    x = []
    for i in co2_new:
        i = i * (1.0)
        x.append(i)
    co2_new = x
    temp += 0.0
    
elif technological == 'Low Growth':
    x = []
    for i in co2_new:
        i = i * (0.9255)
        x.append(i)
    co2_new = x
    temp += -0.1
     
elif technological == 'Medium Growth':
    x = []
    for i in co2_new:
        i = i * (0.8753)
        x.append(i)
    co2_new = x 
    temp += -0.2
    
elif technological == 'High Growth':
    x = []
    for i in co2_new:
        i = i * (0.8106)
        x.append(i)
    co2_new = x 
    temp += -0.3
    

st.header('CARBON EMISSIONS INCREASE BY 2100')

df = pd.DataFrame({
    'Year': year,
    'Current CO2 Emission (Gigatons)': co2_baseline,
    'New CO2 Emission (gigaton)': co2_new,
})
df = df.rename(columns={'Year':'index'}).set_index('index')
st.line_chart(df)
temp = str(temp)
if len(temp) >4:
    temp = temp[:5]
while temp[-1] =='0':
    temp = temp[:-1]

st.header('Rise in Global Teperature by 2100')
st.write("""
# """, '+ ', temp,  """° C
""")

# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [latitude, longitude],
#     columns=['lat', 'lon'])


#country_list  us_city_list
# col1, col2 = st.beta_columns(2)
# with col1:
#     st.write('')

# with col2:
#     st.write("""


#     ## Select Map style


#     """)
for i in range(1,5):
    st.write('')
st.write("""
    ## Expected Global Water Level Rise
    """)

st.write('')
temp = float(temp)

if temp <3.6:
    water_level_metric = 69.1
    water_level_imperial = 27.20
    city = 'Venice, Bangkok, Miami, Los Angeles, Tokyo, Shanghai, London, Sydney, Melbourne, Mumbai, New york'
else:
    water_level_metric = 111.2
    water_level_imperial = 43.77
    city = 'Venice, Jakarta, Houston, Bangkok, Miami, Los Angeles, Tokyo, Rio de Janeiro, Shanghai, London, Bahamas, Sydney, Melbourne, Mumbai, San Francisco, New york'

col111, mid11, col211 = st.beta_columns([1,10,20])
with col111:
    images = Image.open('sea.jpg')
    st.image(images, width=250)
with col211:
    st.write("""
    # +""", water_level_metric, """ cm ( +""",water_level_imperial,""" inches)
    """)
    st.write("""
    ### Major Cities like """, city, """ will be under water by 2100.
    # """)

for i in range(1,5):
    st.write('')

title_container = st.beta_container()
with title_container:
    col11, mid1, col21 = st.beta_columns([1,10,20])
    with col11:
        st.write('')
    with col21:
        st.write("""
        ## Select Map style
        """)
map_style = st.radio('', ['Satellite', 'Light', 'Dark'])

if map_style == 'Satellite':
    mapstyle = 'mapbox://styles/mapbox/satellite-streets-v11'
if map_style == 'Light':
    mapstyle = 'mapbox://styles/mapbox/light-v10'
if map_style == 'Dark':
    mapstyle = 'mapbox://styles/mapbox/dark-v10'

files = open('coordinates_names.csv', 'r')
reader = csv.reader(files)
for j in reader:
    if j[2] == country:
        latitude = j[0]
        longitude = j[1]

latitude = float(latitude)
longitude = float(longitude)
files.close()

df = pd.DataFrame(
    np.random.randn(1000, 2) / [15, 15] + [latitude, longitude],
    columns=['lat', 'lon'])

st.write("""

# High CO2 Activity near you in a 3D Map 
""")
st.write("""
###### Hold Ctrl Key or ⌘ Key to Rotate Map and Scroll to Zoom! Enter your Country through the side Panel.
###### Demo Data Used may differ from real world values. 
""")


st.write('')
st.pydeck_chart(pdk.Deck(
     map_style = mapstyle,
     initial_view_state=pdk.ViewState(
         latitude=latitude,
         longitude=longitude,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))
for ol in range(3):
    st.write("""""")

st.write("""
### Every Dot you see here is a place where climate change was reported. Greater the Height of Cyclinders, Greater the CLimate Change.
""")

st.write("""
# Climate Change Hotspots
""")
st.write("""
### If you Country is marked You will be affected by Climate Change.
""")
st.write("")
coordinates = pd.read_csv("coordinates.csv")
st.map(coordinates)

for ol in range(5):
    st.write("""""")

st.write("""
### Property of Arnav Suman Copyright@2021
Coded in streamlit library in Python and hosted on heroku a free web host.

""")

