import ee
import numpy as np
import matplotlib.pyplot as plt
ee.Authenticate()

ee.Initialize(project='ee-philipkenneweg')

# Import the MODIS land cover collection.
lc = ee.ImageCollection('MODIS/006/MCD12Q1')

# Import the MODIS land surface temperature collection.
lst = ee.ImageCollection('MODIS/006/MOD11A1')

# Import the USGS ground elevation image.
elv = ee.Image('USGS/SRTMGL1_003')

sl2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") # Sentinel 2

# Initial date of interest (inclusive).
i_date = '2017-01-01'

# Final date of interest (exclusive).
f_date = '2020-01-01'

# Selection of appropriate bands and dates for LST.
lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)

# Define the urban location of interest as a point near Lyon, France.
u_lon = 8.5325
u_lat = 52.03202
u_poi = ee.Geometry.Point(u_lon, u_lat)

roi = u_poi.buffer(1e4)

sl2_img = sl2.select("B2", "B3", "B4").filterBounds(roi).filterDate(i_date, f_date).mean()


from IPython.display import Image

# Create a URL to the styled image for a region around France.
url = sl2_img.getThumbUrl({'dimensions': 512, 'region': roi, 'bands': 'B4,B3,B2'})
print(url)

# Display the thumbnail land surface temperature in France.
print('\nPlease wait while the thumbnail loads, it may take a moment...')
img = Image(url=url)

plt.imshow(np.asarray(img))
plt.show()

