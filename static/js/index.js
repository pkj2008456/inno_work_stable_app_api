const SkinTone = document.getElementById("SkinTongSelector");
const Ethnicity = document.getElementById("EthnicitySelector");
const Body = document.getElementById("BodyTypeSelector");
const Style = document.getElementById("ClothingStyleSelector")
const Color = document.getElementById("ClothingColorSelector")
const Top = document.getElementById("ClothingTopSelector")
const Bottom = document.getElementById("ClothingBottomSelector")
const Underwear = document.getElementById("ClothingUnderwearSelector")
const Outerwear = document.getElementById("ClothingOuterwearSelector")
const Footwear = document.getElementById("FootwearSelector")
const Accessory = document.getElementById("AccessorySelector")
const Hairstyle = document.getElementById("HairstyleSelector")
const HairColor = document.getElementById("HairstyleSelector");


const genderList = ["Male", "Female", "Others"]
const ageList = ["Infant", "Child", "Teenager", "Young Adult", "Adult", "middle-age", "Senior", "Elderly"]
const skinToneList = ["Not set", "Porcelain", "Rosie", "Peach", "White"];
const ethnicityList = ["Not set", "African", "Asian", "Caucasian", "Hispanic", "Middle Eastern", "Native American", "Pacific Islander", "South Asian"];
const bodyList = ["Not set", "Slim", "Athletic", "Average", "Curvy", "Plus Size", "Petite", "Tall", "Short", "Muscular", "Stocky", "Other"];
const styleList = ["Not set", "Casual", "Formal", "Bohemian", "Vintage", "Streetwear", "Hipster", "Athleisure", "Preppy", "Gothic", "Punk", "Minimalist", "Tomboy", "Retro", "Glamorous"]
const colorList = ["Not set", "Black", "White", "Gray", "Navy", "Blue", "Teal", "Green", "Olive", "Yellow", "Orange", "Red", "Pink", "Purple", "Brown",
    "Beige", "Cream", "Burgundy", "Mustard", "Lavender", "Mint", "Coral", "Champagne", "Taupe", "Gold"
    , "Rose Gold", "Neutral", "Pastel", "Earth Tone", "Cool Tones", "Warm Tones", "Muted", "Metallic"]
const topList = ["Not set", "T-shirt", "Blouse", "Shirt", "Tank top", "Dress", "Mini dress", "Midi dress", "Maxi dress", "Shirt dress", "Hoodie", "Jumpsuit"]
const bottomList = ["Not set", "Jeans", "Pants", "Wide-Leg Pants", "Cargo Pants", "Flared Pants", "Skirt", "Mini Skirt", "Midi Skirt", "Maxi Skirt", "Pencil Skirt"
    , "Pleated Skirt", "High-Waisted Shorts", "Leggings", "Trousers"]
const underwearList = ["Not set", "Underwear", "Bikini", "Pajamas", "Thermal Underwear", "Swimsuit", "Camisole", "Negligee"]
const outerwearList = ["Not set", "Pea coat", "Trench coat", "Jacket", "Suit jacket", "Denim jacket", "Bomber jacket", "Leather jacket", "Parks", "Cardigan"]
const footwearList = ["Not set", "Sneakers", "Boots", "Sandals", "Heels", "Shoes", "Loafers", "Oxfords", "Ballet Flats", "Platform Shoes"]
const accessoryList = ["Not set", "Hat", "Belt", "Scarf", "Necklace", "Earrings", "Glasses", "Sunglasses", "Handbag", "Headband"]
const backgroundList = ["Not set", "White wall", "Studio backdrop", "Brick wall", "Concreate wall", "Floral wallpaper", "Forest", "Beach", "Cityscape", "Industrial area",
    "Rooftop", "Graffiti wall", "Vintage room", "Minimalist setting", "Bokeh lights", "Nature landscape", "Urban alley", "Botanical garden", "Old staircase", "Library", "Desert", "Countryside",
    "Waterfall", "Mountain range", "Park", "Abandoned building", "Shop", "Rustic barn", "Warehouse", "Sunset", "Sunrise", "Architecture"]
