Input:

Point Cloud (colorized by height): 

<img src="https://user-images.githubusercontent.com/40990773/210366291-2bea5fce-c01a-45a3-89ad-5c8f3fed5679.png" width="500">

and

Plot Boundary (Visualized by ArcGIS pro):

![image](https://user-images.githubusercontent.com/40990773/210366720-1299104e-bd0c-427c-9859-6f149be4d898.png)

Output:

![image](https://user-images.githubusercontent.com/40990773/210364661-ade55b89-b9e5-46e5-93f7-53c4c7178cc5.png)

Note that the heights of the points are geodetic height. To determine the plant heights, a digital elevation model (DEM) is generated using the cloth simulation filter (CSF) method.

This script also includes a quality controll procedure to evaluate the misallignment in z-direction caused by GPS quality.
