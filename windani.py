from SHARv6 import set_datasets, wind_shar_animate
import plotly.graph_objects as go


set_datasets(terrain_path = "datasets/WRF-Terrain2.nc", wind_path = "datasets/SAMPLE_.nc")

params ={}
params["leap"] = 15
params["arrow_size"] = 0.9

traces = wind_shar_animate(params)

fig = go.Figure(traces)
fig.update_layout(
    scene = {
        "xaxis": {"nticks": 10, "range": [70,87]},
        "zaxis" : {"nticks": 5 },
        "yaxis": {"range": [5,20]},
        # "camera_eye": {"x": .1, "y": -.4, "z": .8},
        "aspectratio": {"x": 1, "y": .75, "z": 0.1},
    },
    scene_camera = dict(eye=dict(x=0.28, y=-0.08, z=.15)),
    coloraxis = {'colorscale':'portland'}
)
fig.show()





