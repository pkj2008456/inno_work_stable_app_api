from datetime import datetime
import urllib.request
import base64
import json
import time
import os
import requests
import cv2
import logging
from logging.handlers import RotatingFileHandler
import socket

# Set default socket timeout to 300 seconds
socket.setdefaulttimeout(300)

# Logger configuration
utils_logger = logging.getLogger('utils_logger')
utils_logger.setLevel(logging.INFO)

# Create log folder if it does not exist
log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)

# File handler for info and above
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_folder, 'utils.log')
file_handler = RotatingFileHandler(log_file_path, maxBytes=1*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)

# File handler for error and above
error_log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_folder, 'utils_error.log')
error_file_handler = RotatingFileHandler(error_log_file_path, maxBytes=1*1024*1024, backupCount=5)
error_file_handler.setLevel(logging.ERROR)

# Formatter for all handlers
formatter = logging.Formatter('utils_logger - %(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

# Add handlers to logger
utils_logger.addHandler(file_handler)
utils_logger.addHandler(error_file_handler)

# WebUI server URL and checkpoint configuration
webui_server_url = 'http://127.0.0.1:7860'
checkpoint = "Yuna_NOFACE.safetensors"
base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在的绝对路径
out_dir = os.path.join(base_dir, 'static', 'img')

# Output directories for text-to-image and image-to-image
out_dir_t2i = os.path.join(out_dir, 'txt2img')
out_dir_i2i = os.path.join(out_dir, 'img2img')
os.makedirs(out_dir_t2i, exist_ok=True)
os.makedirs(out_dir_i2i, exist_ok=True)

# Function to get the current timestamp
def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")

# Function to encode a file to base64
def encode_file_to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

# Function to decode base64 and save to a file
def decode_and_save_base64(base64_str, save_path):
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))
    delete_img()

# Function to delete old images, keeping only the most recent 100
def delete_img():
    try:
        img_path = os.path.join(out_dir, 'txt2img')
        utils_logger.info(f"Image path: {img_path}")

        all_files = os.listdir(img_path)
        txt2img_files = [f for f in all_files if f.startswith('txt2img-')]

        # Retain the most recent 100 files
        recent_files = sorted(txt2img_files, reverse=True)[:100]

        for f in all_files:
            if f not in recent_files:
                os.remove(os.path.join(img_path, f))
        
    except Exception as e:
        utils_logger.error(f"Cannot delete files: {e}")

