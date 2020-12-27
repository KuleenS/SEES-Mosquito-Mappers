import os
from PIL import Image
import getpass 
import glob
import time
import xml.etree.ElementTree as ET
from math import pi
from math import cos
from sentinelsat import SentinelAPI
import geopandas as gpd
import folium 
from shapely.geometry import MultiPolygon, Polygon
import rasterio as rio
import pandas as pd

def latlongmeters(lat, lon, dy, dx):
    Radius_of_earth = 6378137
    new_latitude  = lat  + (dy / Radius_of_earth) * (180 / pi)
    new_longitude = lon + (dx / Radius_of_earth) * (180 / pi) / cos(lat * pi/180)
    return [new_latitude,new_longitude]
def make100msquare(lat, lon):
    return [latlongmeters(lat, lon, 1750, 1750), latlongmeters(lat, lon, -1750, 1750), latlongmeters(lat, lon, -1750, -1750), latlongmeters(lat, lon, 1750, -1750)]
def make5msquare(lat, long):
    return [latlongmeters(lat, lon, 5, 5), latlongmeters(lat, lon, -5, 5), latlongmeters(lat, lon, -5, -5), latlongmeters(lat, lon, 5, -5)]
def makeKMLfile(coordinates, PlotID, Category, GridNumber):
    for i in range(len(coordinates)):
        coordinates[i] = str(coordinates[i][1]) + ',' + str(coordinates[i][0])
    coordinatestring = ' '.join(coordinates)+' ' +str(coordinates[0])
    if Category=='CenterPoint':
        prefix = 'CentP'
    else:
        prefix = 'GridP'
    filename = str(PlotID)+'_'+str(GridNumber)+'_' +prefix+'.kml'
    #put folder
    folder = ''
    with open(os.path.join(folder,filename), 'w') as f:
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/kml/2.2 https://developers.google.com/kml/schema/kml22gx.xsd">')
        f.write('\n')
        f.write('<Document>')
        f.write('\n')
        f.write('<Placemark>')
        f.write('\n')
        f.write('<Polygon>')
        f.write('\n')
        f.write('<outerBoundaryIs>')
        f.write('\n')
        f.write('<LinearRing>')
        f.write('\n')
        f.write('<coordinates>'+coordinatestring+'</coordinates>')
        f.write('\n')
        f.write('</LinearRing>')
        f.write('\n')
        f.write('</outerBoundaryIs>')
        f.write('\n')
        f.write('</Polygon>')
        f.write('\n')
        f.write('</Placemark>')
        f.write('\n')
        f.write('</Document>')
        f.write('\n')
        f.write('</kml>')
def latlongmeters(lat, lon, dy, dx):
    Radius_of_earth = 6378137
    new_latitude  = lat  + (dy / Radius_of_earth) * (180 / pi)
    new_longitude = lon + (dx / Radius_of_earth) * (180 / pi) / cos(lat * pi/180)
    return [new_latitude,new_longitude]


def CenterPointKML():
    path = ''
    df = pd.read_csv(path)
    df = df[['PLOTID','Category','LAT','LONG']]
    df = df[df['Category'].str.contains('Center')]
    for ind in df.index: 
        coordinatelist = make100msquare(float(df['LAT'][ind]), float(df['LONG'][ind]))
        makeKMLfile(coordinatelist, df['PLOTID'][ind], df['Category'][ind])


path = ''
df = pd.read_csv(path)
df = df[['PLOTID','Category','LAT','LONG']]
for ind in df.index: 
    lat, lon = float(df['LAT'][ind]), float(df['LONG'][ind])
    upperleftcorner=latlongmeters(lat, lon, 50, -60)
    upperrow = []
    upperrow.append(upperleftcorner)
    for j in range(11):
        for i in range(11):
            nextstop = latlongmeters(upperleftcorner[0],upperleftcorner[1], 0, 10)
            upperrow.append(nextstop)
            upperleftcorner[1] = nextstop[1]
        upperleftcorner = latlongmeters(upperleftcorner[0],upperleftcorner[1], -10, -110)
    newarr = []
    for i in range(11):
        arr = []
        arr = upperrow[i*11:(i+1)*11]
        newarr.append(arr)
    M = 11
    N = 11
    Count = 1 
    for i in range(M): 
        
        # If current row is 
        # even, print from 
        # left to right 
        if i % 2 == 0: 
            for j in range(N): 
                coordinatelist = make5msquare(newarr[i][j][0], newarr[i][j][1])
                makeKMLfile(coordinatelist, df['PLOTID'][ind], df['Category'][ind], Count)
                Count+=1
        # If current row is  
        # odd, print from 
        # right to left 
        else: 
            for j in range(N - 1, -1, -1): 
                coordinatelist = make5msquare(newarr[i][j][0], newarr[i][j][1])
                makeKMLfile(coordinatelist, df['PLOTID'][ind], df['Category'][ind], Count)
                Count+=1
       
