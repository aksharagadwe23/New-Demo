import os
import io
import re
import time
import json
import nltk
import boto3
from flair.models import TextClassifier

from nltk.corpus import stopwords

from flair.data import (
    Sentence,
    Corpus,
    FlairDataset,
    DataPair,
)
from dotenv import load_dotenv

load_dotenv()
bucket=os.getenv('S3_BUCKET')    
s3_key=os.getenv('S3_KEY')       
s3_secret=os.getenv('S3_SECRET')  
s3_location =os.getenv('S3_LOCATION')   


nltk.download('words')
nltk.download('stopwords')
words = set(nltk.corpus.words.words())
stop_words = set(stopwords.words('english'))
stop_words.remove('how')
stop_words.remove('where')
stop_words.remove('when')
stop_words.remove('who')
stop_words.remove('what')
stop_words.remove('which')
stop_words.remove('whom')

label_dict = {'0':'How-to',
              '1' : 'Review',
              '2': 'Interview or Q/A',
              '3':'Events'}


def clean(text):
    text = text.lower()
    text = re.sub("mhm","",text)
    text = re.sub("hmm","",text)
    text = re.sub("yeah","",text)
    text = re.sub("'m"," am",text)
    text = re.sub("'s"," is",text)
    text = re.sub("'ll"," will",text)
    text = re.sub("'ve"," have",text)
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join(w for w in nltk.wordpunct_tokenize(text)
         if w in words )
    text = " ".join(w for w in nltk.wordpunct_tokenize(text)
         if w not in stop_words)
    text = ' '.join(text.split())
    return text



def get_type(filename):

    s3 = boto3.resource(service_name='s3',aws_access_key_id=s3_key,
        aws_secret_access_key=s3_secret)
    obj = s3.Bucket('uploadedfiletranscripts').Object(filename+".json").get()
    temp = json.loads(obj['Body'].read().decode('utf-8'))
    text = temp['results']['transcripts'][0]['transcript']

    clean(text)
    classifier=TextClassifier.load("final-model.pt")
    
    sentence = Sentence(text)
    classifier.predict(sentence)
    pred=sentence.labels[0].value

    return label_dict[str(pred)]