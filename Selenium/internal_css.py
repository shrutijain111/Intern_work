from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.google.com/")
internal_styles = driver.execute_script("""
    var styles = [];
    var styleTags = document.getElementsByTagName('style');
    for (var i = 0; i < styleTags.length; i++) {
        styles.push(styleTags[i].innerHTML);
    }
    return styles;
""")

listToStr = ' '.join(map(str, internal_styles))

with open("internal-css.css",'w') as file:
    file.write(listToStr)

driver.quit()