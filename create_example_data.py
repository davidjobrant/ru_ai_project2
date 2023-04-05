from geopy.geocoders import Nominatim
from faker import Faker
import pandas as pd
import awoc 
import random
import numpy as np

fake = Faker()
Faker.seed()

lat_log = []
counter = 0 ;

countries = []

# list of country codes to include 
countries = ['US', 'GB', 'AU', 'IN', 'SE', 'AR', 'AU', 'CA', 'CL', 'DK', 'DE', 'FR', 'KR', 'CN', 'BE', 'MX', 'BR', 'NZ', 'RU','ES','PT', 'MA', 'IL', 'VE', 'JP', 'NI', 'IT','BY', 'HR', 'CU'] # Available locales: https://faker.readthedocs.io/en/master/locales.html
#countries_30 = ['US', 'GB', 'AU', 'IN', 'SE', 'AR', 'AU', 'CA', 'CL', 'DK', 'DE', 'FR', 'KR', 'CN', 'BE', 'MX', 'BR', 'NZ', 'RU','ES','PT', 'MA', 'IL', 'VE', 'JP', 'NI', 'IT','BY', 'HR', 'CU', 'HK', 'HU']
#countries_25_2 = ['BY', 'HR', 'CU', 'HK', 'HU', 'IS', 'JM', 'KE', 'LV', 'LT', 'LU', 'MY', 'MC', 'NL', 'PK', 'PH','PL', 'PR', 'RO', 'RW', 'SM', 'SA', 'RS', 'SG', 'SK', 'SI', 'ZA', 'CH', 'BO'] # Available locales: https://faker.readthedocs.io/en/master/locales.html
total = 100 #You can also use Panda's Dataframe len(df)
#size = total / len(countries) -1
country = -1
        #fake.location_on_land()

# Two options of generating a random list of locations
#for i in range(total):
    #lat_log.append(fake.local_latlng(country_code=random.choice(countries)))
    #lat_log.append(fake.location_on_land())

i = 0
for c in countries:
    lat_log.append(fake.local_latlng(country_code=c))
    if i <= 20: 
        lat_log.append(fake.local_latlng(country_code=c))
    i+=1

# shuffles the list of locations
random.shuffle(lat_log)
print(lat_log)

lat_log = [incom for incom in lat_log if incom]
df = pd.DataFrame(lat_log, columns=["lat", "lon", "city", "code", "continent"])

awoc = awoc.AWOC()
geolocator = Nominatim(user_agent="data")


countries = []
def get_country(row):
    lat = row['lat']
    lon = row['lon']
    info = geolocator.reverse(lat+","+lon,language='en').raw['address']['country']
    print(info)
    countries.append(info) 
    return info

def get_continent(row):
    try:
        cont = awoc.get_country_continent_name(row['country'])
    except NameError:
        cont = "-"
    return cont

df['country'] = df.apply(get_country, axis =1)
df['continent'] = df.apply(get_continent, axis =1)
df['hype'] = np.random.randint(1,10, size=len(df))
df = df[['lat', 'lon', 'country', 'continent', 'hype']]

# filter 
df = df[df['continent'] != '-']
print(df)

df.to_csv("df.csv")
