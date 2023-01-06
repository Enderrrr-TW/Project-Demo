import numpy as np
import laspy #laspy>2.0
import os
input_folder='E:/Ender/data/UAV/HIPS_2020/non_ground_plot'
output_folder='E:/Ender/data/UAV/HIPS_2020/normalized_subsets'

las_dates=os.listdir(input_folder)
def preprocessing(las_x,las_y,las_z):
    x_avg=np.mean(las_x)
    y_avg=np.mean(las_y)
    z_avg=np.mean(las_z)
    x_temp=las_x-x_avg
    y_temp=las_y-y_avg
    z_temp=las_z-z_avg
    R_max=np.max([np.max(x_temp),np.max(y_temp),np.max(z_temp)])
    x_normalized=x_temp/R_max
    y_normalized=y_temp/R_max
    z_normalized=z_temp/R_max
    # xyz=np.vstack([x_normalized,y_normalized,z_normalized])
    xyz=np.vstack([x_temp,y_temp,z_temp])
    xyz=xyz.T
    return xyz

for i in range(len(las_dates)):
    sub_dir=input_folder+'/'+las_dates[i]
    try:
        os.mkdir(output_folder+'/'+las_dates[i])
    except: pass
    las_list=os.listdir(sub_dir)
    for j in range(len(las_list)):
        # if las_list[j].endswith('subset2.las') or las_list[j].endswith('subset3.las') or las_list[j].endswith('subset4.las') :
        if las_list[j].endswith('.las'):
            las_name=sub_dir+'/'+las_list[j]
            las=laspy.read(las_name)
            las_x=np.array(las.x)
            las_y=np.array(las.y)
            las_z=np.array(las.z)
            xyz=preprocessing(las_x,las_y,las_z)
            root='_normalized.xyz'
            output_name=las_name.replace(input_folder,output_folder)
            output_name=output_name.replace('.las',root)
            np.savetxt(output_name,xyz)