# Function to call an API endpoint
def call_api(api_endpoint, method="post", **payload):
    headers = {'Content-Type': 'application/json'}
    url = f'{webui_server_url}/{api_endpoint}'
    try:
        response = requests.request(method, url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        utils_logger.error(f"Error during API call to {api_endpoint}: {e}")
        return None

# Function to set the checkpoint
def set_checkpoint(**data):
    new_checkpoint_name = data['payload']['override_settings']['sd_model_checkpoint']
    utils_logger.info(f"Setting checkpoint: {new_checkpoint_name}")
    option_payload = {"sd_model_checkpoint": new_checkpoint_name}
    call_api('/sdapi/v1/options', method='POST', **option_payload)

# Function to refresh checkpoints
def refresh():
    call_api('/sdapi/v1/refresh-checkpoints', method='POST')

# Function to get the list of models
def get_model_list():
    try:
        response = requests.get(f'{webui_server_url}/sdapi/v1/sd-models')
        response.raise_for_status()
        response_json = response.json()
        with open("model_list.json", "w") as f:
            json.dump(response_json, f, indent=4)
        return response_json
    except requests.exceptions.RequestException as e:
        utils_logger.error(f"Error occurred while getting model list: {e}")
        return None

# Function to get the current model
def get_current_model():
    try:
        response = requests.get(f'{webui_server_url}/sdapi/v1/options')
        response.raise_for_status()
        data = response.json()
        return data.get('sd_model_checkpoint', '')
    except requests.exceptions.RequestException as e:
        utils_logger.error(f"Error occurred while getting current model: {e}")
        return ''

# Function to call an API endpoint with a long timeout (just for text2img)
def call_api_2(api_endpoint, method="post", **payload):
    headers = {'Content-Type': 'application/json'}
    url = f'{webui_server_url}/{api_endpoint}'
    try:
        response = requests.request(method, url, json=payload, headers=headers, timeout=300)
        response.raise_for_status()
        utils_logger.info(f"==========================text2img responded: {response} =========================")
        return response.json()
    except requests.exceptions.RequestException as e:
        utils_logger.error(f"API call failed: {e}")
        return None
    except Exception as e:
        utils_logger.error(f"Unexpected error during API call: {e}")
        return None

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to get the reactor JSON configuration (for change face)
def get_reactor_json(reactor_img):
    bassae64 = base64.b64decode(reactor_img)
    basse64 = base64.b64encode(bassae64).decode('utf-8')
    model_dir = os.path.join(current_dir, '..', 'stable-diffusion-webui', 'models', 'insightface')
    model_path = os.path.join(model_dir, 'inswapper_128.onnx')
    
    reactor_json = {
        "args": [
            basse64, #0 Base64 encoded image
            True, #1 Enable ReActor
            '0', #2 Comma separated face number(s) from swap-source image
            '0', #3 Comma separated face number(s) for target image (result)
            model_path, #4 Model path
            'CodeFormer', #5 Restore Face: None; CodeFormer; GFPGAN
            1, #6 Restore visibility value
            True, #7 Restore face -> Upscale
            '4x_NMKD-Superscale-SP_178000_G', #8 Upscaler (type 'None' if doesn't need)
            1.5, #9 Upscaler scale value
            1, #10 Upscaler visibility (if scale = 1)
            False, #11 Swap in source image
            True, #12 Swap in generated image
            1, #13 Console Log Level (0 - min, 1 - med or 2 - max)
            0, #14 Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only)
            0, #15 Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only)
            False, #16 Save the original image(s) made before swapping
            0.1, #17 CodeFormer Weight (0 = maximum effect, 1 = minimum effect), 0.5 - by default
            False, #18 Source Image Hash Check, True - by default
            False, #19 Target Image Hash Check, False - by default
            "CUDA", #20 CPU or CUDA (if you have it), CPU - by default
            False, #21 Face Mask Correction
            0, #22 Select Source, 0 - Image, 1 - Face Model, 2 - Source Folder
            "elena.safetensors", #23 Filename of the face model (from "models/reactor/faces")
            "C:/PATH_TO_FACES_IMAGES", #24 The path to the folder containing source faces images
            None, #25 Skip it for API
            True, #26 Randomly select an image from the path
            True, #27 Force Upscale even if no face found
            0.6, #28 Face Detection Threshold
            2, #29 Maximum number of faces to detect (0 is unlimited)
        ]
    }
    return reactor_json

# Function to call the text-to-image API
def call_txt2img_api(controlnet_img_base64, reactor_img=None, **data): 
    able_control = data["able_controlnet"]["able_controlnet"]
    controlnet_img_base64 = controlnet_img_base64["control_pose"]
    image_path = os.path.join(current_dir, 'static', 'img', 'control_pose', controlnet_img_base64)
    result = {}

    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image at path {image_path} not found.")
        
        retval, bytes = cv2.imencode('.png', img)
        if not retval:
            raise ValueError("Image encoding failed.")
        
        controlnet_img_base64 = base64.b64encode(bytes).decode('utf-8')   
    except (FileNotFoundError, ValueError) as e:
        utils_logger.error(f"Error processing image: {e}")
        result['message'] = f"{controlnet_img_base64} can not find in back-end change the new one"
        controlnet_img_base64 =  os.path.join(current_dir, 'static', 'img', 'control_pose', '5.png')
    
    controlnet_api = {
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "enabled": able_control,
                        "image": controlnet_img_base64,
                        "module": "none",
                        "model": "control_v11p_sd15_openpose [cab727d4]",
                        "control_mode": "Balanced",
                        "weight": 2
                    }
                ]
            }
        }
    }
    
    data["payload"].update(controlnet_api)
    if reactor_img:
        utils_logger.info(f"==============================have reactor model=========================")
        reactor_json = get_reactor_json(reactor_img)
        utils_logger.info(f"Reactor JSON: {reactor_json}")
        data["payload"]["alwayson_scripts"]["reactor"] = reactor_json
    
    payload = data["payload"]
    del payload['override_settings']
    
    with open('test.json', 'w') as f:
        json.dump(payload, f, indent=4)
        utils_logger.info("Payload has been written to test.json")
    
    response = call_api_2('sdapi/v1/txt2img', method='POST', **payload)
    
    images = response.get('images', [])
    result_info = response.get("info", "{}")
    load_to_dict = json.loads(result_info)
    seed = {"seed": load_to_dict.get("seed")}
    utils_logger.info(f"Generated seed info: {seed}")
    
    result['images'] = images
    result["seed"]= seed
    for index, image in enumerate(images): # Save the images
        save_path = os.path.join(out_dir_t2i, f'txt2img-{timestamp()}-{index}.png')
        decode_and_save_base64(image, save_path)

    return result

# Function to call the image-to-image API
def call_img2img_api(**payload):
    response = call_api('sdapi/v1/img2img', **payload)
    images = response.get('images', [])
    result_info = response.get("info", "{}")
    load_to_dict = json.loads(result_info)
    seed = load_to_dict["seed"]
    
    result={
        "images":images,
        "seed":seed
    }
    utils_logger.info(json.dumps(result,indent=4))
    return result