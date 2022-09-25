from flask import Flask,send_file,send_from_directory,jsonify,request,make_response

app = Flask(__name__)

@app.route("/")
def home(): 
  response = make_response("Backend for Chordz")
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

if __name__ == '__main__':
    app.run()
