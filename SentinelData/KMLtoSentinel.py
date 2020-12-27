import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from PIL import Image
import getpass 
import glob
import time
import xml.etree.ElementTree as ET
from math import pi
from sentinelsat import SentinelAPI
import geopandas as gpd
import folium 
from shapely.geometry import MultiPolygon, Polygon
import rasterio as rio
"""
u = input('Username: ')
try: 
    p = getpass.getpass('Password: ') 
except Exception as error: 
    print('ERROR', error) """
#use login for collect.earth
u = ''
p = ''
browser= webdriver.Firefox(executable_path=r'src\geckodriver.exe')
browser.get('https://collect.earth/')

time.sleep(5)

try:
    button =WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login/Register']"))) 
    button.click()
    try:
        username = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
    except:
        print('Something went wrong')
    password = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    username.send_keys(u)
    time.sleep(5)
    password.send_keys(p)
    button =WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    button.click()
except:
    print('You are already logged in')
time.sleep(5)
filter = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "filterInstitution")))
filter.send_keys('globe')
button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'btn bg-lightgreen')])[1]")))
button.click()

source = browser.page_source
soup = BeautifulSoup(source, features="html.parser")
anchors = soup.find_all('a',{'class':'btn btn-sm btn-outline-lightgreen btn-block'})
plots_list = []
for anchor in anchors:
    plots_list.append(anchor.text)


while True:
    for i in range(len(plots_list)):
        print(str((i+1))+'. '+str(plots_list[i]))
    Map = input('What map do you want the KML from?(choose number) ')
    try:
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, plots_list[int(Map)-1])))
    except:
        print('Something did\'nt go so right. Try again')
    finally:
        break
time.sleep(2)
button.click()
while True:
    review = input('Is this plot already reviewed by you?(y or n) ')
    if review=='y':
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'reviewCheck')))
        button.click()
        break
    if review=='n':
        break
    else:
        print('Please use y or n')
button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'go-to-first-plot-button')))
button.click()
if review == 'y':
    plt_number = int(input('What is your plot number? '))*100 + 1
    browser.switch_to.window(browser.window_handles[0])
    for i in range(35):
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Download Plot KML')))
        button.click()
        try:
            button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"(//h3[text()='▶'])[1]")))
            button.click()
        except:
            pass
        plotID = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID,"plotId")))
        plotID.clear()
        plt_number+=1
        plotID.send_keys(str(plt_number))
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[text()='Go to plot']")))
        button.click()
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[0])
if review =='n':  
    plt_number = int(input('What is your plot number? '))*100 + 1
    browser.switch_to.window(browser.window_handles[0])
    button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"(//h3[text()='▶'])[1]")))
    button.click()
    plotID = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID,"plotId")))
    plotID.clear()
    plotID.send_keys(str(plt_number))
    button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[text()='Go to plot']")))
    button.click()
    browser.switch_to.window(browser.window_handles[0])
    for i in range(35):
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Download Plot KML')))
        button.click()
        try:
            button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"(//h3[text()='▶'])[1]")))
            button.click()
        except:
            pass
        plotID = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID,"plotId")))
        plotID.clear()
        plt_number+=1
        plotID.send_keys(str(plt_number))
        button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[text()='Go to plot']")))
        button.click()
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[0])
browser.quit()
path = input('Copy the full path to where the KML is')
kml_file_list = glob.glob(path + '*.kml')
namespace = '{http://www.opengis.net/kml/2.2}'
Radius_of_earth = 6378137 #in meters
for kml in kml_file_list:
    fp = open(kml, 'r')
    element = ET.parse(fp)
    Polygon = element.findall('{0}Document/{0}Placemark/{0}Polygon'.format(namespace))
    Coordinates_texts = ((element.findall('{0}Document/{0}Placemark/{0}Polygon/{0}outerBoundaryIs/{0}LinearRing/{0}coordinates'.format(namespace))).text).split()
    #convert to ints lmao idiot
    for i in range(len(Coordinates_texts)):
        Coordinates_texts[i]= Coordinates_texts[i].split(",")
    Coordinates_texts = [list(map(float, x)) for x in Coordinates_texts]
    min_long = Coordinates_texts[0][0]
    max_long = 0
    min_lat =  Coordinates_texts[0][1]
    max_lat = 0
    for i in range(len(Coordinates_texts)):
        min_long = min(min_long, Coordinates_texts[i][0])
        max_long = max(max_long, Coordinates_texts[i][0])
        min_lat = min(min_lat, Coordinates_texts[i][1])
        max_lat = max(max_lat, Coordinates_texts[i][1])
    #
    #new_latitude  = latitude  + (dy / r_earth) * (180 / pi);
    #new_longitude = longitude + (dx / r_earth) * (180 / pi) / cos(latitude * pi/180);
    for i in range(len(Coordinates_texts)): #y
        if Coordinates_texts[i][1]==max_lat:
            Coordinates_texts[i][1] = Coordinates_texts[i][1]+(5 / Radius_of_earth) * (180 / pi)
        else:
            Coordinates_texts[i][1] = Coordinates_texts[i][1]+(-5 / Radius_of_earth) * (180 / pi)
    for i in range(len(Coordinates_texts)): #x
        if Coordinates_texts[i][0]==max_long:
            Coordinates_texts[i][0]=Coordinates_texts[i][0] + (5 / Radius_of_earth) * (180 / pi) / cos(Coordinates_texts[i][1] * pi/180)
        else:
            Coordinates_texts[i][0]=Coordinates_texts[i][0] + (-5 / Radius_of_earth) * (180 / pi) / cos(Coordinates_texts[i][1] * pi/180)
    Coordinates_texts = [list(map(str, x)) for x in Coordinates_texts]
    for i in range(len(Coordinates_texts)):
        Coordinates_texts[i]=','.join(Coordinates_texts[i])
    Coordinates_texts = ' '.join(Coordinates_texts)
    element.findall(('{0}Document/{0}Placemark/{0}Polygon/{0}outerBoundaryIs/{0}LinearRing/{0}coordinates'.format(namespace))).text = Coordinates_texts
    element.remove('{0}Document/{0}Placemark/{0}ExtendedData'.format(namespace))
    a = gpd.read_file(kml)
    os.mkdir(os.path.join(os.getcwd(), 'ShapeFiles'))
    kml_name = os.path.basename(kml).split('.')[0]
    a.to_file(os.path.join(os.getcwd(), 'ShapeFiles', kml_name),driver='ESRI Shapefile')
#insert your login to SentinelAPI
user = ''
password = ''
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

shapefiles_list = glob.glob(os.path.join(os.getcwd(), 'ShapeFiles')+ '*.shp')
for shapefile in shapefiles_list:
    GPD_DF =  gpd.read_file(shapefile)
    footprint = None
    for i in GPD_DF['geometry']:
        footprint = i
    products = api.query(footprint,
                    #modify the date 
                     date = ('20190601', '20190626'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0,10)
                    )
    products_gdf = api.to_geodataframe(products)
    products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
