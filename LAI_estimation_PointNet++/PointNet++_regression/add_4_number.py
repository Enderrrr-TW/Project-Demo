import numpy as np
import os
import re
# f_dir='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2021/trim_normalized_fps'
# output_dir='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2021/trim_normalized_fps_hi'
f_dir='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2020/normalized_subsets_fps_4096'
output_dir='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2020/normalized_subsets_fps_4096_hi'
try: os.mkdir(output_dir)
except: pass
dates=os.listdir(f_dir)
for i in range(len(dates)):
    sub_dir=f'{f_dir}/{dates[i]}'
    output_sub_dir=f'{f_dir}/{dates[i]}'
    try: os.mkdir(output_sub_dir)
    except: pass
    flist=os.listdir(sub_dir)
    for j in flist:
        plot=re.split('_',j)[4]
        if int(plot)<=5444: #<5444=hybrid
            variety=np.int16(1)
        else:
            variety=0
        fname=f'{sub_dir}/{j}'
        xyz=np.loadtxt(fname)
        xyz=np.column_stack((xyz,np.full(4096,variety)))
        output_name=f'{output_sub_dir}/{j}'
        print(output_name)
        np.savetxt(output_name,xyz)
