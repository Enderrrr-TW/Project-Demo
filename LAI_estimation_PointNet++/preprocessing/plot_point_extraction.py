from os import mkdir
import numpy as np
import pandas as pd
import json
from matplotlib.path import Path
import laspy
import os
'''
Get points within the plot boundary
'''
output_folder='E:/Ender/data/UAV/HIPS_2021/with_ground_points'
input_las='E:/Ender/data/UAV/HIPS_2021/subset/20210816_f42m_india_44m.las'
input_json='E:/Ender/data/UAV/HIPS_2021/20210617_india_f42mYS_HIPS_1cm_manshrink.geojson'
try: os.mkdir(output_folder)
except: pass
def read_json(input_json):
    with open(input_json) as j:
        v=json.load(j)
    # print(v['features'][0]['geometry']['coordinates'][0][0])
    # print((v['features'][0]))

    df=dict()
    df['plot_number']=[]
    df['row_ID']=[]
    df['x0']=[]
    df['x1']=[]
    df['x2']=[]
    df['x3']=[]
    df['y0']=[]
    df['y1']=[]
    df['y2']=[]
    df['y3']=[]
        
    for i in range(len(v['features'])):
        df['plot_number'].append(v['features'][i]['properties']['plot'])
        df['row_ID'].append(v['features'][i]['properties']['row'])
        df['x0'].append([v['features'][i]['geometry']['coordinates'][0][0][0]])
        df['x1'].append([v['features'][i]['geometry']['coordinates'][0][1][0]])
        df['x2'].append([v['features'][i]['geometry']['coordinates'][0][2][0]])
        df['x3'].append([v['features'][i]['geometry']['coordinates'][0][3][0]])
        df['y0'].append([v['features'][i]['geometry']['coordinates'][0][0][1]])
        df['y1'].append([v['features'][i]['geometry']['coordinates'][0][1][1]])
        df['y2'].append([v['features'][i]['geometry']['coordinates'][0][2][1]])
        df['y3'].append([v['features'][i]['geometry']['coordinates'][0][3][1]])
    df=pd.DataFrame(df)
    # print(max(set(df['plot_number'])))
    return df
def main():
    las=laspy.read(input_las)
    # print(las.header)
    xy=np.vstack([las.x,las.y]).transpose()
    xyz=np.vstack([las.x,las.y,las.z]).transpose()

    df=read_json(input_json)
    # df = df[df['plot_number']>4350] # df for HIPS_2021
    
    plots=set(df['plot_number'])
    for i in range(min(plots),max(plots)+1):
        subset_df=df[df['plot_number']==i]

        for k in range((len(subset_df['x0']))):
            tupVerts=[(subset_df['x0'].iloc[k][0],subset_df['y0'].iloc[k][0]),  # (1)
                    (subset_df['x1'].iloc[k][0],subset_df['y1'].iloc[k][0]),     # (2)
                    (subset_df['x2'].iloc[k][0],subset_df['y2'].iloc[k][0]), # (3)
                    (subset_df['x3'].iloc[k][0],subset_df['y3'].iloc[k][0])]              
            p = Path(tupVerts)
            if k==0:
                grid = p.contains_points(xy)
            else:
                temp_grid=p.contains_points(xy)
                grid=np.logical_or(grid, temp_grid)
        xyz_sub=xyz[grid]

        subset_las=laspy.LasData(laspy.LasHeader(version="1.3", point_format=3))
        subset_las.x=xyz_sub[:,0]
        subset_las.y=xyz_sub[:,1]
        subset_las.z=xyz_sub[:,2]
        output_name=output_folder+'/20210816_'+str(i)+'.las'
        subset_las.write(output_name)
if __name__ == '__main__':
    main()