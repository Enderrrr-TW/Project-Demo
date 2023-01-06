import numpy as np
import os
from numba import cuda
from pathlib import Path

import cupy as cp
np.random_seed=42
def farthest_point_sample(point, npoint):
    """
    Input:
        xyz: pointcloud data, [N, D]
        npoint: number of samples
    Return:
        centroids: sampled pointcloud index, [npoint, D]
    """
    N, D = point.shape
    xyz = point[:,:3]
    centroids = np.zeros((npoint,)) # clustering center
    distance = np.ones((N,)) * 1e10
    farthest = np.random.randint(0, N)
    for i in range(npoint):
        centroids[i] = farthest
        centroid = xyz[farthest, :]
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = np.argmax(distance, -1)
    point = point[centroids.astype(np.int32)]
    return point
def fps_cuda(point,npoint):
    point=cp.asarray(point)
    N, D = point.shape
    xyz = point
    centroids = cp.zeros((npoint,)) # clustering center
    distance = cp.ones((N,)) * 1e10
    farthest = cp.random.randint(0, N)
    for i in range(npoint):

        centroids[i] = farthest
        centroid = xyz[farthest, :]
        dist = cp.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = cp.argmax(distance, -1)
    point = point[centroids.astype(cp.int32)]
    return point

def main():
    input_folder='E:/Ender/data/UAV/HIPS_2020/for_pointnet/normalized_subsets'
    output_folder='E:/Ender/data/UAV/HIPS_2020/normalized_subsets_fps_4096'
    try:
        os.mkdir(output_folder)
    except:
        pass
    xyz_dates=os.listdir(input_folder)
    for i in range(len(xyz_dates)):
        sub_dir=input_folder+'/'+xyz_dates[i]
        try:
            os.mkdir(output_folder+'/'+xyz_dates[i])
        except: pass
        las_list=os.listdir(sub_dir)
        for j in range(len(las_list)):
            # if las_list[j].endswith('subset2.las') or las_list[j].endswith('subset3.las') or las_list[j].endswith('subset4.las') :
            xyz_name=sub_dir+'/'+las_list[j]            

            root='_fps.xyz'
            output_name=xyz_name.replace(input_folder,output_folder)
            output_name=output_name.replace('.xyz',root)
            xyz=np.loadtxt(xyz_name)
            xyz_fps=fps_cuda(xyz,4096)
            xyz_fps=xyz_fps.transpose()
            xyz_fps[0]=xyz_fps[0]-cp.mean(xyz_fps[0])
            xyz_fps[1]=xyz_fps[1]-cp.mean(xyz_fps[1])
            xyz_fps[2]=xyz_fps[2]-cp.mean(xyz_fps[2])
            xyz_fps=cp.asnumpy(xyz_fps)
            np.savetxt(output_name,xyz_fps)
main()