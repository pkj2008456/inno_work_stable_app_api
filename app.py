import os
from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify, session
from utils import call_txt2img_api, set_checkpoint, refresh, get_current_model, encode_file_to_base64, call_img2img_api, get_model_list
import json
from werkzeug.utils import secure_filename
import secrets
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = 'static/img/face'
app.secret_key = secrets.token_hex(32)

log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)
# Logger configuration
log_file_path = os.path.join(app.root_path,log_folder, 'flask_app.log')
error_log_file_path = os.path.join(app.root_path,log_folder, 'flask_error.log')

logger = logging.getLogger('flask_app')
logger.setLevel(logging.INFO)

# File handler for info and above
file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)

# File handler for error and above
error_file_handler = RotatingFileHandler(error_log_file_path, maxBytes=5*1024*1024, backupCount=5)
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
    response = jsonify({'error': 'An internal error occurred.'})
    response.status_code = 500
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    logger.error(f"Method Not Allowed: {str(e)}", exc_info=True)
    response = jsonify({'error': 'Method Not Allowed'})
    response.status_code = 405
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['faceUpload']
    if file.filename == '':
        update_message = 'No file selected.'
    else:
        filename = f"upload-{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session["file_path"] = filepath
        logger.info(f"File saved, session: {session.items()}")
        update_message = 'File uploaded successfully.'
    return jsonify({'update_message': update_message, 'file_path': filepath})

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
    logger.info(request.method)
    if request.method == 'POST':
        logger.info("Into POST")
        data = request.get_json(force=True)
        logger.info(f"Data received: {data}")
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
        # logger.info(f"Text2Img data: {text2img_data}")
        return jsonify(text2img_data)
    else:
        logger.info("GET request to /txt2img")
        message = "Don't request GET"
        return jsonify({'message': message})

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
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