const hairStyleList = ["Not set", "Long", "Medium", "Short", "Curly", "Wavy", "Bald", "Bob haircut", "Shag haircut", "Bangs", "Ponytail", "Undercut", "Top knot", "French braid", "Messy bun", "Afro hair", "Dreadlocks", "Braids"]
const hairColoList = ["Not set", "Black", "Brown", "Dark-brown", "Gray", "Light-gray", "Blonde", "Light-blonde", "White"]
let insertList = (list, position) => {
    position.remove(0);
    list.forEach(tone => {
        const option = document.createElement("option");
        option.value = tone;
        option.textContent = tone;
        position.appendChild(option);
    });
}


insertList(skinToneList, SkinTone);
insertList(ethnicityList, Ethnicity);
insertList(bodyList, Body);
insertList(styleList, Style);
insertList(colorList, Color);
insertList(topList, Top);
insertList(bottomList, Bottom);
insertList(underwearList, Underwear);
insertList(outerwearList, Outerwear);
insertList(footwearList, Footwear);
insertList(accessoryList, Accessory);
insertList(hairStyleList, Hairstyle);

class HumanStyleSelectCreator {
    constructor() {
        this.selectorOptions = {
            BodyTypeSelector: { list: bodyList },
            SkinTongSelector: { list: skinToneList },
            EthnicitySelector: { list: ethnicityList },
            ClothingStyleSelector: { list: styleList },
            ClothingColorSelector: { list: colorList },
            ClothingTopSelector: { list: topList },
            ClothingBottomSelector: { list: bottomList },
            ClothingUnderwearSelector: { list: underwearList },
            ClothingOuterwearSelector: { list: outerwearList },
            FootwearSelector: { list: footwearList },
            AccessorySelector: { list: accessoryList },
            HairstyleSelector: { list: hairStyleList },
        };
    }

    handleChipClick(chipDiv, chipDropList, value = null, index = null) {
        const selectorId = chipDiv.dataset.selectId;
        const options = this.selectorOptions[selectorId];

        if (options) {
            insertList(options.list, chipDropList);
            if (value !== null) {
                chipDropList.value = value;
            } else if (index !== null) {
                chipDropList.selectedIndex = index;
            }
        }
        // chipDiv.appendChild(chipDropList);
        return chipDiv;
    }
}

const HumanStyleCreator = new HumanStyleSelectCreator()


//when user enter text in the input box bubble will be created 
let promptInput = document.getElementById("promptInput");
promptInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        console.log("dad")
        let prompt = document.getElementById("prompt-bubble-area");

        let chipDiv = document.createElement("div");
        chipDiv.className = "chip backgroudColor-item";
        chipDiv.innerHTML = promptInput.value;
        chipDiv.dataset.id = Date.now();

        let chipClose = document.createElement('span');
        chipClose.className = "closebtn";
        chipClose.innerHTML = "&times;";
        chipClose.onclick = function () {
            chipDiv.remove();
        };
        chipDiv.appendChild(chipClose);
        prompt.appendChild(chipDiv);
        promptInput.value = "";
    }
})
let negativePromptInput = document.getElementById("negativePromptInput");
negativePromptInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        console.log("dad")
        let prompt = document.getElementById("negative-prompt-bubble-area");

        let chipDiv = document.createElement("div");
        chipDiv.className = "chip backgroudColor-item";
        chipDiv.innerHTML = negativePromptInput.value;
        chipDiv.dataset.id = Date.now();

        let chipClose = document.createElement('span');
        chipClose.className = "closebtn";
        chipClose.innerHTML = "&times;";
        chipClose.onclick = function () {
            chipDiv.remove();
        };
        chipDiv.appendChild(chipClose);
        prompt.appendChild(chipDiv);
        promptInput.value = "";

    }
})




