import glob,os
#Library for dataframe
from pandas import DataFrame, read_csv
import csv
#Library for PDF + Merge
from PyPDF2 import PdfFileReader,PdfFileWriter
from PyPDF2 import PdfFileMerger
#Library for connetion to AWS
import boto3
import botocore
import pandas as pd
#Library for plotting the data
import matplotlib
import datetime as dt
matplotlib.use('Agg')
import boto, os
import matplotlib.pylab as plt
import numpy as np
import sys
import json
from scipy import signal
import pyedflib
import os
from datetime import datetime
import time
import logging
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.backends.backend_pdf
from itertools import islice, chain
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime
from boto.s3.connection import S3Connection
channel_info = []
data_list = []

#Creditonals 
AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXX'
#Bucket Name
bucket_name = 'XXXXXXXXXXXXXXXXXXXX'
merger = PdfFileMerger()
# connect to the bucket
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
#Connect to dataebase
dynamodb = boto3.resource('dynamodb',region_name='XXXXXXXXXXXXXXXXXXXX')
table = dynamodb.Table('XXXXXXXXXXXXXXXXXXXX')
#Connection to bucket
bucket = conn.get_bucket(bucket_name)
#Current Date and time
now = datetime.datetime.now()
#Grabs all data from bucket
s3client = boto3.client("s3")
s3 = boto3.resource('s3')
# download file into current directory
BUCKET_NAME = 'XXXXXXXXXXXXXXXXXXXX'
#for file in files:
try:
    s3.Bucket(BUCKET_NAME).download_file('PATH/TO/FILE', 'FILE')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

