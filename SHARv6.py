#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objs.scatter3d import Line
import plotly.express as px

#from Plotly3DBasemap2 import get_3D_Plotly_Basemap as pbmap


# In[ ]:
terrain_data_path = "../../../datasets/WRF-Terrain2.nc"
wind_data_path = "../../../datasets/SAMPLE_.nc"

def set_datasets(terrain_path ="datasets/WRF-Terrain2.nc" , wind_path = "/datasets/SAMPLE_.nc"):
    print("Setting Datasets")
    terrain_data_path = terrain_path
    wind_data_path = wind_path

def load_datasets():
    print(terrain_data_path)
    print(wind_data_path)
    ds = Dataset(terrain_data_path)
    #print(ds.variables.keys())
    ds1 = Dataset(wind_data_path)
    #print(ds1.variables.keys())
    print("Datasets Loaded")
    return (ds, ds1)


# In[ ]:


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
    
    print("Variables configured")
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


# In[ ]:


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
    
    lev_wind = cache["lev_wind"]
    wind_val = np.asarray(lev_wind[:])
    wind_arr = []
    wind_arr_val = []
    for i in range(0, len(wind_val)-1):
        if i > 6:
            wind_arr.append(i)
            wind_arr_val.append(wind_val[i])
    
    # Adding new parameters in Cache
    cache["terrain_"] = terrain_
    cache["lon_T"] = lon_T
    cache["lon_wind_v2"] = lon_wind_v2
    cache["lat_wind_v2"] = lat_wind_v2
    cache["wind_val"] = wind_val
    cache["wind_arr"] = wind_arr
    cache["wind_arr_val"] = wind_arr_val
    
    print("Masking Performed")
    return cache


# In[ ]:


def hyperparameters(level = 15, leap = 15, h = 500, arrow_size = 0.9, terrain_flag = False, wind_flag = False, contour_flag = False):
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
    print("Hyperparameters are set")
    
    return hpcache


# In[ ]:


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

# In[ ]:


def india_shp_trace():
    import geopandas as gpd
    geodf = gpd.read_file('../../../datasets/IND_adm/IND00.shp')
    multipoly1 = geodf["geometry"][0]
    traces = []
    for p in multipoly1:
        x_, y_ = p.exterior.xy
        X = x_.tolist()
        Y = y_.tolist()
        trace = go.Scatter3d(x=X,y=Y,z=np.zeros(len(X)),mode='lines',line=Line(color="black"),name=' ', showlegend = False)
        traces.append(trace)
        
    print("Map Added")
    return traces


# In[ ]:


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


# In[ ]:


def wind_animation(cache, anim_cache):
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    fig_dict["layout"]["sliders"] = {
        "args": [
            "transition", {
                "duration": 600,
                "easing": "cubic-in-out"
            }
        ],
        "initialValue": str(cache["wind_arr_val"][0]),
        "plotlycommand": "animate",
        "values": cache["wind_arr_val"],
        "visible": True
    }
    
    fig_dict["layout"]["title"] = "Wind TimeLine"
    
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 700, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 500,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Level:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 500, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    
    cscale = terrain_colorscale()
    
    lon_T = anim_cache["lon_T"]
    lat = anim_cache["lat"]
    lon_ = anim_cache["lon_"]
    lat_ = anim_cache["lat_"]
    height = anim_cache["height"]
    u_wind_slice = anim_cache["u_wind_slice"]
    v_wind_slice = anim_cache["v_wind_slice"]
    Z = anim_cache["Z"]
    arrow_size = anim_cache["arrow_size"]
    indtrace = india_shp_trace()
    
    fig_dict["data"].append(go.Surface(x = lon_T, y = lat, z = np.squeeze(cache["terrain_"]), showscale = True, opacity = .8,colorscale=cscale))
    for i in range(0, lon_.shape[0]):
        fig_dict["data"].append(go.Cone(x=lon_[i,:], y=lat_[i,:], z=np.full(lon_[0,:].shape,0), u=u_wind_slice[7,i,:], v=v_wind_slice[7,i,:], w=Z,sizeref = arrow_size, coloraxis = "coloraxis"))                   
    fig_dict["data"] += indtrace
    fig_dict["data"] += get_marker()
    
    for level in cache["wind_arr"]:
        frame = {"data": [], "name": str(cache["wind_val"][level])}
        frame["data"].append(go.Surface(x = lon_T, y = lat, z = np.squeeze(cache["terrain_"]), showscale = True, opacity = .8,colorscale=cscale))
        h = cache["wind_val"][level] * 100
        height = np.full(lon_[0,:].shape,h)
        for i in range(0, lon_.shape[0]): 
            frame["data"].append(go.Cone(x=lon_[i,:], y=lat_[i,:], z=height, u=u_wind_slice[level,i,:], v=v_wind_slice[level,i,:], w=Z,sizeref = arrow_size, coloraxis = "coloraxis"))
        frame["data"] += indtrace
        frame["data"] += get_marker()
        
        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [cache["wind_val"][level]],
            {"frame": {"duration": 500, "redraw": False},
             "mode": "immediate"}
        ],
            "label": cache["wind_val"][level],
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)
        
    fig_dict["layout"]["sliders"] = [sliders_dict]
    return fig_dict


