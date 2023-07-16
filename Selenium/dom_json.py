from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import time
url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"

driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 15)  # Wait for a maximum of 15 seconds
wait.until(lambda driver: driver.execute_script("return document.readyState") == 'complete')
time.sleep(5)
dom_json = driver.execute_script("""
    const forms = document.querySelectorAll('form');
    const formsDef = {};
                                 function traverse(element){
                                            let domObject = {}
                                            const classnames = Array.from(element.classList) || '';
                                            const id = element.id || ''; 
                                            const type = element.type || '';
                                            if(classnames){
                                                domObject['classname'] = classnames;
                                            }
                                            if(id){
                                                domObject['id'] = id;
                                            }
                                            if(type){
                                                domObject['type'] = type;
                                            }
                                            const mapping = {};
                                            if(element.children){for (const child of element.children) {
                                                if (child.nodeType === Node.ELEMENT_NODE) {
                                                    const tag_name = child.tagName.toLowerCase();
                                                    const traversalValue = traverse(child) || {};
                                                    if(mapping[tag_name]){
                                                        let value = mapping[tag_name];
                                                        domObject[tag_name+'['+value+']'] = traversalValue;
                                                        mapping[tag_name] = mapping[tag_name]+1;
                                                    }
                                                    else{
                                                        domObject[tag_name] = traversalValue;
                                                        mapping[tag_name] = 1;
                                                    }
                                                }
                                            }}
                                            return domObject;
                                 }
    if(forms){
                                 forms.forEach((form,index) => {
                                        const name = form.id || form.name || `Form-${index}`;
                                        formsDef[name] = traverse(form);
                                 });
    }
                                 
    return formsDef;

""")
                                 

with open('dom.json','w') as file:
    json.dump(dom_json,file)