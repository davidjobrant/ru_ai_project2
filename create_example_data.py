from geopy.geocoders import Nominatim
from faker import Faker
import pandas as pd
import awoc 
import pycountry
import random
import numpy as np

fake = Faker()
Faker.seed()

lat_log = []
counter = 0 ;

countries = []
#for c in list(pycountry.countries):
#    countries.append(str(c.alpha_2))
#countries = ['US', 'GB', 'CN']
countries_25 = ['US', 'GB', 'AU', 'IN', 'SE', 'AR', 'AU', 'CA', 'CL', 'DK', 'DE', 'FR', 'KR', 'CN', 'BE', 'MX', 'BR', 'NZ', 'RU','ES','PT', 'MA', 'IL', 'VE', 'JP', 'NI', 'IT','BY', 'HR', 'CU'] # Available locales: https://faker.readthedocs.io/en/master/locales.html
#countries_30 = ['US', 'GB', 'AU', 'IN', 'SE', 'AR', 'AU', 'CA', 'CL', 'DK', 'DE', 'FR', 'KR', 'CN', 'BE', 'MX', 'BR', 'NZ', 'RU','ES','PT', 'MA', 'IL', 'VE', 'JP', 'NI', 'IT','BY', 'HR', 'CU', 'HK', 'HU']
#countries_25_2 = ['BY', 'HR', 'CU', 'HK', 'HU', 'IS', 'JM', 'KE', 'LV', 'LT', 'LU', 'MY', 'MC', 'NL', 'PK', 'PH','PL', 'PR', 'RO', 'RW', 'SM', 'SA', 'RS', 'SG', 'SK', 'SI', 'ZA', 'CH', 'BO'] # Available locales: https://faker.readthedocs.io/en/master/locales.html
#countries = countries_25 + countries_25_2 + ['TR'] + ['GT']
print(len(countries_25))
total = 100 #You can also use Panda's Dataframe len(df)
#size = total / len(countries) -1
country = -1
        #fake.location_on_land()

# for _ in range(total):
#     if counter >= size +1:
#         counter =0
#         country = country + 1
#         print(country)
#         print(len(countries))
#         print (countries[country])
#     lat_log.append(fake.local_latlng(country_code=random.choice(countries)))
#     #lat_log.append(fake.location_on_land())

#     counter = counter + 1 
i = 0
for c in countries_25:
    #print(c)

    lat_log.append(fake.local_latlng(country_code=c))
    if i <= 20: 
        lat_log.append(fake.local_latlng(country_code=c))
    i+=1



    #lat_log.append(fake.local_latlng(country_code=c))
    #lat_log.append(fake.local_latlng(country_code=c))
    #lat_log.append(fake.local_latlng(country_code=c))

random.shuffle(lat_log)
#for i in range (50):
#    lat_log.append(fake.local_latlng(country_code=random.choice(countries)))




print(lat_log)
lat_log = [incom for incom in lat_log if incom]
df = pd.DataFrame(lat_log, columns=["lat", "lon", "city", "code", "continent"])
#print(df)

awoc = awoc.AWOC()

geolocator = Nominatim(user_agent="data")
#df_coords = df[["lat", "lon"]]
#print(df_coords)

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

#print(df)
df = df[['lat', 'lon', 'country', 'continent', 'hype']]

# filter 
df = df[df['continent'] != '-']
print(df)

df.to_csv("df.csv")