# In[ ]:


def wind_shar_animate(hypercache):
    # Load the Datasets
    ds, ds1 = load_datasets()
    # Get Variables
    cache = get_variables(ds, ds1)
    # Set Masks
    cache = set_masks(cache)
    # Get hyperparameters
    hpcache = hyperparameters(leap = hypercache["leap"], arrow_size = hypercache["arrow_size"])
    
    # Take slices
    lon_wind_slice = cache["lon_wind_v2"][hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    lat_wind_slice = cache["lat_wind_v2"][hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    u_wind_slice = cache["u_wind"][0,:,hpcache["start"]:hpcache["end"]:hpcache["leap"],hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    v_wind_slice = cache["v_wind"][0,:,hpcache["start"]:hpcache["end"]:hpcache["leap"],hpcache["start"]:hpcache["end"]:hpcache["leap"]]
    
    # Create Mesh Grid
    lon_, lat_ = np.meshgrid(lon_wind_slice,lat_wind_slice)
    
    # Get Color Scale
    cscale = terrain_colorscale()
    
    # Initialize traces to plot
    traces = []
    
    # Get India shp Trace
    #indtrace = india_shp_trace()
    #traces += (indtrace) 
    
    
    # Retrieve required Variables from caches
    lon_T = cache["lon_T"]
    lat = cache["lat"]
    terrain_ = cache["terrain_"]
    h = hpcache["h"]
    arrow_size = hpcache["arrow_size"]
    
    height = np.full(lon_[0,:].shape,h)
    Z = np.full(lon_[0,:].shape,0)
    
    anim_cache = {}
    anim_cache["lon_"] = lon_
    anim_cache["lat_"] = lat_
    anim_cache["height"] = height
    anim_cache["u_wind_slice"] = u_wind_slice
    anim_cache["v_wind_slice"] = v_wind_slice
    anim_cache["Z"] = Z
    anim_cache["arrow_size"] = arrow_size
    anim_cache["lon_T"] = lon_T
    anim_cache["lat"] = lat
    
    
    traces = wind_animation(cache, anim_cache)
    print("Performing final computation. ETA ~ 22s")
    # Plot Loaction Marker for Shar
    #traces += get_marker()
    
    return traces


# In[ ]:


if __name__ == '__main__':
    from timeit import default_timer as timer
    s_time = timer()
    traces= wind_shar_animate()
    fig = go.Figure(traces)
    fig.update_layout(
        scene = {
            "xaxis": {"nticks": 10, "range": [55,105]},
            "zaxis" : {"nticks": 5 },
            "yaxis": {"range": [5,35]},
            # "camera_eye": {"x": .1, "y": -.4, "z": .8},
            "aspectratio": {"x": 1, "y": .75, "z": 0.1},
        },
        scene_camera = dict(eye=dict(x=0.28, y=-0.08, z=.15)),
        coloraxis = {'colorscale':'portland'}
    )
    e_time = timer()
    print("Time taken to compute: ", e_time-s_time)
    fig.show()


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




