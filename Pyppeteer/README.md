Few things to keep in mind while Integrating Pyppeteer with flask:
initialise loop above the flask app 
disable the signal handling in pyppeteer


dom_css.py => used to extract the dom element and the corresponding css styles
css_styles.css , element_dom.html => output'

css_extraction.py => extraction of css styles and replacing the var(--) values with the computed values
css-extraction.css => output