// Clear humam select and set the default
let selectionClear = document.querySelectorAll('[name="selectionClear"]');
selectionClear.forEach((selection) => {
    selection.addEventListener("click", function (e) {
        const prompt = document.getElementById("prompt-bubble-area");
        const childDivs = prompt.querySelectorAll("div");

        if (selection.id === "genderClear") {
            let radioButtons = document.querySelectorAll("[name='radioGender']");
            radioButtons.forEach(radioButton => {
                radioButton.checked = false;
                let femaleNode = prompt.querySelector('[data-select-id="Female"]');
                let maleNode = prompt.querySelector('[data-select-id="Male"]');
                let othersNode = prompt.querySelector('[data-select-id="Others"]');
                let matchingNodes = femaleNode || maleNode || othersNode;
                matchingNodes.remove();

            });
        } else if (selection.id === "ageClear") {
            let radioButtons = document.getElementById("ageRange");
            radioButtons.value = 0;
            document.getElementById("rangeValue").innerHTML = ""
            if (prompt.querySelector('[data-select-id="ageRange"]'))
                prompt.querySelector('[data-select-id="ageRange"]').remove();
        } else if (selection.id === "hairClear") {
            console.log("res")
            let radioButtons = document.querySelectorAll("[name='hair-color-div']");
            radioButtons.forEach(radioButton => {
                radioButton.classList.remove("hair-item-clicked");
            });
            if (prompt.querySelector('[data-select-id="HairColor"]'))
                prompt.querySelector('[data-select-id="HairColor"]').remove();
        }
        else {
            const selectElement = e.target.closest('.col-6').querySelector('[name="RoleStyleSelector"]');
            if (selectElement) {
                selectElement.value = "Not set";
            }
            childDivs.forEach((childDiv) => {
                const selectId = childDiv.dataset.selectId;
                console.log(`data-select-id: ${selectId}`);
                if (selectId === selectElement.id) {
                    console.log("id:test")
                    childDiv.remove();
                }
            });
        }

    })
})


// add hair border color
let hairColors = document.querySelectorAll('[class="hair-item"]');
hairColors.forEach((hairColor) => {
    hairColor.addEventListener("click", function (e) {
        hairColors.forEach(item => item.classList.remove("hair-item-clicked"));
        this.classList.add("hair-item-clicked");
    })
})


//Add the bubble when the human select option click 
document.addEventListener('DOMContentLoaded', function (e) {
    let dropList = document.querySelectorAll("[name ='RoleStyleSelector']");
    let prompt = document.getElementById("prompt-bubble-area");

    dropList.forEach(function (select) {
        select.addEventListener('change', function () {
            let selectedOptionValue = this.value;
            console.log("test selects", selectedOptionValue)

            let oldDiv = prompt.querySelector(`div[data-select-id="${select.id}"]`);
            if (oldDiv) {
                prompt.removeChild(oldDiv);
            }


            if (selectedOptionValue === "Not set") {
                return;
            }


            let chipDiv = document.createElement("div");
            chipDiv.className = "chip backgroudColor-item";
            chipDiv.dataset.selectId = select.id

            let chipDropList = document.createElement('select');
            chipDropList.setAttribute("aria-label", select.ariaLabel);
            let chipClose = document.createElement('span');
            chipClose.className = "closebtn";
            chipClose.innerHTML = "&times;";
            chipClose.onclick = function () {
                chipDiv.remove();
            };

            chipDiv = HumanStyleCreator.handleChipClick(chipDiv, chipDropList, selectedOptionValue)



            chipDiv.appendChild(chipDropList);
            chipDiv.appendChild(chipClose);
            prompt.appendChild(chipDiv);

        });
    });
});


