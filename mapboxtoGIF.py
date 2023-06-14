#This is a hobby project, it takes two LAT/LONG points, calculates points between them and calls MAPBOX API requests to pull images. The images are then taken and a GIF is made between point one and point two. 

from pathlib import Path
import imageio.v2 as imageio
import os
import math

#Enter MAPBOX API token
TOKEN=''

#Enter your start and stop points for GIF movement
start_point=[-11.1111,11.1111]
end_point=[-12.2222,12.2222]
steps=1
#Step_count sets the distance between each API (image) pulled from map box, the smaller the number the more pictures and the smooter the animation
step_count=0.0003
lat = 1
lon = 1

#list of intermediate points for GET request for maps. 
intermediate_points=[]

intermediate_points += start_point

inter_point = start_point


#calculate slope of the triangle the start and end points given above
direction_travel = (end_point[0]-start_point[0])/(end_point[1]-start_point[1])

#set slope to travel in the direction required for later calculations
if end_point[0] < start_point[0]:
    lat*=-1
if end_point[1] < start_point[1]:
    lon*=-1

#pythagorean therum used to calculate the length of the lat and long steps based on a hypotenuse (travel distance) set as the variable step count
lon_step = step_count/(math.sqrt(direction_travel*direction_travel)+1)

lat_step = abs(lon_step*direction_travel)

#print(lat_step)
#print(lon_step)

if end_point[0] >= start_point[0] and end_point[1] >= start_point[1]:
    while inter_point[0] <= end_point[0] and inter_point[1] <= end_point[1]:
        inter_point[0] = round(start_point[0]+(lat*lat_step*steps),4)
        inter_point[1] = round(start_point[1]+(lon*lon_step*steps),4)
        intermediate_points += inter_point
        steps = steps +1

elif end_point[0] <= start_point[0] and end_point[1] >= start_point[1]:
    while inter_point[0] >= end_point[0] and inter_point[1] <= end_point[1]:
        inter_point[0] = round(start_point[0]+(lat*lat_step*steps),4)
        inter_point[1] = round(start_point[1]+(lon*lon_step*steps),4)
        intermediate_points += inter_point
        steps = steps +1


elif end_point[0] <= start_point[0] and end_point[1] <= start_point[1]:
    while inter_point[0] >= end_point[0] and inter_point[1] >= end_point[1]:
        inter_point[0] = round(start_point[0]+(lat*lat_step*steps),4)
        inter_point[1] = round(start_point[1]+(lon*lon_step*steps),4)
        intermediate_points += inter_point
        steps = steps +1

elif end_point[0] >= start_point[0] and end_point[1] <= start_point[1]:
    while inter_point[0] <= end_point[0] and inter_point[1] >= end_point[1]:
        inter_point[0] = round(start_point[0]+(lat*lat_step*steps),4)
        inter_point[1] = round(start_point[1]+(lon*lon_step*steps),4)
        intermediate_points += inter_point
        steps = steps +1

#list of coordinates that can be used to start making GET requests to MAPBOX to get the maps well use for the next step
intermediate_points += end_point
print(intermediate_points)

count=0
while count <= (len(intermediate_points)/2 - 1):    
    print(count)
    os.system('curl -g https://api.mapbox.com/styles/v1/mapbox/dark-v10/static/{0},{1},12.00,0/500x500?access_token={2} --output {0},{1}.png'.format(intermediate_points[count*2],intermediate_points[count*2+1],TOKEN))
    count +=1



image_path = Path('./')
images = list(image_path.glob('*.png'))
images.sort()
image_list = []
for i in images:
    image_list.append(imageio.imread(i))
    
imageio.mimwrite('results.gif', image_list, loop=100, duration=300)
