# Image-Similarity-Search-Milvus
Image Similarity search build on Milvus 

## 1. Getting Started

Clone the repo:

  ```bash
  git clone https://github.com/bigmb/Image-Similarity-Search-Milvus.git
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
Running the search file
```
./milvus_search.py -path_loc "path_to_img_folder" -num "number of simliar images" -batch_size "Extraction batch size if needed" -collection_name "name_of_the_collection"
```
