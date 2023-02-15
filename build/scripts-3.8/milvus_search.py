#!python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 03:01:28 2021

@author: malav
"""

## importing libs

import pandas as pd
import os
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import pymilvus
import glob
import numpy as np
from mb_milvus.src.milvus_extraction import FeatureExtractor, batch_create
import argparse
from mb_utils.src.logging import logger


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def main():
    
    #defining the variables
    path_loc = args.path_loc 
    batch_size=args.batch_size
    collection_name = args.collection_name
    field_name = args.collection_name
    no_of_images = args.num ##no of images to search
    logging = args.logging
    if logging == 'True':
        logger = logger
    else:
        logger = None
    
    t1 =glob.glob(path_loc+'*')
    t1_im =path_loc+'images_fea'
    t1_names = os.listdir(path_loc)

    i=0
    for i in range(len(t1)):
        if t1[i]==t1_im:
            if logger:
                logger.info('removing the name of images_fea from the list')
            else:
                print('removing the name of images_fea from the list')
            t1_im_i = i

    t1.pop(t1_im_i);
    t1_names.pop(t1_im_i);
 
    ## Creating a folder for storing embeddings

    path_fea = path_loc + 'images_fea'
    if os.path.exists(path_fea)==True:
        if logger:
            logger.info("File already exists")
        else:
            print("File already exists")
    else:
        try:
            os.mkdir(path_fea)
        except OSError:
            if logger:
                logger.info("Creation of the directory %s failed" % path_fea)
            else:
                print("Creation of the directory %s failed" % path_fea)
        else:
            if logger:
                logger.info("Successfully created the directory %s" % path_fea)
                logger.info("Extracting all the features now")
            else:
                print("Successfully created the directory %s" % path_fea)
                print("Extracting all the features now")


    t2_names=[]
    t2_extract_file=[]
    t2_extract_name=[]
    t2_emb = os.listdir(path_fea+'/')
    i=0
    for i in range(len(t2_emb)):
        t2_temp = t2_emb[i][:-8]
        t2_names.append(t2_temp)

    for j in range(len(t1_names)):
        if t1_names[j] not in t2_names:
            t2_extract_file.append(t1[j])
            t2_extract_name.append(t1_names[j])

    if logger:
        logger.info(f"Files left to extract : {len(t2_extract_name)}")
    else:
        print(f"Files left to extract : {len(t2_extract_name)}")

    ##Feature extraction
    batches = batch_create(t2_extract_file,batch_size)
    batches_names= batch_create(t2_extract_name,batch_size)

    if len(batches)!=0:
        if logger:
            logger.info('extracting the image files')
        else:
            print('extracting the image files')
        fea_extract = FeatureExtractor('ResNet50')
        fea_extract.batch_extract(batches,batches_names,batch_size,write_to=path_fea)

    t3_emb = glob.glob(path_fea+'/*')
    t3_names=[]
    t3_emb_data=[]
    t3_names_dict={}
    for k in range(len(t3_emb)):
        t3_temp = np.load(t3_emb[k])
        t3_names.append(t3_emb[k][:-8])
        t3_emb_data.append(t3_temp)
        t3_names_dict[t3_names[k]]=k
    
    t3_values=list(t3_names_dict.values())
    ##Calling milvus
    connections.connect("default", host='localhost', port='19530')
    if logger:
        logger.info('Connections Establised with Milvus')
    else:
        print('Connections Establised with Milvus')

    ##Search
    if logger:
        logger.info('Searching the images')
    else:
        print('All extracted and Milvus connected')
    dim = len(t3_emb_data[0])

    #checking if the collection is created
    list_of_collections = pymilvus.utility.get_connection().list_collections()
    if logger:
        logger.info('list of collections : {}'.format(list_of_collections))
    else:
        print('list of collections : {}'.format(list_of_collections))
  
    if collection_name in list_of_collections:
        if logger:
            logger.info('collection name already exists. Pick another because I was lazy and didnt write the code to add a partition or remove and create a new one')
            logger.info('If you need it, let me know by creating an issue and I will add it in a day.')
        else:
            print('collection name already exists. Pick another because I was lazy and didnt write the code to add a partition or remove and create a new one')
            print('If you need it, let me know by creating an issue and I will add it in a day.')
    
    event_id_field = FieldSchema(name="id", dtype=DataType.INT64, description="id_location",is_primary=True)
    field = FieldSchema(name=field_name, dtype=DataType.FLOAT_VECTOR, dim=dim)
    schema = CollectionSchema(fields=[event_id_field,field],auto_id=False,description="event_munet UM Model collection")
    collection = Collection(name=collection_name, schema=schema)  
    if logger:
        logger.info('new collection created')
    else:
        print('new collection created')
    list_of_collections = pymilvus.utility.get_connection().list_collections()
    if logger:
        logger.info('list of collections : {}'.format(list_of_collections))
    else:
        print('list of collections : {}'.format(list_of_collections))
    entities = [t3_values,t3_emb_data]
    
    mr = collection.insert(entities)
    if logger:
        logger.info('inserted entities')
        logger.info('mr : {}'.format(mr))
        logger.info('mr.primary_keys[:10] : {}'.format(mr.primary_keys[:10]))
    else:    
        print(mr)
        print(mr.primary_keys[:10])
    #pymilvus.utility.get_connection().flush([collection_name])

    index_param = {
            "metric_type":"L2",
            "index_type":"IVF_FLAT",
            "params":{"nlist":1024}
            }
    collection.create_index(field_name=field_name, index_params=index_param)
    if logger:
        logger.info('index created')
        logger.info('index params : {}'.format(collection.index().params))
    else:
        print(collection.index().params)
    search_params = {"metric_type": "L2", "params": {"nprobe": 50}}
    #collection.release()
    collection.load()


    xbc=[]
    for i in range(len(t3_emb_data)):
        xbc.append(list(t3_emb_data[i]))
    
    
    if logger:
        logger.info('Starting Search for complete file')
    else:
        print('Starting Search for complete file')
    results = collection.search(xbc[:],field_name,param=search_params,limit=no_of_images,expr=None)

    res_ids = []
    res_dis = []
    for i in range(len(t3_names)):
        res_ids.append(results[i].ids)
        res_dis.append(results[i].distances)

    if logger:
        logger.info('Search Done. Adidng results to csv')
    else:
        print("Search Done. Adidng results to csv")

    res_names=[]
    for l in range(len(res_ids)):
        res_temp_val=[]
        for m in range(len(res_ids[l])):
            for name, ids in t3_names_dict.items():    
                if ids==res_ids[l][m]:
                    res_temp_val.append(name)
        res_names.append(res_temp_val)
    
    res_csv = pd.DataFrame(columns=['img_name'],data=list(t3_names_dict.keys()))
    res_csv['similar_ids'] = res_names
    res_csv['distance'] = res_dis
    
    res_csv.to_csv(args.save_csv)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-path_loc', type=str, default='/home/malav/Desktop/images/',
                        help="Image folder location. Default '/home/malav/Desktop/images/'.")
    parser.add_argument('-collection_name', type=str, default='first_collection',
                        help="Collection name. Should be same as the field name. Default 'first_collection'")
    parser.add_argument('-num', type=int, default='10',
                        help="number of images to save in results. Default '10'")
    parser.add_argument('-batch_size',type=int,default='8',
                        help="Batch size for extracting images. Default='8'")
    parser.add_argument('-save_csv',type=str,default='/home/malav/Desktop',
                        help="Final CSV file save location. Default='/home/malav/Desktop'")
    parser.add_argument('-logging',type=bool,default=False,help='logging tool for logger msgs. Uses mb_utils.src.logging. Default=False')
    args = parser.parse_args()

    try:
        main()
    except (RuntimeError, TypeError, NameError) as error:
        print(error)


