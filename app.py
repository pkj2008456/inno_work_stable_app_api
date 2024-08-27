import os
from flask import Flask, url_for, request, redirect, make_response, jsonify, session,abort
from utils import call_txt2img_api, set_checkpoint, refresh, get_current_model, encode_file_to_base64, call_img2img_api, get_model_list
import json
from werkzeug.utils import secure_filename
import secrets
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
# from db import db  
from models import User, Image 
from auth_utils import check_password
import socket
socket.setdefaulttimeout(300)


app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Desktop\\test1.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = 'static/img/face'
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024


PASSWORD = '9WUCV45bUUnZ4s%xy*gaN@GZuUZrwK%uv#uf-kYR4Xs6p$4mBH#2E3K=dG85u!Ax'



log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)
# Logger configuration
log_file_path = os.path.join(app.root_path,log_folder, 'flask_app.log')
error_log_file_path = os.path.join(app.root_path,log_folder, 'flask_error.log')

logger = logging.getLogger('flask_app')
logger.setLevel(logging.INFO)

# File handler for info and above
file_handler = RotatingFileHandler(log_file_path, maxBytes=1*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)

# File handler for error and above
error_file_handler = RotatingFileHandler(error_log_file_path, maxBytes=1*1024*1024, backupCount=5)
error_file_handler.setLevel(logging.ERROR)

# Formatter for all handlers
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(error_file_handler)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
    error_message = str(e)
    response = jsonify({'jimmy_error': 'An internal error occurred.', 'error': str(error_message)})
    response.status_code = 500
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    logger.error(f"Method Not Allowed: {str(e)}", exc_info=True)
    error_message = str(e)
    response = jsonify({'jimmy_error': 'Method Not Allowed','error' : {error_message}})
    response.status_code = 405
    return response
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File is too large"}), 413

import base64

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['faceUpload']
    
    if file.filename == '':
        update_message = 'No file selected.'
        return jsonify({'update_message': update_message}), 400
    
    # 读取文件内容并进行Base64编码
    file_data = file.read()
    encoded_file = base64.b64encode(file_data).decode('utf-8')
    
    update_message = 'File uploaded and encoded successfully.'
    return jsonify({'update_message': update_message, 'encoded_file': encoded_file})

@app.route('/get_control_pose', methods=["GET"])
def get_control_pose():
    img_folder = os.path.join('static', 'img', 'control_pose')
    result = []
    for root, dirs, files in os.walk(img_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, 'static')
                result.append({"path": relative_path})
    return jsonify(result)

@app.route('/')
def hello():
    return redirect('/txt2img', code=302)

@app.route("/get_model_list", methods=["GET"])
def get_model():
    model_list = get_model_list()  # 获取模型列表数据
    return jsonify(model_list)

@app.route("/setCheckPoint", methods=["POST"])
def set_checkpoint_route():
    try:
        logger.info("In the setCheckpoint route")
        data = request.get_json(force=True)
        logger.info(f"Received data: {data}")
        if not data or 'payload' not in data or 'override_settings' not in data['payload']:
            raise ValueError("Invalid data format")
        refresh()
        set_checkpoint(**data)
        current_model = get_current_model()
        logger.info(f"Checkpoint set: {current_model}")
        return jsonify({'message': 'Checkpoint set successfully', 'current_model': current_model})
    except Exception as e:
        logger.error(f"Error in setCheckpoint route: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/txt2img', methods=['GET', 'POST'])
def index():
    logger.info(f"Request method: {request.method}")

    data = request.get_json(force=True)
    password = data.get('password')
    logger.info(password)
    if password and PASSWORD == password:
        if request.method == 'POST':
            logger.info("Into POST")
            data = request.get_json(force=True)

            refresh()
            set_checkpoint(**data)
            current_model = get_current_model()
            logger.info(f"Current model: {current_model}")
            control_pose = data["control_pose"]
            logger.info(f"Control pose: {control_pose}")
            reactor_img = data.get("reactor_img", {}).get("reactor_img", None)
            if 'reactor_img' in data:
                del data['reactor_img']
            logger.info(f"Data after removing reactor_img: {data}")
            text2img_data = call_txt2img_api(control_pose, reactor_img, **data)
            with open('testapi/text2img_data.json','w') as f:
                json.dump(text2img_data,f,indent=4)
                logger.info("already gen to text2img_data.json")
                
            return jsonify(text2img_data)
        else:
            logger.info("GET request to /txt2img")
            message = "Don't request GET"
            return jsonify({'message': message})
    else:
        logger.warning(f"Unauthorized access attempt with no valid password token provided.")
        return jsonify({'error': 'Unauthorized access'}), 401


@app.route("/img2img", methods=["POST"])
def img2img():
    data = request.get_json()
    
    #for log testa
    key_to_exclude = 'init_images'
    log_show = {k:v for k , v in data.items() if k != key_to_exclude}
    log_show = json.dumps(log_show,indent=4)
    logger.info(f"Received data for img2img: {log_show} Remain: there is init_images include it but I deleted")
    
    if not data or 'init_images' not in data:
        return jsonify({'error': 'Invalid data provided'}), 400
    try:
        images_base64 = call_img2img_api(**data)
        logger.info('img2img process done')
        return jsonify({'images': images_base64}), 200
    except Exception as e:
        logger.error(f"Error in img2img: {e}")
        return jsonify({'jimmy_error': f'Internal Server Error{str(e)}'}), 500

# with app.app_context():
#     db.create_all()
    
if __name__ == '__main__':

    from waitress import serve
    serve(app, host='0.0.0.0', port=8080, channel_timeout=60000,channel_backlog=100)
