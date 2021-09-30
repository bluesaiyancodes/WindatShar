#!/usr/bin/env python
# coding: utf-8

# In[1]:


from netCDF4 import Dataset
import geopandas as gpd
#from mpl_toolkits.basemap import Basemap
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objs.scatter3d import Line


# In[2]:


def load_datasets():
    # Load India Shape File
    geodf = gpd.read_file('../../../datasets/IND_adm/ind00.shp')
    
    # Load Terrain Dataset
    ds = Dataset('../../../datasets/WRF-Terrain2.nc')
    #print(ds.variables.keys())
    
    # Load Wind Dataset
    ds1 = Dataset('../../../datasets/SAMPLE_.nc')
    #print(ds1.variables.keys())
    
    return (geodf, ds, ds1)


# In[3]:


def get_variables(ds, ds1):

    # Variables for Terrain Plot
    lon = ds.variables['lon'][:]
    lat = ds.variables['lat'][:]
    lev = ds.variables['lev'][:]
    time = ds.variables['time'][:]
    terrain = ds.variables['terrain'][0,0,:,:]
    # Variables for Wind Plots
    lon_wind = ds1.variables['lon']
    lat_wind = ds1.variables['lat']
    lev_wind = ds1.variables['lev']
    lev2_wind = ds1.variables['lev_2']
    time_wind = ds1.variables['time']
    u_wind = ds1.variables['u']
    v_wind = ds1.variables['v']
    u10 = ds1.variables['u10']
    v10 = ds1.variables['v10']
    
    # Storing Parameters in Cache
    cache = {
        "lon": lon,
        "lat": lat,
        "lev": lev,
        "time": time,
        "terrain": terrain,
        "lon_wind": lon_wind,
        "lat_wind": lat_wind,
        "lev_wind": lev_wind,
        "lev2_wind": lev2_wind,
        "time_wind": time_wind,
        "u_wind": u_wind,
        "v_wind": v_wind,
        "u10": u10,
        "v10": v10
    }
    
    return cache


# In[4]:


def set_masks(cache):
    # Get Variables from cache
    terrain = cache["terrain"]
    lon = cache["lon"]
    lon_wind = cache["lon_wind"]
    lat_wind = cache["lat_wind"]
    
    # masking Terrain
    terrain_ = np.ma.masked_less_equal(terrain, -3)
    terrain_ = np.ma.filled(terrain_, -3)
    
    #terrain_ = np.ma.default_fill_value(None)
    lon_T = np.ma.masked_greater_equal(lon, 80.5)
    lon_T = np.ma.filled(lon_T, 80.5)
    
    # masking wind for lons and lats based on SHAR
    lon_wind_v2 = np.ma.masked_greater_equal(lon_wind, 82)
    lon_wind_v2 = np.ma.filled(lon_wind_v2, 82)
    lat_wind_v2 = np.ma.masked_greater_equal(lat_wind, 16.50)
    lat_wind_v2 = np.ma.filled(lat_wind_v2, 16.50)
    
    # Adding new parameters in Cache
    cache["terrain_"] = terrain_
    cache["lon_T"] = lon_T
    cache["lon_wind_v2"] = lon_wind_v2
    cache["lat_wind_v2"] = lat_wind_v2
    
    return cache


# In[5]:


def hyperparameters(level = 35, leap = 15, h = 500, arrow_size = 0.9, terrain_flag = False, wind_flag = False, contour_flag = False):
    # Starting and ending indices of the wind dataset
    start = 0
    end = 400
    
    # Set Cache for hyperparameters
    hpcache = {
        "level": level,
        "leap": leap,
        "start": start,
        "end": end,
        "h": h,
        "arrow_size": arrow_size,
        "terrain_flag": terrain_flag,
        "wind_flag": wind_flag,
        "contour_flag": contour_flag
    }
    
    return hpcache


# In[6]:


def terrain_colorscale():
    cscale = [[0, "rgb(31,120,180)"],
              [0.008, "rgb(178,223,138)"],
              [0.07, "rgb(112, 166, 65)"],
              [0.12, "rgb(51, 160, 44)"],
              [0.18, "rgb(17, 115, 10)"],
              [0.23, "rgb(79, 136, 35)"],
              [0.28, "rgb(130, 158, 52)"],
              [0.35, "rgb(184, 189, 36)"],
              [0.40, "rgb(247,207,26)"],
              [0.50, "rgb(247,166,23)"],
              [0.60, "rgb(247,121,19)"],
              [0.80, "rgb(247,67,15)"],
              [0.90, "rgb(212, 141, 140)"],      
              [1, "rgb(239,239,249)"]
             ]
    return cscale


# def terrain_colorscale():
#     cscale = [[0, "rgb(31,120,180)"],
#               [0.01, "rgb(178,223,138)"],
#               [0.10, "rgb(51,160,44)"],
#               [0.15, "rgb(30,125,60)"],
#               [0.20, "rgb(79,136,35)"],
#               [0.25, "rgb(170,174,30)"],
#               [0.30, "rgb(170,174,30)"],
#               [0.40, "rgb(247,207,26)"],
#               [0.50, "rgb(247,166,23)"],
#               [0.60, "rgb(247,121,19)"],
#               [0.80, "rgb(247,67,15)"],
#               [0.90, "rgb(212, 141, 140)"],      
#               [1, "rgb(239,239,249)"]
#              ]
#     return cscale

