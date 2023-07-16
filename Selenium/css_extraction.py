from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import time
def find_css_by_class(driver, class_name):
    
    # Retrieve all stylesheets
    stylesheets = driver.execute_script('''
        const stylesheets = Array.from(document.styleSheets);
        return stylesheets.map(stylesheet => {
            if (stylesheet.href) {
                // External stylesheet
                return stylesheet.href;
            } else if (stylesheet.ownerNode) {
                // Inline or embedded stylesheet
                return stylesheet.ownerNode.textContent;
            }
        });
    ''')
    #css_rules extracted from the stylesheets
    css_rules = []
    for stylesheet in stylesheets:
        if stylesheet.startswith('http'):
            # External stylesheet
            try:
                response = driver.execute_script(f'return fetch("{stylesheet}").then(response => response.text());')
                css_rules.append(response)
            except Exception as e:
                print(stylesheet)
                pass
        else:
            # Inline or embedded stylesheet
            css_rules.append(stylesheet)

    # Find CSS rules corresponding to the class name
    matching_css = set()
    for css in css_rules:
        matches = re.findall(f'\.{class_name}+[^{{]*{{[^}}]*}}', css)
        pattern = r"var\(([^)]+)\)" 
        for match in matches:
            pattern_matches = re.findall(pattern, match)
            unique_matches = list(set(pattern_matches))
            text = match
            for pattern in unique_matches: #replace var(--) with their respective computed styles
                computed_value_var = driver.execute_script('''
                    const match = arguments[0];
                    const computedValue = getComputedStyle(document.documentElement).getPropertyValue(match);
                    return computedValue;
                ''',pattern)
                text = text.replace(f"var({pattern})", computed_value_var)
            matching_css.add(text)

    driver.quit()

    return matching_css

# Example usage
url = 'https://www.instagram.com/?hl=en'
class_name = '_ab1y'
driver = webdriver.Chrome()  # Browser initialisation
driver.get(url) 
wait = WebDriverWait(driver, 15)  # Wait for a maximum of 15 seconds
wait.until(lambda driver: driver.execute_script("return document.readyState") == 'complete')
time.sleep(5)
matching_css = find_css_by_class(driver, class_name)

# Print the matching CSS rules
with open('css-extraction.css','w') as file:
    for item in matching_css:
        file.write(item)