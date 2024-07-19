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
    


