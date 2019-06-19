FROM ubuntu:16.04
MAINTAINER aoqingy

RUN sed -i "s/archive\.ubuntu\.com/mirrors\.aliyun\.com/g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install apt-utils && \
    apt-get autoclean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install supervisor && \
    apt-get autoclean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/supervisor && \
    mkdir -p /etc/supervisor/conf.d

ADD supervisor.conf /etc/supervisor.conf
ADD startup.sh /usr/sbin/startup.sh

RUN apt-get update ;\
    apt-get -y upgrade ;\
    apt-get install -y x11vnc ;\
    apt-get autoclean -y && apt-get autoremove -y ;\
    rm -rf /var/lib/apt/lists/*

COPY startvnc.sh /usr/sbin/startvnc.sh
COPY x11vnc.sv.conf /etc/supervisor/conf.d/

RUN apt-get update ;\
    apt-get -y upgrade ;\
    apt-get install -y wget bzip2 ;\
    apt-get autoclean -y && apt-get autoremove -y ;\
    rm -rf /var/lib/apt/lists/*

RUN wget https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh --directory-prefix=/tmp/

RUN bash /tmp/Anaconda3-5.2.0-Linux-x86_64.sh -b -p /opt/conda/ && \
    rm /tmp/Anaconda3-5.2.0-Linux-x86_64.sh && \
    echo "export PATH=/opt/conda/bin:$PATH" >> /root/.bashrc

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get autoclean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

#RUN /opt/conda/bin/pip install python=3.6 pip
#scipy numpy jupyter ipython
#RUN /opt/conda/bin/pip install easydict opencv-contrib-python==4.0.0.21 Cython h5py lmdb mahotas pandas requests bs4 matplotlib lxml -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN /opt/conda/bin/pip install -U pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/
#RUN /opt/conda/bin/pip install web.py==0.40.dev0
RUN /opt/conda/bin/pip install keras tensorflow
#RUN /opt/conda/bin/pushd text/detector/utils && sh make-for-cpu.sh && popd
#RUN /opt/conda/bin/conda install pytorch torchvision -c pytorch
RUN /opt/conda/bin/pip install xlrd xlsxwriter
RUN /opt/conda/bin/pip install pyecharts
RUN /opt/conda/bin/pip install opencv-python
RUN /opt/conda/bin/pip install torch

RUN apt-get update ;\
    apt-get -y upgrade ;\
    apt-get install -y vim ;\
    apt-get autoclean -y && apt-get autoremove -y ;\
    rm -rf /var/lib/apt/lists/*

ENV LANG C.UTF-8

RUN mkdir /opt/redenv
COPY darknet /opt/redenv/darknet
COPY models /opt/redenv/models
COPY apphelper /opt/redenv/apphelper
COPY crnn /opt/redenv/crnn
COPY text /opt/redenv/text
COPY tools /opt/redenv/tools
COPY train /opt/redenv/train
COPY config.py /opt/redenv/config.py
COPY model.py /opt/redenv/model.py
COPY main.py /opt/redenv/main.py
#ADD redenv.tar.gz /opt/
#ENTRYPOINT ["/bin/bash", "/usr/sbin/startup.sh"]

