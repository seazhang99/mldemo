import json
import cv2
import os
import zipfile

from scp_api_caller import *
from constants import *

def similarity_scoring(feature_files):
  if os.path.exists(tmp_feature_zip_file):
    os.remove(tmp_feature_zip_file)
  z = zipfile.ZipFile(tmp_feature_zip_file, 'w')
  for feature_file in feature_files:
    feature_file = feature_file.split('.')[0] + '.txt'
    z.write(tmp_folder + "/" + feature_file, os.path.basename(feature_file))
  z.close()
  url = urls['similarity-scoring']
  payload = {'options': '{"numSimilarVectors":%d}'%(len(feature_files) - 1)}
  files = {'files': open(tmp_feature_zip_file, 'rb')}
  response = call_api(url, payload, files = files)
  print(response)
  return response

def face_feature_extract(filename, saved_prefix, saved_folder = tmp_folder):
  filenames = []
  url = urls['face-feature-extract']
  img = cv2.imread(filename)
  files = {"files": open(filename, 'rb')}
  response = call_api(url, None, files = files)
  faces = json.loads(response)['predictions'][0]['faces']
  for index, face in enumerate(faces):
    features = face['face_feature']
    location = face['face_location']
    crop_img = img[int(location['top']):int(location['bottom']), int(location['left']):int(location['right'])]
    filename = "%s_%d.png"%(saved_prefix, index)
    cv2.imwrite(os.path.join(tmp_folder, filename), crop_img)
    feature_filename = filename.split(".")[0] + '.txt'
    feature_file = open(os.path.join(saved_folder, feature_filename), 'w')
    feature_file.write('[' + ','.join(str(x) for x in features) + ']')
    feature_file.close()
    filenames.append(filename)

  return filenames

def image_feature_extract(filename, saved_folder = tmp_folder):
  files = {"files": open(filename, 'rb')}
  url = urls['image-feature-extract']
  response = call_api(url, None, files = files)
  features = json.loads(response)['predictions'][0]['featureVectors']
  feature_filename = os.path.basename(filename).split(".")[0] + '.txt'
  feature_file = open(os.path.join(saved_folder, feature_filename), 'w')
  feature_file.write('[' + ','.join(str(x) for x in features) + ']')
  feature_file.close()

def face_detect(file_path, saved_prefix):
  filenames = []
  url = urls['face-detect']
  img = cv2.imread(file_path)
  files = {"files": open(file_path, 'rb')}
  response = call_api(url, None, files = files)
  faces = json.loads(response)['predictions'][0]['faces']
  for index, face in enumerate(faces):
    crop_img = img[int(face['top']):int(face['bottom']), int(face['left']):int(face['right'])]
    filename = "%s_%d.png"%(saved_prefix, index)
    cv2.imwrite(os.path.join(tmp_folder, filename), crop_img)
    filenames.append(filename)

  return filenames

def ocr(file_path):
  url = urls['ocr']
  files = {"files": open(file_path, 'rb')}
  options = {'options': '{"lang": "en,de,zh-Hans", "outputType": "txt", "pageSegMode": "1", "modelType": "lstmStandard"}'}
  return call_api(url, payload = options, files = files)

def detect_language(str):
  data = json.dumps({"message": str})
  return call_api(urls['lang-detect'], payload = data, files = None)

def translate_language(str, source_lang, target_lang, key):
    data = json.dumps({'sourceLanguage': source_lang, 'targetLanguages': [target_lang], 'units': [{'value': str, 'key': key}]})
    return call_api(urls['lang-translate'], payload = data, files = None)

def call_with_file(url_key, file_path, file_key = 'files'):
  url = urls[url_key]
  files = {file_key: open(file_path, 'rb')}
  return call_api(url, None, files = files)  

def call_with_data(url_key, data):
  url = urls[url_key]
  return call_api(url, data, None)

def translate_content(content, target_lang = 'en'):
  trans_strings = []
  paragraphs = content.split("\n")
  for index, paragraph in enumerate(paragraphs):
    print('Processing line %d...'%(index + 1))
    if len(paragraph) == 0:
      continue
    results = json.loads(detect_language(paragraph))
    if results.get('error') is None :
      source_lang = results['detections'][0]['langCode']
      if target_lang != source_lang:
        key = '%s-%d'%(paragraph, index)
        trans_string = json.loads(translate_language(paragraph, source_lang, target_lang, key))['units'][0]['translations'][0]['value']
      else:
        trans_string = paragraph
      trans_strings.append(trans_string)
  return "\n".join(trans_string for trans_string in trans_strings)

def ocr_and_translate(file_path, target_lang = 'en'):
  content = json.loads(ocr(file_path))['predictions'][0]
  print('OCR done.')
  trans_strings = translate_content(content, target_lang)

  return content, trans_strings
"""
image_path = '../../resources/Driving_License.jpg'
origin_filenames = face_feature_extract(image_path, 'face_from_origin')
print(origin_filenames)
image_path = tmp_folder + "/temp_img_webcam.png"
webcam_faces = face_feature_extract(image_path, 'face_from_webcam')
print(webcam_faces)
origin_filenames = ['face_from_origin_0.png', 'face_from_origin_1.png']
webcam_faces = ['face_from_webcam_0.png']
similarity_scoring(origin_filenames + webcam_faces)
"""

