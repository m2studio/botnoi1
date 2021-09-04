import os
from flask import Flask, flash, request, render_template
from datetime import datetime
import pickle
import botnoi as bn
from botnoi import cv

from PIL import Image

#UPLOAD_DIRECTORY = './images/'
UPLOAD_DIRECTORY = '/app/tmp/'
app = Flask(__name__)

model_file = 'cloud_predict.pickle'
model = pickle.load(open(model_file,'rb'))

@app.route('/')
def hello_world():
    return 'hello world'

def upload_form():
    with open('upload.html') as f:
        return f.read()

def get_description(cloud_type):
    switcher = {
        'altocumulus': 'Description 1',
        'altostratus': 'Description 2',
        'cirrocumulus': 'Description 3',
        'cirrostratus': 'Description 4',
        'cirrus': 'Description 5',
        'cumulonimbus': 'Description 6',
        'cumulus': 'Description 7',
        'nimbostratus': 'Description 8',
        'stratocumulus': 'Description 9',
        'stratus': 'Description 10',
    }
    return switcher.get(cloud_type, 'Unknown')

def get_image_path(cloud_type):
    switcher = {
        'altocumulus': '<img src="/static/clouds/altocumulus.png" width="400px" />',
        'altostratus': '<img src="/static/clouds/altostratus.png" width="400px" />',
        'cirrocumulus': '<img src="/static/clouds/cirrocumulus.png" width="400px" />',
        'cirrostratus': '<img src="/static/clouds/cirrostratus.png" width="400px" />',
        'cirrus': '<img src="/static/clouds/cirrus.png" width="400px" />',
        'cumulonimbus': '<img src="/static/clouds/cumulonimbus.png" width="400px" />',
        'cumulus': '<img src="/static/clouds/cumulus.png" width="400px" />',
        'nimbostratus': '<img src="/static/clouds/nimbostratus.png" width="400px" />',
        'stratocumulus': '<img src="/static/clouds/stratocumulus.png" width="400px" />',
        'stratus': '<img src="/static/clouds/stratus.png" width="400px" />',
    }
    return switcher.get(cloud_type, '<img src="/static/clouds/altocumulus.png" width="400px" />')

def test(filename):
    a = cv.image(filename)
    feat = a.getmobilenet()
    res = model.predict([feat])
    return str(res[0])

def read_predict_html():
    with open('prediction.html') as f:
        return f.read()

def get_predict_html(filename):
    # filename = './static/clouds/altocumulus.png'
    print('current directory : ' + os.getcwd())
    print('filename : ' + filename)

    if os.path.isdir(UPLOAD_DIRECTORY):
        print('directory : ' + UPLOAD_DIRECTORY + ' is exsited')
    else:
        print('directory : ' + UPLOAD_DIRECTORY + ' is NOT exsited')

    if os.path.isfile(filename):
        print('filename is existed')
    else:
        print('filename is NOT existed')

    try:
        img = Image.open(filename)
    except (IOError, SyntaxError) as e:
        print('Bad file : ' + filename)

    cloud_type = test(filename)    
    # cloud_type = 'nimbostratus' #fix the cloud type TODO: call model.predict with the given filename to get cloud_type
    description = get_description(cloud_type)
    predict_html = read_predict_html()
    predict_html = predict_html.replace('__PREDICTION__', cloud_type)
    image_path = get_image_path(cloud_type)
    predict_html = predict_html.replace('__IMAGE__', image_path)
    print('predict_html')
    print(predict_html)
    return predict_html

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/cloud', methods = ['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        print('file length : ' + str(len(request.files)))
        f = request.files['file']                
        print(f)
        current_time = datetime.now().strftime('%d-%b-%YT%H-%M-%S') # 1-Sep-2021T21-52-19
        filename = current_time + '_' + f.filename # 1-Sep-2021T21-52-19_cloud123.jpg
        f.save(UPLOAD_DIRECTORY + filename)

        predict_html = get_predict_html(UPLOAD_DIRECTORY + filename)
        content = upload_form().replace('__PREDICTION__', predict_html)

        # remove uploaded file after prediction to cleanup space
        # os.remove(UPLOAD_DIRECTORY + filename)

        return content, 201  # Return 201 CREATED

    return upload_form().replace('__PREDICTION__', '')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)