// add gender bubble to promtp
var lastGenderValue = null;
function handleGenderInput() {

    const prompt = document.getElementById("prompt-bubble-area");
    if (lastGenderValue !== null) {
        console.log("a")
        let oldDiv = prompt.querySelector(`div[data-select-id="${lastGenderValue}"]`);
        if (oldDiv) {
            prompt.removeChild(oldDiv);
        }
    }

    let chipDropList = document.createElement('select');
    chipDropList.setAttribute("aria-label", "Gender");

    // chipDropList.className = "chipsDropList browser-default  ";

    let chipClose = document.createElement('span');
    chipClose.className = "closebtn";
    chipClose.innerHTML = "&times;";
    chipClose.onclick = function () {
        let oldDiv = prompt.querySelector(`div[data-select-id="${lastGenderValue}"]`);
        if (oldDiv) {
            prompt.removeChild(oldDiv);
        }
    };


    insertList(genderList, chipDropList)
    let checkedRadio = document.querySelector('input[name="radioGender"]:checked');
    if (checkedRadio) {
        chipDropList.value = checkedRadio.value;
        console.log(checkedRadio.value)
        lastGenderValue = checkedRadio.value;
    }

    let chipDiv = document.createElement("div");
    chipDiv.dataset.selectId = lastGenderValue;
    chipDiv.className = "chip backgroudColor-item";

    chipDiv.appendChild(chipDropList);
    chipDiv.appendChild(chipClose);
    prompt.appendChild(chipDiv);
}

window.onload = function () {
    var genderInputs = document.querySelectorAll('input[name="radioGender"]');
    genderInputs.forEach(input => {
        input.addEventListener('change', handleGenderInput);
    });
}


//Reset all select 
let ResetAllButton = document.getElementById("ResetAllButton");
ResetAllButton.addEventListener("click", function () {
    let promptBubbleArea = document.getElementById("prompt-bubble-area");
    while (promptBubbleArea.firstChild) {
        promptBubbleArea.removeChild(promptBubbleArea.firstChild);
    }
    let RoleStyleSelector = document.getElementsByName("RoleStyleSelector");
    RoleStyleSelector.forEach((select) => {
        select.selectedIndex = 0;
    })

});

let AgeInput = document.getElementById("ageRange")
AgeInput.addEventListener("input", function () {
    const prompt = document.getElementById("prompt-bubble-area");
    var range = document.getElementById("ageRange");
    var rangeValue = document.getElementById("rangeValue");
    for (let i = 0; i < ageList.length; i++) {
        if (range.value == i * 10) {
            rangeValue.innerHTML = ageList[i];
        }
    };
    let a = prompt.querySelector('[data-select-id="ageRange"]')
    if (a) {
        prompt.removeChild(a);
    }


    let chipDropList = document.createElement('select');
    chipDropList.setAttribute("aria-label", "Age");
    let chipClose = document.createElement('span');
    chipClose.className = "closebtn";
    chipClose.innerHTML = "&times;";
    chipClose.onclick = function () {
        let oldDiv = prompt.querySelector('div[data-select-id="ageRange"]');
        if (oldDiv) {
            prompt.removeChild(oldDiv);
        }
    };


    insertList(ageList, chipDropList)
    chipDropList.value = rangeValue.innerHTML;
    let chipDiv = document.createElement("div");
    chipDiv.dataset.selectId = "ageRange";
    chipDiv.className = "chip backgroudColor-item";


    chipDiv.appendChild(chipDropList);
    chipDiv.appendChild(chipClose);
    prompt.appendChild(chipDiv);
    lastRangeValue = range.value;
});

