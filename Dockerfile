# Dockerize Python Flask app and deploy to Heroku
# https://medium.com/analytics-vidhya/dockerize-your-python-flask-application-and-deploy-it-onto-heroku-650b7a605cc9

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