# In[7]:


def basemap_coor():
    trace = pbmap()
    return (trace)


# In[8]:


def india_shp_trace(geodf):
    multipoly1 = geodf["geometry"][0]
    traces = []
    for p in multipoly1:
        x_, y_ = p.exterior.xy
        X = x_.tolist()
        Y = y_.tolist()
        trace = go.Scatter3d(x=X,y=Y,z=np.zeros(len(X)),mode='lines',line=Line(color="black"),name=' ', showlegend = False)
        traces.append(trace)
    return traces


# In[9]:


def get_marker():
    x = [80.213547]
    y = [13.767119]
    trace = []
    mark_cs =  [[0, 'red'], [1.0, 'red']]
    mark = go.Cone(x=x, y=y, z=[0], u=[0], v=[0], w=[-1], sizeref = 160, anchor = "tip", colorscale = mark_cs, showscale = False, name = "SHAR")
    ball = go.Scatter3d(x= [80.213547], y= [13.767119], z=[220], text=["SHAR"],mode='markers',showlegend = False,name = "SHAR", 
                        marker=dict(
                            sizemode='diameter',
                            size = 5, 
                            color = "crimson"
                        )
                       )
    trace.append(mark)
    trace.append(ball)
    return trace


# In[10]:


def wind_shar(hypercache):
    # Load the Datasets
    geodf, ds, ds1 = load_datasets()
    # Get Variables
    cache = get_variables(ds, ds1)
    # Set Masks
    cache = set_masks(cache)

    # Get hyperparameters
    hpcache = hyperparameters(level = hypercache["level"], leap = hypercache["leap"], h = hypercache["h"], arrow_size = hypercache["arrow_size"], terrain_flag = hypercache["terrain_flag"], wind_flag = hypercache["wind_flag"], contour_flag = hypercache["contour_flag"])
    
    # Take slices
    lon_wind_slice = cache["lon_wind_v2"][hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    lat_wind_slice = cache["lat_wind_v2"][hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    u_wind_slice = cache["u_wind"][0,hpcache["level"],hpcache["start"]:hpcache["end"]:hpcache["leap"],hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    v_wind_slice = cache["v_wind"][0,hpcache["level"],hpcache["start"]:hpcache["end"]:hpcache["leap"],hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    
    # Create Mesh Grid
    lon_, lat_ = np.meshgrid(lon_wind_slice,lat_wind_slice)
    
    # Get Color Scale
    cscale = terrain_colorscale()
    
    # Initialize traces to plot
    traces = []
    traces2 = []
    # Get Basemap Traces
   # bmtrace = basemap_coor()
    #traces2 += bmtrace
    
    # Get India shp Trace
    indtrace = india_shp_trace(geodf)
    traces += (indtrace) 
    
    
    # Retrieve required Variables from caches
    lon_T = cache["lon_T"]
    lat = cache["lat"]
    terrain_ = cache["terrain_"]
    h = hpcache["h"]
    arrow_size = hpcache["arrow_size"]
    
    height = np.full(lon_[0,:].shape,h)
    Z = np.full(lon_[0,:].shape,0)

    # Terrain Surface
    if hpcache["terrain_flag"] == True:
        traces.append(go.Surface(x = lon_T, y = lat, z = np.squeeze(terrain_), showscale = True, opacity = .8,colorscale=cscale))
        #traces2.append(go.Surface(x = lon_T, y = lat, z = np.squeeze(terrain_), showscale = False, opacity = .8,colorscale=cscale))
    

    # Cone Plots
    if hpcache["wind_flag"] == True:
        traces.append(go.Cone(x=lon_[0,:], y=lon_[0,:], z=height, u=u_wind_slice[0,:], v=v_wind_slice[0,:], w=Z, coloraxis="coloraxis", sizeref= arrow_size))
    
        for i in range(1, lon_.shape[0]):
            traces.append(go.Cone(x=lon_[i,:], y=lat_[i,:], z=height, u=u_wind_slice[i,:], v=v_wind_slice[i,:], w=Z,sizeref = arrow_size, coloraxis = "coloraxis"))
    
    # U Contour Plot
    if hpcache["contour_flag"] == True:
        Z1 = np.ma.masked_less_equal(u_wind_slice[:,:], 0)
        Z1 = np.ma.filled(Z1, 0)
        traces.append(go.Surface(x = lon_[:,:], y = lat_[:,:], z = np.squeeze(Z1), showscale = True, opacity = 1, name = "U_wind1", coloraxis='coloraxis', contours = {
            "x": {"show": True},
            "y": {"show": True},
            "z": {"show": True, "start": 0, "end": np.ma.max(np.ma.max(Z1, axis = 0), axis = 0), "size": 0.5, "color": "black"}
        }))
    
    # Plot Loaction Marker for Shar
    traces += get_marker()
    
    return traces


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Testing 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




