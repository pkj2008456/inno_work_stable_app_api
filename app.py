import os
from flask import Flask,render_template,url_for,request,redirect,make_response,jsonify,session
from utils import call_txt2img_api,set_checkpoint,refresh,get_current_model,encode_file_to_base64,call_img2img_api,get_model_list
import json
from werkzeug.utils import secure_filename
import secrets
from flask_cors import CORS
import logging


app = Flask(__name__)
CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
# app.logger.info(os.path.join(os.path.dirname(os.path.abspath(__file__)), '/templates'))
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = 'static/img/face'
app.secret_key = secrets.token_hex(32)
log_file_path = os.path.join(app.root_path, 'flask_app.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.errorhandler(Exception)
def handle_exception(e):

    app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
    

    response = jsonify({'error': 'An internal error occurred.'})
    response.status_code = 500
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    app.logger.error(f"Method Not Allowed: {str(e)}", exc_info=True)
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
        app.logger.info(f"save,session:{session.items()}")
        update_message = 'File uploaded successfully.'
    
    return jsonify({'update_message': update_message,'file_path': filepath})


@app.route('/get_control_pose', methods=["GET"])
def get_control_pose():
    # app.logger.info("geted")
    img_folder = os.path.join('static', 'img', 'control_pose')
    # img_folder = os.path.join(app.root_path)

    image_files = [f for f in os.listdir(img_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_paths = [os.path.join('img', 'control_pose', f) for f in image_files]
    image_base64 = [encode_file_to_base64(os.path.join(img_folder, f)) for f in image_files]
    result = [{"path": path, "base64": base64_str} for path, base64_str in zip(image_paths, image_base64)]
        
    jsonify(result)
    # app.logger.info(f"======================={type(result)}=================================")
    return result    

@app.route('/')
def hello():
    
    return redirect('/txt2img',code=302)

@app.route("/get_model_list",methods = ["get"])
def get_model():
    model_list = get_model_list()  # 获取模型列表数据
    return jsonify(model_list)
    
@app.route("/setCheckPoint", methods=["POST"])
def set_checkpoint_route():
    try:
        app.logger.info("in the setcheckpoint route")
        data = request.get_json(force=True)
        app.logger.info(f"Received data: {data}")
        # Verify data format
        if not data or 'payload' not in data or 'override_settings' not in data['payload']:
            raise ValueError("Invalid data format")

        refresh()
        set_checkpoint(**data)
        current_model = get_current_model()
        app.logger.info(f"done to set checkpoint: {current_model}")
        return jsonify({'message': 'Checkpoint set successfully', 'current_model': current_model})

    except Exception as e:
        app.logger.error(f"Error in setCheckpoint route: {e}")
        return jsonify({'error': str(e)}), 400

    
@app.route('/txt2img', methods=['GET', 'POST'])
def index():
    app.logger.info(request.method)
    if request.method == 'POST':        
        app.logger.info("into post")

        data = request.get_json(force=True)
        app.logger.info(f"================={data}==================")
        refresh()
        set_checkpoint(**data)
        current_model = get_current_model()
        app.logger.info(f"Current model: {current_model}")
        control_pose = data["control_pose"]
        
        app.logger.info(f"========================contorl_pose:{control_pose}===================")
        
            
        reactor_img = data.get("reactor_img", {}).get("reactor_img", None)

        if 'reactor_img' in data:             
            del data['reactor_img']
            
        app.logger.info(f"------------------------------{data}--------------------")
        Gen_base64 = call_txt2img_api(control_pose,reactor_img,**data)
        # app.logger.info(Gen_base64)
        pass_json = json.dumps({"Gen_base64":Gen_base64})
        app.logger.info(f"======================this is Gen_base64:{pass_json}================")
        # app.logger.info(pass_json)
        return pass_json
    else:
        app.logger.info("this is get txt2img")
        message = "dont request get"
        return json.dumps({message:message})
        # return render_template('index.html')
    
@app.route("/img2img", methods=["POST"])
def img2img():
    data = request.get_json()
    app.logger.info(f"Received data for img2img: {data}")

    # 验证数据
    if not data or 'init_images' not in data:
        return jsonify({'error': 'Invalid data provided'}), 400

    # 调用 utils.py 中的 call_img2img_api 函数
    try:
        images_base64 = call_img2img_api(**data)
        app.logger.info(f'img2img_done')
        return jsonify({'images': images_base64}), 200
    except Exception as e:
        app.logger.error(f"Error in img2img: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500



# if __name__ == "__main__":
#     app.run(threaded=False,process = 3)
#     #app.run(debug=True)
if __name__ == '__main__':
        from waitress import serve  
        serve(app, host='0.0.0.0', port=8080)