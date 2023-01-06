'''
Author: An-Te Huang
Time: 2021/12/25
'''
from importlib.resources import path
import os
import numpy as np
import warnings
import pickle
import json
from tqdm import tqdm
from torch.utils.data import Dataset

# from Pointnet_Pointnet2_pytorch.test_classification import test
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

warnings.filterwarnings('ignore')
def decide_npoints(data_dict):
    npoint_list=[]
    assert type(data_dict)==dict
    for i in data_dict['train']['path']:
        xyz=np.loadtxt(i)
        npoint_list.append(xyz.shape[0])
    for i in data_dict['test']['path']:
        xyz=np.loadtxt(i)
        npoint_list.append(xyz.shape[0])
    print('minimum number of points:',np.min(npoint_list))
    return np.min(npoint_list)

def randomly_sample(xyz,npoints):
    '''
    xyz: preprocessed point cloud
    npoints: output from decide_npoints
    return a sampled point cloud in order to build a tensor (all point clouds must have the same number of points)
    '''
    np.random.seed(42)
    random_indice=np.random.choice(xyz.shape[0],size=npoints,replace=False)
    xyz_sampled=xyz[random_indice]
    return xyz_sampled

class LASDataLoader(Dataset):
    def __init__(self,data,fold,split='train', preprocessed=True,sampled=True):
        super().__init__()
        # self.root = '/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/backpack/normalized_subset_fps'
        # self.root='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/trim_normalized_fps' # HIPS_2021
        self.root='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2020/normalized_subsets_fps_4096' # HIPS_2020
        self.preprocessed = preprocessed
        self.split=split
        self.sampled=sampled

        # with open(self.root+'/train_test_split.json','r') as json_file:
        with open(self.root+'/train_test_split_transfer.json','r') as json_file:

            self.data_dict=json.load(json_file)

        self.npoints = decide_npoints(self.data_dict)
        
        assert (split == 'train' or split == 'test')
        self.datasize=len(self.data_dict[split]['LAI'])
        print('root:',self.root)
    def __len__(self):
        return self.datasize

    def _get_item(self,index):
        if self.preprocessed==True:
            xyz=np.loadtxt(self.data_dict[self.split]['path'][index])
            LAI=np.float32(self.data_dict[self.split]['LAI'][index])
            # xyz_sampled=farthest_point_sample(xyz,self.npoints)
            # xyz_sampled=randomly_sample(xyz,self.npoints)
            if self.sampled==False:
                xyz_sampled=xyz
                return xyz_sampled,LAI
            else:
                return xyz,LAI
        else: 
            print('write this part by yourself dude')
            quit()
    def __getitem__(self, index):
        return self._get_item(index)

class LASDataLoader_kfold(Dataset):
    def __init__(self,data,fold,split='train', preprocessed=True,sampled=True):
        super().__init__()
        assert (data=='HIPS_2020' or data== 'HIPS_2021')
        if data=='HIPS_2020':
            self.root='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2020/normalized_subsets_fps_4096' # HIPS_2020
        elif data=='HIPS_2021':
            self.root='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2021/trim_normalized_fps' # HIPS_2021
        else:
            print('no matched data')
        self.preprocessed = preprocessed
        self.split=split
        self.sampled=sampled
        self.fold=fold

        with open(self.root+f'/train_test_split_fold{self.fold}.json','r') as json_file:
            self.data_dict=json.load(json_file)

        self.npoints = decide_npoints(self.data_dict)
        
        assert (split == 'train' or split == 'test')
        self.datasize=len(self.data_dict[split]['LAI'])
        print('root:',self.root)
        print('json:', f'/train_test_split_fold{self.fold}.json')
    def __len__(self):
        return self.datasize

    def _get_item(self,index):
        if self.preprocessed==True:
            xyz=np.loadtxt(self.data_dict[self.split]['path'][index])
            LAI=np.float32(self.data_dict[self.split]['LAI'][index])
            # xyz_sampled=farthest_point_sample(xyz,self.npoints)
            # xyz_sampled=randomly_sample(xyz,self.npoints)
            path=self.data_dict[self.split]['path'][index]
            if self.sampled==False:
                xyz_sampled=xyz
                return xyz_sampled,LAI
            else:
                return xyz,LAI
        else: 
            print('write this part by yourself dude')
            quit()
    def __getitem__(self, index):
        return self._get_item(index)
class LASDataLoader_all(Dataset):
    def __init__(self,data,fold,split='train', preprocessed=True,sampled=True):
        super().__init__()
        assert (data=='HIPS_2020' or data== 'HIPS_2021')
        if data=='HIPS_2020':
            self.root='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2020/normalized_subsets_fps_4096' # HIPS_2020
        elif data=='HIPS_2021':
            self.root='/home/tirgan/a/huan1577/Pointnet_Pointnet2_pytorch/data/UAV/HIPS_2021/trim_normalized_fps' # HIPS_2021
        else:
            print('no matched data')
        self.preprocessed = preprocessed
        self.split=split
        self.sampled=sampled
        self.fold=fold

        with open(self.root+f'/all_train.json','r') as json_file:
            self.data_dict=json.load(json_file)

        self.npoints = decide_npoints(self.data_dict)
        
        assert (split == 'train' or split == 'test')
        self.datasize=len(self.data_dict[split]['LAI'])
        print('root:',self.root)
        print('json:', f'/all_train.json')
    def __len__(self):
        return self.datasize

    def _get_item(self,index):
        if self.preprocessed==True:
            xyz=np.loadtxt(self.data_dict[self.split]['path'][index])
            LAI=np.float32(self.data_dict[self.split]['LAI'][index])
            # xyz_sampled=farthest_point_sample(xyz,self.npoints)
            # xyz_sampled=randomly_sample(xyz,self.npoints)
            path=self.data_dict[self.split]['path'][index]
            if self.sampled==False:
                xyz_sampled=xyz
                return xyz_sampled,LAI
            else:
                return xyz,LAI
        else: 
            print('write this part by yourself dude')
            quit()
    def __getitem__(self, index):
        return self._get_item(index)

if __name__ == '__main__':
    import torch

    data = LASDataLoader_kfold(data='HIPS_2021', split='test',fold=0)
    DataLoader = torch.utils.data.DataLoader(data, batch_size=2, shuffle=False)
    ii=0
    for pts, LAI in DataLoader:
        # print(pts.shape)#(batchsize,number of points, xyz+otherfeatures)
        # print(LAI)
        ii+=1
        print(LAI)
        if ii==3:
            quit()
    
