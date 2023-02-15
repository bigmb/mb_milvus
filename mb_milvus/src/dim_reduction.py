## package for dim reduction of data

from sklearn.decomposition import PCA,KernelPCA
import numpy as np
from mb_pandas.src.dfload import load_any_df
import pandas as pd
from mb_utils.src.logging import logger
import ast
from scipy.spatial import distance as dist_scipy
from sklearn.manifold import TSNE
import umap


__all__ = ['distance_scipy','get_data','get_avg_per_label','get_distance_mean']

def distance_scipy(event1,event2):
    """
    Distance between two points
    Inputs:
        event1 : list of coordinates of the points
        event2 : list of coordinates of the points
    Returns:
        distance between the points
    """
    return dist_scipy.euclidean(event1,event2)


def get_data(df_np,label,ids=None,dim_type= 'pca',dim_comp =2, logger=None):
    """
    Get the data from the file
    Inputs:
        df_np : numpy array (numpy array) or list
        label : label of the data (list)
        ids : ids of the data (list)
        dim_type : dimensionality reduction type. Options are 'pca','tsne' and 'umap'. Default is 'pca'
        dim_comp : number of pca components , also can be tsne or umap components. Default is 2
        logger : logger
    Returns:
        data : dataframe
    """
    
    
    assert type(df_np) == np.ndarray or type(df_np) == list, 'df_np should be numpy array or list'
    assert dim_type in ['pca','tsne','umap'] , 'dim_type should be pca, tsne or umap'
    assert type(dim_comp) == int, 'dim_comp should be integer'
    assert type(label) == list, 'label should be list'

    if type(df_np) == np.ndarray:
        data = list(df_np)
    else:
        data = df_np
    

    if dim_type == 'pca':
        pca = PCA(n_components=dim_comp)
        pca_emb = pca.fit_transform(data)
    elif dim_type == 'tsne':
        tsne = TSNE(n_components=dim_comp, perplexity=15, random_state=42, init='random', learning_rate=200)
        pca_emb = tsne.fit_transform(np.array(data))
        #pca_emb = TSNE(n_components=dim_comp).fit_transform(list(data['embedding']))
    elif dim_type == 'umap':
        pca_emb = umap.UMAP(n_components=dim_comp).fit_transform(data)
    if logger:
        logger.info(pca_emb[:3])
    temp_pca = list(pca_emb)

    data_pd = pd.DataFrame()
    data_pd['original_embedding'] = data
    data_pd['embedding'] = temp_pca
    data_pd['taxcode'] = label
    if ids:
        data['event_id'] = ids
    
    if logger:
        df_unique_taxcode = data['taxcode'].unique()
        logger.info('Number of unique taxcodes {}'.format(len(df_unique_taxcode)))
    
    return data

def get_avg_per_label(df,logger=None):
    """
    Get the average of the data per label
    Inputs:
        df : dataframe
        logger : logger
    Returns:
        df_avg : dataframe
    """
    assert type(df) == pd.DataFrame, 'df should be pandas dataframe'
    assert 'taxcode' in df.columns, 'taxcode should be in the dataframe'
    assert 'embedding' in df.columns, 'embedding should be in the dataframe'

    df_unique_taxcode = df['taxcode'].unique()

    pca_mean = {}
    for taxcode in df_unique_taxcode:
        df_temp = df[df['taxcode']==taxcode]
        pca_mean[taxcode]  = np.mean(df_temp['pca_res'],axis=0)
    if logger:
        logger.info('Length of PCA avg dict : {}'.format(str(len(pca_mean))))
    return pca_mean

def get_distance_mean(dm1,dm2,dm_mean=False,logger=None):
    """
    Get the distance of the data from the average of the data per label
    Inputs:
        dm1 : dataframe , one whos avg. might me needed
        dm2 : dataframe
        logger : logger
    Returns:
        df : dataframe
    """

    assert type(dm1) == pd.DataFrame, 'dm1 should be pandas dataframe'
    assert type(dm2) == pd.DataFrame, 'dm2 should be pandas dataframe'
    assert 'taxcode' in dm1.columns, 'taxcode should be in the dataframe'
    assert 'embedding' in dm1.columns, 'embedding should be in the dataframe'
    assert 'taxcode' in dm2.columns, 'taxcode should be in the dataframe'
    assert 'embedding' in dm2.columns, 'embedding should be in the dataframe'

    df = pd.DataFrame()
    df['event_id'] = dm2['event_id']
    df['taxcode'] = dm2['taxcode']
    if dm_mean == True:
        pca_mean = get_avg_per_label(dm1,logger=logger)
    
    dist = []
    dist_1 = []
    for i in range(len(dm2)):
        dist_all = []
        for j in range(len(dm1)):
            if dm_mean == True:
                dist_all.append(distance_scipy(dm2['embedding'][i],pca_mean[dm1['taxcode'][j]]))
            else:
                dist.append(distance_scipy(dm2['embedding'][i],dm1['embedding'][j]))
        dist_1.append(dist_all)
    if sum(dist_all)==0:
        dist_f = dist_all
    else:
        dist_f = dist
    df['distance'] = dist_f

    if logger:
        logger.info('Length of df : {}'.format(str(len(df))))
    return df
