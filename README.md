# Flask Image Processing API

这是一个基于Flask的Web应用程序，提供图像上传、处理和控制图像生成功能。它利用了`txt2img` API和自定义图像处理功能。

## 目录

- [Flask Image Processing API](#flask-image-processing-api)
  - [目录](#目录)
  - [功能](#功能)
  - [安装](#安装)
  - [API文档](#api文档)

## 功能

- 上传图片
- 获取控制姿态图
- reactor change face
- 通过`txt2img` API生成图像
- 获取和设置模型检查点


## 安装
***if you not need to setup just ignore it and go to [API文档](#api文档)***

1.ensure you already install the stable diffusion webui and and setup the "--api"

1. **clone项目：**

   ```bash
   git clone https://github.com/pkj2008456/inno_work_stable_app_api.git
   cd inno_work_stable_app_api
   ```
2. Install `virtualenv`:
    ```bash
    $ pip install virtualenv
    ```
3. Open a terminal in the project root directory and run:
    ```
    $ virtualenv env
    ```
4. Then run the command:
    ```
    $ .\env\Scripts\activate
    ```
5. Then install the dependencies:
    ```
    $ (env) pip install -r requirements.txt
    ```
6. Finally start the web server:
    ```bash
    $ (env) python app.py   
    ```
## API文档
    >domain: `https://ai-generation.innocorn.xyz`

1. this endpoint is for text to img "https://ai-generation.innocorn.xyz/txt2img"
2.   the request sample below 
      ***(methods = post)***
   ```json
    {
    "able_controlnet": {
        "able_controlnet": true #use controlnet or not
    },
    "payload": {
        "prompt": "a south asian young adult others with white skin tone and an plus size body type, wearing a bohemian navy shirt dress leggings and white shoes, accessorized with a necklace,with long brown hair",
        "negative_prompt": "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4),(deformed, distorted, disfigured:1.3),poorly drawn,bad anatomy,wrong anatomy,extra limb,missing limb,floating limbs,disconnected limbs,mutation,mutated,ugly,disgusting,amputation,watermark text,",
        "seed": 1,
        "steps": 20,
        "width": 720,
        "height": 720,
        "cfg_scale": 5,
        "sampler_name": "DPM++ 2M",
        "n_iter": 1,
        "batch_size": 1,#how many gen photo you want
        "override_settings": {
            "sd_model_checkpoint": "realisticVisionV60B1_v51HyperVAE"
        }
    },
    "control_pose": {
        "control_pose": "2.jpg"#if able_controlnet is false just dont change it
    },
    "reactor_img": { #if dont want to change the face just delete whole key
        "reactor_img": "static/img/face\\upload-Damian_2_1.jpeg"
    }
}
```
***return***
```json
{
    Gen_base64:"string"
}
```





