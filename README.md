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
>domain: `https://ai-generation.innocorn.xyz`/'34.90.139.98:8080'

1. this endpoint is for text to img "https://ai-generation.innocorn.xyz/txt2img"
-   the request sample below 
      ***(methods = post)***
   ```json    
{
    able_controlnet: { able_controlnet: true },
    payload: {
        prompt: 'extreme detail description , monochrome background , highly detailed , physically-based rendering ,ultra-fine painting ,a south asian young adult female with rosie skin tone and an plus size body type, accessorized with a nothings,wearing a bohemian warm tones mini dress leggings and white loafers, bob haircut hair , blonde hair colors, ',
        negative_prompt: "(deformed iris,deformed pupils, foot don't grasp some things , semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4),(deformed, distorted, disfigured:1.3),poorly drawn,bad anatomy,wrong anatomy,extra limb,missing limb,floating limbs,disconnected limbs,mutation,mutated,ugly,disgusting,amputation,watermark text, , moving, <knees bending:10> , bending knees , hand carry somethings",
        seed: '-1',
        steps: 25,
        width: '620',
        height: '880',
        cfg_scale: 2,
        sampler_name: 'DPM++ 2M',
        n_iter: 1,
        batch_size: 1,
        override_settings: {
        sd_model_checkpoint: 'realisticVisionV60B1_v51HyperVAE',
        sd_vae: 'Karras'
        }
    },
    control_pose: { control_pose: '5.png' },
    reactor_img: { #if dont want to change the face just delete whole key
        reactor_img:"base64" },
    password: '9WUCV45bUUnZ4s%xy*gaN@GZuUZrwK%uv#uf-kYR4Xs6p$4mBH#2E3K=dG85u!Ax'
}
 
```
***return***
```json
{
    "images":["base64_string","base64_string"],
    "seed":{
        seed:int_num
    },
    "message":"warning message" #for cant find the control net 
}
```
___
2. for img to img
- **/img2img", methods=["POST"]**
- request
  ```
  data = {
        "prompt": "1girl, blue hair",
        "seed": 1,
        "steps": 20,
        "width": 512,
        "height": 512,
        "denoising_strength": 0.5,#the lager the value,the less like the original image.The max value is one
        "n_iter": 1,
        "init_images": [example_base64_image],
        "batch_size": 1 # num of gen_img
    }
    ```
    ```
- respone
```
{
    "images": [
        "base64_String"
    ]
}
```
___
3. set the check point
- ("/setCheckPoint", methods=["POST"])
  
**request**
```
  #the data may be are json:data['payload']['override_settings']['sd_model_checkpoint']
  #e.g (js)
  document.getElementById("test").addEventListener("click", () => {
    let payload = {
        "override_settings": {
            'sd_model_checkpoint': "realisticVisionV60B1_v51HyperVAE"  //this can use to switch sd model waiREALCN_v70 or realisticVisionV60B1_v51HyperVAE
        }
    };
    let data = { payload };
    fetch("https://ai-generation.innocorn.xyz/setCheckPoint", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
```
**return**

```
{current_model:"string",
message:"checkpoint set successfully"}
```
___
4. get_model_list (in case on you dont know what model you can change)
- ("/get_model_list",methods = ["get"])
  
**return**(model_name may use on set_check_point)

```
[
    {
        "title": "chilloutrealistic_v21.safetensors [e114478c02]",
        "model_name": "chilloutrealistic_v21",
        "hash": "e114478c02",
        "sha256": "e114478c0212307077585e2cca0c3aa71180f52784d7b54944431249f8f827d9",
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\chilloutrealistic_v21.safetensors",
        "config": null
    },
    {
        "title": "hanfu.safetensors",
        "model_name": "hanfu",
        "hash": null,
        "sha256": null,
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\hanfu.safetensors",
        "config": null
    },
    {
        "title": "hanfuSong_v35.safetensors",
        "model_name": "hanfuSong_v35",
        "hash": null,
        "sha256": null,
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\hanfuSong_v35.safetensors",
        "config": null
    },
    {
        "title": "orientalGoddess_001LCM.safetensors",
        "model_name": "orientalGoddess_001LCM",
        "hash": null,
        "sha256": null,
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\orientalGoddess_001LCM.safetensors",
        "config": null
    },
    {
        "title": "realisticVisionV60B1_v51HyperVAE.safetensors [f47e942ad4]",
        "model_name": "realisticVisionV60B1_v51HyperVAE",
        "hash": "f47e942ad4",
        "sha256": "f47e942ad4c30d863ad7f53cb60145ffcd2118845dfa705ce8bd6b42e90c4a13",
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\realisticVisionV60B1_v51HyperVAE.safetensors",
        "config": null
    },
    {
        "title": "v1-5-pruned-emaonly.safetensors",
        "model_name": "v1-5-pruned-emaonly",
        "hash": null,
        "sha256": null,
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\v1-5-pruned-emaonly.safetensors",
        "config": null
    },
    {
        "title": "wdr_realisti_hanfu.safetensors",
        "model_name": "wdr_realisti_hanfu",
        "hash": null,
        "sha256": null,
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\wdr_realisti_hanfu.safetensors",
        "config": null
    },
    {
        "title": "Yuna_NOFACE.safetensors [50329e6356]",
        "model_name": "Yuna_NOFACE",
        "hash": "50329e6356",
        "sha256": "50329e635601f4a44b62dbf010d3b6681a3fbd64e5c6fd00d5aa1a7f5e1356f1",
        "filename": "C:\\stable_diffusion_app\\stable-diffusion-webui\\models\\Stable-diffusion\\Yuna_NOFACE.safetensors",
        "config": null
    }
]
```
   




