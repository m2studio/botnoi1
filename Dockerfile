# FROM python:3.6-buster
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .
# CMD ["python", "app.py"]

# FROM ubuntu:latest
# RUN apt-get update -y
# RUN apt-get install -y python3-pip python3-dev build-essential
# COPY . /app
# WORKDIR /app
# COPY requirements.txt .
# RUN pip3 install tensorflow-cpu==2.6.0
# RUN pip3 install keras==2.6.0
# RUN pip3 install Keras-Preprocessing==1.1.2
# RUN pip3 install Pillow==7.1.2
# RUN pip3 install scikit-learn==0.22.2.post1
# RUN pip3 install -r requirements.txt
# CMD ["python3", "app.py"]

FROM python:3.7.11-buster
COPY . /app
WORKDIR /app
COPY docker-requirements.txt .
RUN pip install tensorflow==2.4.3
RUN pip install keras==2.4.3
RUN pip install Pillow==7.1.2
RUN pip install scikit-learn==0.22.2.post1
RUN pip install h5py==2.10.0
RUN pip install -r docker-requirements.txt
CMD ["python", "app.py"]

# FROM floydhub/tensorflow:2.4-gpu.cuda10cudnn7-py3_aws.57
# COPY . /app
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install tensorflow==2.6.0
# RUN pip install keras==2.6.0
# RUN pip install Keras-Preprocessing==1.1.2
# RUN pip install Pillow==7.1.2
# RUN pip install -r requirements.txt
# CMD ["python", "app.py"]