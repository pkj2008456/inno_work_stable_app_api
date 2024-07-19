let base64String = "";
document.addEventListener("DOMContentLoaded", function () {
    let generateButton = document.getElementById("generateButton");
    generateButton.addEventListener("click", function () {
        let promptOutput = "";
        let prompt = document.getElementById("prompt-bubble-area");
        let allSelection = prompt.querySelectorAll("select");
        let keyObject = {
            "Gender": getRandomValueFromList(genderList),
            "Age": getRandomValueFromList(ageList),
            "Skin Tone": getRandomValueFromList(skinToneList),
            "Ethnicity": getRandomValueFromList(ethnicityList),
            "Body Type": getRandomValueFromList(bodyList),
            "Clothing Style": getRandomValueFromList(styleList),
            "Clothing Color": getRandomValueFromList(colorList),
            "Clothing Top": getRandomValueFromList(topList),
            "Clothing Bottom": getRandomValueFromList(bottomList),
            "Underwear": getRandomValueFromList(underwearList),
            "Outerwear": getRandomValueFromList(outerwearList),
            "Footwear": getRandomValueFromList(footwearList),
            "Accessory": getRandomValueFromList(accessoryList),
            "Hairstyle": getRandomValueFromList(hairStyleList),
            "HairColors": getRandomValueFromList(hairColoList),
        }
        allSelection.forEach((select) => {
            if (keyObject.hasOwnProperty(select.ariaLabel)) {
                if (select.value) {
                    keyObject[select.ariaLabel] = select.value;
                }
            }
        })
        let promptText = `a ${keyObject["Ethnicity"]} ${keyObject["Age"]} ${keyObject["Gender"]} with ${keyObject["Skin Tone"]} skin tone and an ${keyObject["Body Type"]} body type, wearing a ${keyObject["Clothing Style"]} ${keyObject["Clothing Color"]} ${keyObject["Clothing Top"]} ${keyObject["Clothing Bottom"]} and white ${keyObject["Footwear"]}, accessorized with a ${keyObject["Accessory"]},with ${keyObject["Hairstyle"]} ${keyObject["HairColors"]} hair`
        promptOutput += promptText.toLowerCase();

        let customInput = prompt.querySelectorAll("[data-id]");
        customInput.forEach((input) => {
            // const chipText = input.textContent.trim().split('\n')[0];
            promptOutput += input.firstChild.textContent + " , ";

        });
        console.log("this is positive prompt: " + promptOutput);
        // promptOutput = "";

        let negativePrompt = document.getElementById("negative-prompt-bubble-area");
        let customNegativeInput = negativePrompt.querySelectorAll("[data-id]");
        let promptOutputN = "";
        customNegativeInput.forEach((input) => {

            promptOutputN += input.firstChild.textContent + " , ";
        });
        let nprompt = "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4),(deformed, distorted, disfigured:1.3),poorly drawn,bad anatomy,wrong anatomy,extra limb,missing limb,floating limbs,disconnected limbs,mutation,mutated,ugly,disgusting,amputation,watermark text," + promptOutputN;

        let checkpoint = "aaa"
        if (keyObject["Gender"] === "Female") {
            console.log("sds " + keyObject["Gender"])
            checkpoint = "Yuna_NOFACE"
        } else {
            checkpoint = "realisticVisionV60B1_v51HyperVAE"
        }


        let payload = {
            "prompt": promptOutput,
            "negative_prompt": nprompt,
            "seed": 1,
            "steps": 20,
            "width": 720,
            "height": 720,
            "cfg_scale": 5,
            "sampler_name": "DPM++ 2M",
            "n_iter": 1,
            "batch_size": 1,
            "override_settings": {
                'sd_model_checkpoint': checkpoint,  //this can use to switch sd model waiREALCN_v70 or realisticVisionV60B1_v51HyperVAE
            }
        };
        let control_pose ={
            "control_pose":"2.jpg"
        }
       document.getElementById("waitingImg").style.display = "block";
        const date = { payload ,control_pose };

        fetch('/txt2img', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(date)
        })
        .then(response => response.json())
        .then(data => {
            //   console.log('Response from Python:', data);
            promptOutput = "";
            nprompt = "";
            document.getElementById("waitingImg").style.display = "none";
            document.getElementById("aiImage").src = data['img_path'];

        })
        .catch(error => {
            console.error('Error:', error);
        });
    })

});




// function imageUploaded() {
//     return new Promise((resolve, reject) => {
//         let file = document.querySelector('input[type=file]')['files'][0];
//         let reader = new FileReader();
//         reader.onload = function () {
//             let base64String = reader.result.replace("data:", "")
//                 .replace(/^.+,/, "");
//             resolve(base64String);
//         };

//         reader.onerror = function (error) {
//             reject(error);
//         };

//         reader.readAsDataURL(file);
//     });
// }

