from selenium import webdriver
import json
import time
driver = webdriver.Chrome()
driver.get("https://form-block-full--nedbank--vdua.hlx.live/en/personal/borrow/personal-loans-form")
time.sleep(20)
# Get the external stylesheets using Selenium
external_stylesheets = driver.execute_script("""
        var styleSheets = document.styleSheets;
        var styles = {};
        for (var i = 0; i < styleSheets.length; i++) {
            var rules;
            try {
                rules = styleSheets[i].cssRules || styleSheets[i].rules;
            } catch (error) {
                continue;
            }

            for (var j = 0; j < rules.length; j++) {
                var rule = rules[j];
                if (rule instanceof CSSStyleRule) {
                    if (styles[rule.selectorText] === undefined){
                        styles[rule.selectorText] = ''                   
                    }
                    styles[rule.selectorText] = styles[rule.selectorText]  + rule.style.cssText.split(';');
                }
            }
        }
                                             
        return styles;
""")


with open("external_stylesheets.json",'w') as file:
    json.dump(external_stylesheets, file)

driver.quit()
