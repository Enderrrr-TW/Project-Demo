Input:

Point Cloud (colorized by height): 

<img src="https://github.com/Enderrrr-TW/Project-Demo/blob/main/LiDAR_Feature_Extraction/LiDAR_point_cloud.png" width="500">

and

Plot Boundary (Visualized by ArcGIS pro):

![image](https://github.com/Enderrrr-TW/Project-Demo/blob/main/LiDAR_Feature_Extraction/plot_boundary.png)

Output:

![image](https://github.com/Enderrrr-TW/Project-Demo/blob/main/LiDAR_Feature_Extraction/LiDAR%20features.png)

Note that the heights of the points are geodetic height. To determine the plant heights, a digital elevation model (DEM) is generated using the cloth simulation filter (CSF) method.

This script also includes a quality controll procedure to evaluate the misallignment in z-direction caused by GPS quality.
