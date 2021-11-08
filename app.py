import os
import string
import time
import urllib.request
from flask import Flask,flash, request, redirect, url_for, render_template
from flask_session import Session
from google.cloud import storage
from flask_session import Session

from keras.models import model_from_json
from pytube import YouTube
from werkzeug.utils import secure_filename
import boto3
import get_label
import get_recom
import numpy as np

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# app.secret_key = "New App"
sess = Session()

UPLOAD_FOLDER = 'static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 120 * 1024 * 1024

bucket=os.getenv('S3_BUCKET')    
s3_key=os.getenv('S3_KEY')       
s3_secret=os.getenv('S3_SECRET')  
s3_location =os.getenv('S3_LOCATION')   


@app.route('/')
def upload_form():
    return render_template('new_index.html')



@app.route('/', methods=['POST'])
def upload_video():

    url = request.form.get('file')
    if url == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
        fileurl = secure_filename(url)
        filename = YouTube(url).streams.get_by_itag(22).download()
    
        #print('upload_video filename: ' + filename)
        flash('Video successfully uploaded and displayed below')
        s3 = boto3.client('s3',aws_access_key_id=s3_key,
                  aws_secret_access_key= s3_secret)
        
        name = str(filename).replace(r"C:\Users\Akshara\Terra Digital\Demo","")
        exp = "\\"
        name = "".join(ch for ch in name if ch not in exp)
        s3.upload_file(Bucket= bucket,
        Filename = filename,
        Key = name)
        
        transcribe = boto3.client('transcribe',aws_access_key_id=s3_key,
        aws_secret_access_key=s3_secret)
        job_name = "transcription_job"+ str(np.random.randint(0,99999))
        job_uri = "s3://uploadedfiletranscripts/"+str(name)
        transcribe.start_transcription_job(
               TranscriptionJobName=job_name,
               Media={'MediaFileUri': job_uri},
               MediaFormat='mp4',
               OutputBucketName = "uploadedfiletranscripts",
               LanguageCode='en-US'
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
    
        time.sleep(5)
        classification = get_label.get_type(job_name)
        recom = get_recom.choose_recom(classification)


    #eturn new_url
    return render_template('new_index.html', filename=fileurl,output=classification,recom = recom)
    

@app.route('/display/<filename>')
def display_video(filename):
    v = str(filename).replace("https_www.youtube.com_watchv","")
    new_url = "https://www.youtube.com/embed/" + v
    return redirect(str(new_url))



if __name__ == '__main__':
    
    app.secret_key = "some key"
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(host='127.0.0.1', port=8080, debug=True)


