from flask import Flask, jsonify, redirect, render_template, request
import requests
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import io
from glob import glob

from constants import *
from scp_api_functions import *

app = Flask(__name__)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(save_folder, file_param = 'files'):
  if file_param not in request.files:
    return json.dumps({'Error': 'Needs file parameter'})
  file = request.files[file_param]
  if file.filename == '':
    return json.dumps({'Error': 'No file selected'})
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(save_folder, filename))
    file.close()
  return file.filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autotag')
def auto_tag():
  return render_template('auto_tag_demo.html', api_key = apikey)

@app.route('/recieptrecog')
def reciept_recognition():
  return render_template('reciept_recognition_demo.html', api_key = apikey)

"""
@app.route('/demo2')
def demo2():
  return render_template('text_classification_demo.html', api_key = apikey)

@app.route('/demo3')
def demo3():
  return render_template('language_detection_demo.html', api_key = apikey)

@app.route('/demo4')
def demo4():
  return render_template('translation_demo.html', api_key = apikey)
"""

@app.route('/translateservice')
def translate_service():
  return render_template('translate_service_demo.html', api_key = apikey)

@app.route('/facerecognize')
def face_recognize():
  return render_template('face_recognize_demo.html', api_key = apikey)

@app.route('/recieptdetect', methods=['POST'])
def recieptdetect_detection():
  file_name = save_file(tmp_folder)
  file_path = os.path.join(tmp_folder, file_name)
  return call_with_file('scene-text-recognition', file_path)

@app.route('/facedetect', methods=['POST'])
def face_detection():
  photo = request.files['photo']
  in_memory_file = io.BytesIO()
  photo.save(in_memory_file)
  data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
  img = cv2.imdecode(data, cv2.IMREAD_COLOR)
  cv2.imwrite(os.path.join(tmp_folder, 'temp_img_webcam.png'), img)
  filenames = request.form['faces'].split(',')
  faces = face_feature_extract(os.path.join(tmp_folder, 'temp_img_webcam.png'), 'face_from_webcam')
  response = similarity_scoring(filenames + faces)
  ret = json.dumps({'face-from-origin': filenames, 'face-from-webcam': faces, 'response': json.loads(response)})
  return ret

@app.route('/idupload', methods=['POST'])
def id_upload():
  file_name = save_file(tmp_folder)
  filenames = face_feature_extract(os.path.join(tmp_folder, file_name), 'face_from_origin')
  return json.dumps({'name': file_name, 'faces': filenames})

@app.route('/ocrtrans', methods=['POST'])
def ocr_trans():
  file_name = save_file(tmp_folder)
  target_lang = request.form['target-lang']
  content, trans_strings = ocr_and_translate(os.path.join(tmp_folder, file_name), target_lang)
  return json.dumps({'ocr_content': content, 
                     'translate_content': trans_strings})

@app.route('/contenttrans', methods=['POST'])
def content_trans():
  content = request.form['content']
  target_lang = request.form['target-lang']
  trans_strings = translate_content(content, target_lang)
  return json.dumps({'translate_content': trans_strings})

@app.route('/langdetect', methods=['POST'])
def language_detect():
  text = request.form['text']
  detect_language(text)
  return json.dumps({'result': 'Done'})

@app.route('/refreshprod', methods=['POST'])
def refresh_production():
  files = glob(benz_library + "/*")
  for file in files:
    file_ext = os.path.basename(file).split('.')[1].lower()
    if file_ext == 'jpg' or file_ext == 'png':
      image_feature_extract(file, benz_library)
  return json.dumps({'Results': 'Done'})

@app.route('/imageclassfication', methods=['POST'])
def image_classification():
  file_name = save_file(tmp_folder)
  file_path = os.path.join(tmp_folder, file_name)
  response = json.loads(call_with_file('image-classification', file_path))
  return json.dumps({'name': os.path.basename(file_name), 'response': response})

@app.route('/apicallwithdata', methods=['POST'])
def apicallwithdata():
  url_key = request.args.get('api')
  data = request.get_data()
  return call_with_data(url_key, data)

port = int(os.getenv("PORT", 5000))
if __name__ == '__main__':
  if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)
  app.run(debug = True, host='0.0.0.0', port=port)