//random options function
let randomButton = document.getElementById("randomButton");
randomButton.addEventListener("click", function () {


    // random gender 
    let gender = document.querySelectorAll("[name='radioGender']");
    let randomIndex = Math.floor(Math.random() * gender.length);
    gender.forEach((radio, index) => {
        if (index === randomIndex) {
            radio.checked = true;
            radio.dispatchEvent(new Event('change'));
        } else {
            radio.checked = false;
        }
    });

    // random humam style e.g skin tone , ethnicity etc..
    let humanStyleArray = document.querySelectorAll("[name ='RoleStyleSelector']")
    humanStyleArray.forEach((select) => {
        const prompt = document.getElementById("prompt-bubble-area");

        let randomIndex = Math.floor(Math.random() * select.options.length);
        select.selectedIndex = randomIndex;

        if (randomIndex === 0) {
            return;
        }

        let selectedOptionValue = this.value;
        console.log("test random", randomIndex)

        let oldDiv = prompt.querySelector(`div[data-select-id="${select.id}"]`);
        if (oldDiv) {
            prompt.removeChild(oldDiv);
        }



        let chipDiv = document.createElement("div");
        chipDiv.className = "chip backgroudColor-item";
        chipDiv.dataset.selectId = select.id;

        let chipDropList = document.createElement('select');
        chipDropList.setAttribute("aria-label", select.ariaLabel);
        let chipClose = document.createElement('span');
        chipClose.className = "closebtn";
        chipClose.innerHTML = "&times;";
        chipClose.onclick = function () {
            chipDiv.remove();
        };

        chipDiv = HumanStyleCreator.handleChipClick(chipDiv, chipDropList, null, randomIndex)
        chipDiv.appendChild(chipDropList);
        chipDiv.appendChild(chipClose);
        prompt.appendChild(chipDiv);

    })


})


// 獲取所有 hair radio 按鈕
const hairColorRadios = document.querySelectorAll('input[name="hair-color"]');

hairColorRadios.forEach(radio => {
    radio.addEventListener('click', () => {
        const prompt = document.getElementById("prompt-bubble-area");


        const selectedColor = radio.value;
        console.log('Selected hair color:', selectedColor);

        let a = prompt.querySelector('[data-select-id="HairColor"]')
        if (a) {
            prompt.removeChild(a);
        }


        let chipDropList = document.createElement('select');
        chipDropList.setAttribute("aria-label", "Hair Color");

        let chipClose = document.createElement('span');
        chipClose.className = "closebtn";
        chipClose.innerHTML = "&times;";
        chipClose.onclick = function () {
            chipDiv.remove();
        };


        insertList(hairColoList, chipDropList)
        chipDropList.value = selectedColor;
        let chipDiv = document.createElement("div");
        chipDiv.dataset.selectId = "HairColor";
        chipDiv.className = "chip backgroudColor-item";




        chipDiv.appendChild(chipDropList);
        chipDiv.appendChild(chipClose);
        prompt.appendChild(chipDiv);

    });
});

// hidden all harir radio button ,which just show the lable
hairColorRadios.forEach(radio => {
    radio.style.display = 'none';
});



function getRandomValueFromList(list) {
    while(true){
        let text = list[Math.floor(Math.random() * list.length)]
        if(text != "Not set"){
            return text;
        }
    }
} 

document.querySelectorAll('.insideNavbarItem').forEach(item => {
    item.addEventListener('click', (e) => {
      document.querySelectorAll('[name = "selectContext"]').forEach(i => {
        i.style.display = 'none';
      });
  
      if (e.target.id === 'generatorPageButton') {
        document.querySelector('.sidebar-context').style.display = 'block';
        document.querySelector('.sidebar-context').classList.add("clicked")
      } else if (e.target.id === 'faceUploadPageButton') {
        document.querySelector('.sidebar-face-upload').style.display = 'block';
      } else if(e.target.id === 'posePageButton'){
        document.querySelector('.sidebar-pose').style.display = 'block';
      }
    });
  });

