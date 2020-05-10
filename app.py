from __future__ import unicode_literals
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask import send_file
from lxml import etree
import urllib.request
import lxml
import youtube_dl
import os

app = Flask(__name__)
Bootstrap(app)

lis = []

@app.route('/')
def hello_world():
    cwd = os.getcwd()
    test=os.listdir(cwd)
    for item in test:
        if item.endswith(".webm"):
            os.remove(item)
    return render_template("index.html")


def makeName(video_title):
    str=''
    for i in video_title:
        str=str+i
        str=str+'-'
    return str[:len(str)-1]

def editName(name):
                fname=name.replace("|"," ")
                return fname


@app.route('/geturl', methods = ['POST', 'GET'])
def geturl():
    global url
    global video_title

    if request.method == 'POST':
        url = request.form["url"]
        lis[0]=url
        youtube = etree.HTML(urllib.request.urlopen(url).read())
        video_title = youtube.xpath("//span[@id='eow-title']/@title")
        lis[1]=video_title
        print(''.join(video_title))
        vt=makeName(video_title)
        et=editName(vt)
        return render_template("title.html",data=et)

def success():
                return render_template("success.html")


def vdownload():
    global path
    video_title = lis[1]
    url=lis[0]
    name = makeName(video_title)+'.webm'
    fname= editName(name)
    download_options = {
            'format' : 'bestaudio/best',
            'outtmpl' : '/'+fname,


            'postprossessors' : [{
                'key' : 'FFmpegExtractAudio',
                'prefferedcodec' : 'mp3',
                'prefferedquality' : '192',
            }],
        }
    if url=="":
                pass
    else:
        with youtube_dl.YoutubeDL(download_options) as dl:
            dl.download([url])
        path = fname


@app.route('/download', methods = ['POST','GET'])
def download():
    vdownload()
    if(path!=""):
        return send_file(path, as_attachment=True)
    return render_template("success.html")
