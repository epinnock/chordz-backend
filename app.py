from flask import Flask,send_file,send_from_directory,jsonify,request,make_response
from omnizart.chord import app as capp
from pytube import YouTube
import os
import csv
import json

cache = {}

def csv_to_json(filename):
  csvfile = open(filename, 'r')
  fieldnames = ("chord","start","end",)
  reader = csv.DictReader( csvfile, fieldnames)
  json_array = []
  next(reader, None)  # skip the headers
  for row in reader:
      json_array.append(row)
  return {"chord_segments":json_array}

def transformToChord(file,name):
  capp.transcribe(file,output="./songs/"+name)

def get_chords_csv_file(youtube_link):
  # url input from request 
  yt = YouTube(youtube_link)

  #extract audio stream notice videos can have multiple audio streams we are just grabbing the first one
  audio = yt.streams.filter(only_audio=True).first()
  destination = './songs'
  
  # download the file
  out_file = audio.download(output_path=destination)
  transformToChord(out_file,yt.title)
  print(yt.title + " has been successfully downloaded. 1")

  # result of success
  return "./songs/{}".format(yt.title)

def get_from_cache(youtube_link):
  if(youtube_link not in cache.keys()):
    csv_filepath = get_chords_csv_file(youtube_link)
    cache[youtube_link]=csv_filepath
  return cache[youtube_link]

app = Flask(__name__)

@app.route("/")
def home(): 
  response = make_response("Backend for Chordz on gCloud")
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response
'''flask endpoint
  @param ytl= string youtube link
  @response [{chord:string,start:float,stop:float}]
'''
@app.route("/yt")
def yt(): 
    yt_link = request.args.get('ytl')
    try:
      response = jsonify(csv_to_json(get_from_cache(yt_link)))
      response.headers.add("Access-Control-Allow-Origin", "*")
      return response
    except FileNotFoundError:
      abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
    get_from_cache("https://www.youtube.com/watch?v=ozUZBCSfl9c")