// print out all selec when Generate chicked 
// document.addEventListener("DOMContentLoaded", function () {
//     let promptOutput = "";
//     let generateButton = document.getElementById("generateButton");
//     generateButton.addEventListener("click", function () {
//         let prompt = document.getElementById("prompt-bubble-area");
//         let allSelection = prompt.querySelectorAll("select");
//         let keyObject = {
//             "Gender": getRandomValueFromList(genderList),
//             "Age" : getRandomValueFromList(ageList),
//             "Skin Tone" : getRandomValueFromList(skinToneList),
//             "Ethnicity" : getRandomValueFromList(ethnicityList),
//             "Body Type" : getRandomValueFromList(bodyList),
//             "Clothing Style" : getRandomValueFromList(styleList),
//             "Clothing Color" : getRandomValueFromList(colorList),
//             "Clothing Top" : getRandomValueFromList(topList),
//             "Clothing Bottom" : getRandomValueFromList(bottomList),
//             "Underwear" : getRandomValueFromList(underwearList),
//             "Outerwear" : getRandomValueFromList(outerwearList),
//             "Footwear" : getRandomValueFromList(footwearList),
//             "Accessory"  : getRandomValueFromList(accessoryList),
//             "Hairstyle" : getRandomValueFromList(hairStyleList),
//             "HairColors" : getRandomValueFromList(hairColoList), 
//         }
//         allSelection.forEach((select) => {            
//             if(keyObject.hasOwnProperty(select.ariaLabel)){
//                 if(select.value){
//                     keyObject[select.ariaLabel] = select.value;
//                 }
//             }
//         })
//         let promptText = `a ${keyObject["Ethnicity"]} ${keyObject["Age"]} ${keyObject["Gender"]} with ${keyObject["Skin Tone"]} skin tone and an ${keyObject["Body Type"]} body type, wearing a ${keyObject["Clothing Style"]} ${keyObject["Clothing Color"]} ${keyObject["Clothing Top"]} ${keyObject["Clothing Bottom"]} and white ${keyObject["Footwear"]}, accessorized with a ${keyObject["Accessory"]},with ${keyObject["Hairstyle"]} ${keyObject["HairColors"]} hair`
//         promptOutput += promptText.toLowerCase();

//         let customInput = prompt.querySelectorAll("[data-id]");
//         customInput.forEach((input) => {
//             // const chipText = input.textContent.trim().split('\n')[0];
//             promptOutput += input.firstChild.textContent + " , ";
            
//         });
//         console.log("this is positive prompt: "+promptOutput);
//         // promptOutput = "";

//         let negativePrompt = document.getElementById("negative-prompt-bubble-area");
//         let customNegativeInput = negativePrompt.querySelectorAll("[data-id]");
//         let promptOutputN
//         customNegativeInput.forEach((input) => {
           
//              promptOutputN += input.firstChild.textContent  + " , ";
//         });
//         console.log("this is nagative prompt: (deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4),(deformed, distorted, disfigured:1.3),poorly drawn,bad anatomy,wrong anatomy,extra limb,missing limb,floating limbs,disconnected limbs,mutation,mutated,ugly,disgusting,amputation,watermark text,"+promptOutputN);
//         // promptOutput = "";


        
//         const payload = {
//             "prompt": promptOutput,
//             "negative_prompt": promptOutputN,
//             "seed": 1,
//             "steps": 20,
//             "width": 720,
//             "height": 720,
//             "cfg_scale": 5,
//             "sampler_name": "DPM++ 2M",
//             "n_iter": 1,
//             "batch_size": 6,
//             "override_settings": {
//               'sd_model_checkpoint': "sd_xl_base_1.0"
//             }
//           };
//         const data = { message: payload };

//         fetch('http://34.90.139.98:8000', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json'
//           },
//           body: JSON.stringify(data)
//         })
//         .then(response => response.json())
//         .then(data => {
//           console.log('Response from Python:', data);
//         })
//         .catch(error => {
//           console.error('Error:', error);
//         });

        
        
        

//     })
// });

//for the update state
// $('#upload-form').submit(function(event) {
//     event.preventDefault(); 
    
//     var formData = new FormData(this);
    
//     $.ajax({
//         type: 'POST',
//         url: '{{ url_for("upload_file") }}',
//         data: formData,
//         processData: false,
//         contentType: false,
//         success: function(response) {
//             $('#update-container').html(response.update_message);
//         },
//         error: function() {
//             alert('Error uploading file.');
//         }
//     });
// });



