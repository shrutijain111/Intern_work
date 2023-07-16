from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
# Set up Selenium and launch the browser
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://form-block-full--nedbank--vdua.hlx.live/en/personal/borrow/personal-loans-form")

# Wait for the page to load completely
wait = WebDriverWait(driver, 15)  # Wait for a maximum of 10 seconds
wait.until(lambda driver: driver.execute_script("return document.readyState") == 'complete')
time.sleep(10)

import json

element_dom = driver.execute_script('''
    const selector = arguments[0];
    const element = document.querySelector(selector);
    let elemdomObject = {}
    if (element) {
        function traverse(element) {
            let domObject = {};
            const attributenames = ['name','class','id','type','style'];
            // Store the element's attributes
            for (const attr of element.attributes) {
                if (attributenames.includes(attr.name)) {
                    domObject[`${attr.name}`] = `${attr.value}`
                }
            }

            if(domObject['type'] == 'hidden'){
                return ;
            }                        
            
            for (const child of element.children) {
                if (child.nodeType === Node.ELEMENT_NODE) {
                    if(domObject['children']){
                    domObject["children"].push(child.tagName.toLowerCase());
                    }
                    else{
                        domObject['children'] = [];
                        domObject["children"].push(child.tagName.toLowerCase());
                    }
                }
            }

            for (const child of element.children) {
                if (child.nodeType === Node.ELEMENT_NODE) {
                    traverse(child)
                }
            }
            let count = 0
            const tag_name = element.tagName.toLowerCase();
            for (var key in elemdomObject){
                    if(key.includes(tag_name)){
                        if(elemdomObject[key].value === domObject.value){
                            return;
                        }
                        else{
                            count = count + 1;
                        }
                    }
            }
            
            domObject['children'] = Array.from(new Set(domObject['children']));
            if(count){
                count = count + 1;
                elemdomObject[tag_name+`[${count}]`] = domObject;
            }
            else{
                elemdomObject[tag_name] = domObject;                  
            }

            return domObject;
        }
        traverse(element)
        return JSON.stringify(elemdomObject);
    } else {
        return null;
    }
''', 'form')

json_data = json.loads(element_dom)



propertiess = ["align-content","background-color","border-block-end-color","border-block-end-style","border-block-end-width","border-block-start-color","border-block-start-style","border-block-start-width","border-bottom-color","border-bottom-left-radius","border-bottom-right-radius","border-bottom-style","border-bottom-width","border-collapse","border-end-end-radius","border-end-start-radius","border-inline-end-color","border-inline-end-style","border-inline-end-width","border-inline-start-color","border-inline-start-style" ,"border-inline-start-width","border-left-color","border-left-style","border-left-width","border-right-color","border-right-style" ,"border-right-width","border-start-end-radius","border-start-start-radius","border-top-color","border-top-left-radius","border-top-right-radius","border-top-style","border-top-width","caret-color","color","color-interpolation","font-family","font-size","font-style","font-weight","margin-block-end", "margin-block-start","margin-bottom","margin-inline-end","margin-inline-start","margin-left","margin-right","margin-top","padding-block-end","padding-block-start","padding-bottom","padding-inline-end","padding-inline-start","padding-left","padding-right","padding-top","position" ]


for key in json_data:
    id = ''
    if 'id' in json_data[key].keys():
        id = json_data[key]['id']
    class_ = '' 
    if 'class' in json_data[key].keys():
        class_ = json_data[key]['class']
    
    if id:
        element = driver.find_element(By.XPATH,f'//*[@id="{id}"]')
        properties = driver.execute_script('return window.getComputedStyle(arguments[0], "null");', element)
        csss = {}
        for property in properties:
            if property in propertiess:
                csss[property] = element.value_of_css_property(property)
        
        json_data[key]['css'] = csss

    elif class_:
        tagname = key
        element = driver.find_element(By.XPATH,f'//{tagname}[@class="{class_}"]')
        properties = driver.execute_script('return window.getComputedStyle(arguments[0], "null");', element)
        csss = {}
        for property in properties:
            if property in propertiess:
                csss[property] = element.value_of_css_property(property)
        
        json_data[key]['css'] = csss

with open('dom-computedcss.json' , 'w') as file:
    json.dump(json_data,file)