i=0
count=0
count1=0
#Look for any of the files related to the raw data
for filename in glob.glob('FILE'):
    c=canvas.Canvas(filename[:10]+"S.pdf", pagesize=letter)
    c.fontSize=15
    test_data_file = os.path.join('.', filename[:10]+'.edf')
    f = pyedflib.EdfWriter(test_data_file,7,file_type=pyedflib.FILETYPE_EDFPLUS)
    meta = pd.read_csv(filename,sep='\n',header=[0,1])
    df = pd.read_csv(filename, skiprows=2)
    #df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    #Saves the results into a PDF file
    with PdfPages(filename[:10]+'Scored.pdf',"wb") as pdf:
           #Plots all of raw data
	   fig1=plt.figure()
           #Subplot only does 3 at a time
           ax4=fig1.add_subplot(3,1,1)
           ax5=fig1.add_subplot(3,1,2)
           ax6=fig1.add_subplot(3,1,3)
           #Leave title empty or else titel and y-axis will overlap
           ax4=df.plot(x=df['Time'], y='Temp',figsize=(12,6),title="",ax=ax4)#.get_figure()
	   ax5=df.plot(x='Time', y='Heart',figsize=(12,6),title="",ax=ax5)#.get_figure()
           ax6=df.plot(x='Time', y='Oxy',figsize=(12,6),title="",ax=ax6)#.get_figure()
           fig2=df.plot(x='Time', y='AirFlow',figsize=(12,6),title='AirFlow').get_figure()
           #Leave this here for some reason it takes any extra and plot it inside Body Position Graph 
	   pdf.savefig(fig2)
           fig=plt.figure()
           #Allows Below to be ploted in a single graph
           ax=plt.gca()
           fig=df.plot(x='Time', y='X',figsize=(12,6),title='X-Axis',ax=ax).get_figure() 
           df.plot.line(x='Time', y='Y',figsize=(12,6),title='Y-Axis',ax=ax).get_figure()
	   df.plot.line(x='Time', y='Z',figsize=(12,6),title='Z-Axis',ax=ax).get_figure()
           #Is the sum of X Y Z 
           df['BSum']=df['X']+df['Y']+df['Z']
           df.plot.line(x='Time', y='BSum',figsize=(12,6),title='Z-Axis',ax=ax).get_figure()
           #Save Graph onto PDF file Header
           head=list(islice(meta,3))
           #Starts data results
           c.drawString(10,780,str(head)+'  Duration: '+str(df['Time'].max()))
           c.setFont("Times-Roman",12)
           c.drawString(10,764,'Patient ID:__________')
           c.drawString(125,764,'Date of Birth:___/___/______')
           c.drawString(10,749,'Address:___________________________________Zip:_________City:__________')
           c.drawString(275,764,'Height:________Weight:________  Age:____')
           c.drawString(425,749,'Phone Number:____-____-________')
           c.line(0,730,1000,729)
           c.setFont("Times-Roman" ,20)
           c.drawString(10,715,'Body Temperature')
           c.setFont("Times-Roman",10)
           c.drawString(10,700,'Max Temperature: '+str(df['Temp'].max()))
           c.drawString(10,685,'Min Temperature: '+str(df['Temp'].min()))
           c.drawString(10,670,'Average Temperature: '+str(df['Temp'].median()))
           c.drawString(150,700,'Time it hit above 100F: '+str((df['Temp'] >= 100).values.sum()))
           c.drawString(150,685,'Time it hit below 80F: '+str((df['Temp'] <= 80).values.sum()))
           c.line(0,650,1000,650)
           c.setFont("Times-Roman" ,20)
           c.drawString(10,635,'Pulse')
           c.setFont("Times-Roman",10)
           c.drawString(10,620,'Max Heart Beat: '+str(df['Heart'].max()))
           c.drawString(10,605,'Min Heart Beat: '+str(df['Heart'].min()))
           c.drawString(10,590,'Average Heart Beat: '+str(df['Heart'].median()))
           c.drawString(150,620,'Time it hit above 100 bpm: '+str((df['Heart'] >= 100).values.sum()))
           c.drawString(150,605,'Time it hit below 40 bpm: '+str((df['Heart'] <= 40).values.sum()))
           c.line(0,575,1000,575)
           c.setFont("Times-Roman" ,20)
           c.drawString(10,560,'Oxygen Saturation (Sp02)')
           c.setFont("Times-Roman",10)
           c.drawString(10,545,'Max Oxygen Rate: '+str(df['Oxy'].max()))
           c.drawString(10,530,'Min Oxygen Rate: '+str(df['Oxy'].min()))
           c.drawString(150,545,'Time it hit above 700: '+str((df['Oxy'] >= 700).values.sum()))
           c.drawString(150,530,'Time it hit below 300: '+str((df['Oxy'] <= 300).values.sum()))
           c.drawString(10,515,'Average Oxygen Rate: '+str(df['Oxy'].median()))
           c.line(0,500,1000,500)
           c.setFont("Times-Roman" ,20)
           c.drawString(10,485,'Body Position')
           c.setFont("Times-Roman",10)
           c.drawString(10,470,'Total Time of each position ')
           back_time=((-20<df['Y']) & (df['Y']<20)).values.sum()
           back_time=back_time%60
           front_time=((-60>df['Y']) | (df['Y']>60)).values.sum()
           front_time=back_time%60
           left_time=((-60<df['Y']) & (df['Y']<-20)).values.sum()
           left_time=back_time%60
           right_time=((20<df['Y']) & (df['Y']<60)).values.sum()
           right_time=back_time%60
           c.drawString(10,455,'Back: '+str(((-20<df['Y']) & (df['Y']<20)).values.sum())+'s')
           c.drawString(10,440,'Front: '+str(((-60>df['Y']) | (df['Y']>60)).values.sum())+'s')
           c.drawString(10,425,'Left Side: '+str(((-60<df['Y']) & (df['Y']-20)).values.sum())+'s')
           c.drawString(10,410,'Right Side: '+str(((20<df['Y']) & (df['Y']<60)).values.sum())+'s')
           #Saves all the data into the PDF document
           c.save()
           pdf.savefig(fig1)
           pdf.savefig(fig)
    #Start of creation of EDF file
    ch_dict = {'label': 'Body Tempurature', 'dimension': 'F', 'sample_rate': 200, 'physical_max': 130, 'physical_min': 60, 'digital_max': 32767, 'digital_min': -32768, 'transducer': '', 'prefilter':''}
    #Put Channel info into EDF+C
    channel_info.append(ch_dict)
    #Puts data into EDF+C
    data_list.append(df['Temp'])
    #Input Channel Basic info
    ch_dict = {'label': 'Heart Rate', 'dimension': 'BMP', 'sample_rate': 200, 'physical_max': 150, 'physical_min': 0, 'digital_max': 32767, 'digital_min': -32768, 'transducer': '', 'prefilter':''}
    #Put Channel info into EDF+C
    channel_info.append(ch_dict)
    #Puts data into EDF+C
    data_list.append(df['Heart'])
    #Input Channel Basic info
    ch_dict = {'label': 'Oxygen Rate', 'dimension': 'F', 'sample_rate': 200, 'physical_max': 150, 'physical_min': 0, 'digital_max': 32767, 'digital_min': -32768, 'transducer': '', 'prefilter':''}
    #Put Channel info into EDF+C
    channel_info.append(ch_dict)
    #Puts data into EDF+C
    data_list.append(df['Oxy'])
    #Input Channel Basic info
    ch_dict = {'label': 'AirFlow', 'dimension': 'F', 'sample_rate': 200, 'physical_max': 150, 'physical_min': 0, 'digital_max': 32767, 'digital_min': -32768, 'transducer': '', 'prefilter':''}
    #Put Channel info into EDF+C
    channel_info.append(ch_dict)
    #Puts data into EDF+C
    data_list.append(df['AirFlow'])
    #Input Channel Basic info
    ch_dict = {'label': 'Body Position', 'dimension': 'degree', 'sample_rate': 200, 'physical_max': 150, 'physical_min': 0, 'digital_max': 32767, 'digital_min': -32768, 'transducer': '', 'prefilter':''}
    #Put Channel info into EDF+C
    channel_info.append(ch_dict)
    #Puts data into EDF+C
    data_list.append(df['X'])
    channel_info.append(ch_dict)
    data_list.append(df['Y'])
    channel_info.append(ch_dict)
    data_list.append(df['Z'])    
    #Writes Header to EDF
    f.setSignalHeaders(channel_info)
    #Writes data into EDF
    f.writeSamples(data_list)    
    channel_info = []
    data_list = []
    f.close
    del f
    #Combine the Graph and Results PDF together
    filenames=[filename[:10]+'S.pdf',filename[:10]+'Scored.pdf']
    for filename1 in filenames:
        merger.append(PdfFileReader(file(filename1, 'rb')))
    #Merges them
    merger.write(filename[:10]+'Final.pdf')
    #Insert File Status to Database
    table.put_item(
            Item={
                 'Patient File': filename[:10]+'Final.pdf',
                 'Status':"Complete",
                 'Date':now.strftime("%Y-%m-%d %H:%M")
            }
           )
    s3 = boto3.client('s3')
    bucket_name = 'snooze2'
    bucket = conn.get_bucket(bucket_name)
    #Uploads data to S3 Bucket
    s3.upload_file(filename[:10]+'.edf','snooze2', filename[:10]+'.edf')
    s3.upload_file(filename[:10]+'Final.pdf','snooze2', filename[:10]+'Final.pdf')
    s3.upload_file(filename,'snooze2', filename)
    #Removes excess documents
    os.remove(filename[:10]+'Final.pdf')
    os.remove(filename[:10]+'Scored.pdf')
    os.remove(filename[:10]+'.edf')
    os.remove(filename[:10]+'S.pdf')
    #Delete anything downloaded from S3 recently
    os.remove(filename)
 
