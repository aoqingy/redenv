## 本项目实现交大校友群微信红包自动统计
## 基于github项目chineocr

## 环境部署

wget https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh
bash ./Anaconda3-5.2.0-Linux-x86_64.sh -b -p /opt/conda/

修改~/.bashrc，在最后一行添加
export PATH="/opt/conda/bin:$PATH"

git clone https://github.com/chineseocr/chineseocr.git
cd chineseocr/
git clone https://github.com/pjreddie/darknet.git
conda create -n chineseocr python=3.6 pip scipy numpy jupyter ipython

git submodule init && git submodule update
pip install easydict opencv-contrib-python==4.0.0.21 Cython h5py lmdb mahotas pandas requests bs4 matplotlib lxml -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install -U pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install web.py==0.40.dev0
pip install keras==2.1.5 tensorflow==1.8
pushd text/detector/utils && sh make-for-cpu.sh && popd
conda install pytorch torchvision -c pytorch
#apt-get install -y python-qt4
#pip install opencv-python
pip install xlrd xlsxwriter
pip install pyecharts


For GPU:
pip install tensorflow-gpu==1.8
bash /root/cuda_10.0.130_410.48_linux.run --silent --toolkit
export PATH="/usr/local/cuda-10.0/bin:$PATH" #~/.bashrc
dpkg -i /root/libcudnn7_7.5.0.56-1+cuda10.0_amd64.deb
dpkg -i /root/libcudnn7-dev_7.5.0.56-1+cuda10.0_amd64.deb


修改darknet/python/darknet.py第48行
lib = CDLL("/root/chineseocr/darknet/libdarknet.so", RTLD_GLOBAL)
#vim darknet/python/darknet.py

修改darknet/Makefile前2行
GPU=1
CUDNN=1
OPENCV=0
OPENMP=0

pushd darknet/ && make && popd


## 下载模型文件   
模型文件地址: [baidu pan](https://pan.baidu.com/s/1gTW9gwJR6hlwTuyB6nCkzQ)
复制文件夹中的所有文件到models目录


## 生成统计
将当日红包截屏拷贝到sjtu相应日期（20190615）的目录下；
运行python redenv.py /root/chineseocr/sjtu/20190615；
复制生成的结果文件（在/root/chineseocr/sjtu目录下）。


## DOCKER
docker build -t redenv .
docker run -p 5900:5900 -v /root/redenv/sjtu:sjtu -it redenv /bin/bash
 
