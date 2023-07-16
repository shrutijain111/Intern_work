from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
obj = {}
# Function to generate XPath for an element
def getElementXPath(element):
    xpath = ''
    classes = ''
    id = ''
    tagname = element.tag_name
    idxpath = ''
    try:
        if element.get_attribute('id'):
            id = element.get_attribute('id')
    except:
        pass
    try:
        while element:
            xpath_component = element.tag_name
            # Method to get the right position of element
            sibling_elements = element.find_elements(By.XPATH, 'preceding-sibling::*[name()="' + element.tag_name + '"]')
            xpath = '/' + xpath_component + f"[{len(sibling_elements) + 1}]" + xpath
            if element.get_attribute('class'):
                if(len(element.get_attribute('class'))):
                    classes = element.get_attribute('class') + " " + classes
            if element.tag_name != 'html':
                element = element.find_element(By.XPATH , '..')

                if idxpath == '':
                    if element.get_attribute('id'):
                        idd = element.get_attribute('id')
                        idxpath = '//'+element.tag_name+"[@id='"+idd+"']" + xpath
            else:
                break

    except:
        pass
    if "body" in xpath:
            if id !='':
                obj['//'+tagname+"[@id='"+id+"']"] = {}
                obj['//'+tagname+"[@id='"+id+"']"]["class_name"] = classes
                obj['//'+tagname+"[@id='"+id+"']"]["id_name"] = id
                obj['//'+tagname+"[@id='"+id+"']"]["tag_name"] = tagname
                return '//'+tagname+"[@id='"+id+"']"
            elif idxpath != '':
                obj[idxpath] = {}
                obj[idxpath]["class_name"] = classes
                obj[idxpath]["id_name"] = id
                obj[idxpath]["tag_name"] = tagname
                return idxpath
                
            else:
                obj['/' + xpath] = {}
                obj['/' + xpath]["class_name"] = classes
                obj['/' + xpath]["id_name"] = id
                obj['/' + xpath]["tag_name"] = tagname
                return '/' + xpath
                
    

url = 'https://form-block-full--nedbank--vdua.hlx.live/en/personal/borrow/personal-loans-form'  
driver = webdriver.Chrome()  
driver.get(url)
# driver.implicitly_wait(1)
# try:
#     wait = WebDriverWait(driver, 60)
#     ele = wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//*")))
# finally:
#     pass

time.sleep(20)#Wait to render the js-content
elements = driver.find_elements(By.XPATH, "//form//*")
xpaths = set()
for element in elements:
    xpath = getElementXPath(element)
    xpaths.add(xpath)

#properties to fetch
properties = ["align-content","background-color","border-block-end-color","border-block-end-style","border-block-end-width","border-block-start-color","border-block-start-style","border-block-start-width","border-bottom-color","border-bottom-left-radius","border-bottom-right-radius","border-bottom-style","border-bottom-width","border-collapse","border-end-end-radius","border-end-start-radius","border-inline-end-color","border-inline-end-style","border-inline-end-width","border-inline-start-color","border-inline-start-style" ,"border-inline-start-width","border-left-color","border-left-style","border-left-width","border-right-color","border-right-style" ,"border-right-width","border-start-end-radius","border-start-start-radius","border-top-color","border-top-left-radius","border-top-right-radius","border-top-style","border-top-width","caret-color","color","color-interpolation","font-family","font-size","font-style","font-weight","margin-block-end", "margin-block-start","margin-bottom","margin-inline-end","margin-inline-start","margin-left","margin-right","margin-top","padding-block-end","padding-block-start","padding-bottom","padding-inline-end","padding-inline-start","padding-left","padding-right","padding-top","position" ]
for path in xpaths:
        try:
            element = driver.find_element(By.XPATH,path)
            computed_properties = driver.execute_script('return window.getComputedStyle(arguments[0], null);', element)
            csss = {}
            for property in computed_properties:
                if property in properties:
                    csss[property] = element.value_of_css_property(property)
            obj[path]['css_style'] = csss
        except:
            print('error at ', path)
            pass

with open("xpath-computed.json",'w') as file:
    json.dump(obj, file)

driver.quit()
