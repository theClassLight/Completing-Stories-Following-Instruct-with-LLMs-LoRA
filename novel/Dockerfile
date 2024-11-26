FROM dockerproxy.net/nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

LABEL com.uxhao.image.authors="ahaoao"

LABEL com.uxhao.image.cooperation="VX:SystemUA"



ENV TZ=Asia/Shanghai \

    DEBIAN_FRONTEND=noninteractive \

    PATH=/opt/miniconda3/bin:$PATH



WORKDIR /root



RUN cp /etc/apt/sources.list /etc/apt/sources.list.back && rm -rf /etc/apt/sources.list  && echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse \ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse \ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse \ndeb http://security.ubuntu.com/ubuntu/ noble-security main restricted universe multiverse \n" >> /etc/apt/sources.list  



RUN apt-get update

RUN apt-get upgrade -y



RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ssh \

 && mkdir /var/run/sshd  && echo 'root:root' |chpasswd \

 && sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config  \

 && sed -i 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config



RUN apt install -y tzdata \

 && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \

 && echo ${TZ} > /etc/timezone \

 && dpkg-reconfigure --frontend noninteractive tzdata



RUN apt-get install -y vim && apt-get install -y git && apt-get install -y net-tools



RUN echo "service ssh start >>/root/start_ssh.log" >> ~/start_ssh.sh \

 && chmod 777 ~/start_ssh.sh \

 && echo "# <<< ssh <<< \nif [ -f /root/start_ssh.sh ]; then \n      /root/start_ssh.sh \nfi \n# <<< ssh <<<" >> ~/.bashrc \

 && echo '#! /bin/bash\na=$(netstat -anp |grep 6006) \nif [ -z "$a" ] \nthen \nsource /opt/miniconda3/etc/profile.d/conda.sh \nconda activate cv \nnohup python /opt/miniconda3/envs/cv/lib/python3.10/site-packages/tensorboard/main.py --logdir /gemini/logs --bind_all > /root/start_tensorboard.log 2>&1 & \nfi' >> ./start_tensorboard.sh \

 && chmod 777 ~/start_tensorboard.sh \

 && echo "# <<< tensorboard <<< \nif [ -f /root/start_tensorboard.sh ]; then \n      /root/start_tensorboard.sh \nfi \n# <<< tensorboard <<<" >> ~/.bashrc



RUN wget -O /opt/Miniconda3-py310_24.3.0-0-Linux-x86_64.sh "https://mirrors.bfsu.edu.cn/anaconda/miniconda/Miniconda3-py310_24.3.0-0-Linux-x86_64.sh" \

 && chmod +x /opt/Miniconda3-py310_24.3.0-0-Linux-x86_64.sh \

 && sh -c '/bin/echo -e "\nyes\n\nyes" | sh /opt/Miniconda3-py310_24.3.0-0-Linux-x86_64.sh -b -p /opt/miniconda3'

ENV PATH=/opt/miniconda3/bin:$PATH



RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \

 && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \

 && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ \

 && conda config --set show_channel_urls yes \

 && conda config --set auto_activate_base no  \

 && conda config --set ssl_verify false



RUN conda create --name cv python=3.10.13

SHELL ["/bin/bash","--login", "-c"]

RUN export PATH=/opt/miniconda3/bin:$PATH \

 && conda update --name base conda \

 && conda init bash \

 && source activate \

 && conda activate cv \

 && conda install -y --quiet numpy pyyaml mkl mkl-include setuptools cmake cffi typing \

 && conda install -y --quiet -c mingfeima mkldnn \

 && python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \

 && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \

 && pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu118 \

 && pip install pydantic pandas pillow matplotlib comet_ml openpyxl opencv-python torchmetrics lightning scikit-learn scikit-image albumentations segmentation-models-pytorch tensorboard easydict packaging timm einops yarl typing_extensions



RUN apt-get install -y ffmpeg libsm6 libxext6

RUN mkdir /gemini && mkdir /gemini/code && mkdir /gemini/output

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 22

EXPOSE 6006

EXPOSE 8888



CMD ["bash"]