# Image-Similarity-Search-Milvus
Image Similarity search build on Milvus.
Get similar images from the dataset. Can be used for augmentation, diffusion models and finding similar patterns in images.  

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fbigmb%2FImage-Similarity-Search-Milvus&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## 1. Getting Started

Clone the repo:

  ```bash
  git clone https://github.com/bigmb/mb_milvis.git
  ```
  
## 2. Requirements

```
python>=3.6
numpy
pymilvus==2.0.0rc7
tensorflow
pandas
glob
argparse
cv2
pathlib
PIL

```
Install all dependent libraries:
  ```bash
  pip install -r requirements.txt
  ```
## 3. Run the file

Make sure you have the milvus 2.0.0rc7 docker-compose file and then Milvus docker running. (Refer to: https://milvus.io/docs/v2.0.0/install_standalone-docker.md)
```
wget https://github.com/milvus-io/milvus/releases/download/v2.0.0-rc7/milvus-standalone-docker-compose.yml -O docker-compose.yml
```
Start the docker container using
```
docker-compose up -d
```

Image embedings extraction methods available:
[Resnet, Xception,VGG16,VGG19,InceptionV3, MobileNet]
Default : Resnet


Running the search file
```
./milvus_search.py -path_loc "path_to_img_folder" -num "number of simliar images" -batch_size "Extraction batch size if needed" -collection_name "name_of_the_collection" -save_csv "Saving location of the final CSV output"
```

## 4. Running video

https://user-images.githubusercontent.com/14040051/143135715-b0d6461c-e63f-40c2-869a-6331e826d9a4.mp4


