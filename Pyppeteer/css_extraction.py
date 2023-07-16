import asyncio
import pyppeteer
import re
url = 'https://www.instagram.com/?hl=en'
class_name = ['_ab1y']

async def computed_value(page,variable):
     computed_value_var = await page.evaluate('''(variable) => {
        const computedValue = getComputedStyle(document.documentElement).getPropertyValue(variable);
        return computedValue;
    }''',variable)
     
     return computed_value_var

async def extract_css(page,classnames,coverage):
        css_rules = ''
        for entry in coverage:
            for range in entry['ranges']:
                    for classname in classnames:
                        if classname in entry['text'][range['start']:range['end']]:
                            pattern = r"var\(([^)]+)\)"
                            matches = re.findall(pattern, entry['text'][range['start']:range['end']])
                            unique_matches = list(set(matches))
                            text = entry['text'][range['start']:range['end']]
                            for match in unique_matches:
                                #  match = 'var('+match+')'
                                 computed_value_var = await computed_value(page,match)
                                 text = text.replace(f"var({match})", computed_value_var)
                            css_rules = css_rules + ' ' + text
        css_rules = css_rules.replace('{','{{')
        css_rules = css_rules.replace('}','}}')    
        return css_rules

async def mainn():
    options = { 
        "waitUntil": 'networkidle0',
        "timeout": 200000,
        "origins": 'exclude',
        "inlineStyles": 'include'
    }
    
    browser = await pyppeteer.launch()
    print('browser started')
    page = await browser.newPage()
    print('page started')
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0')
    print('user successfully set')
    response = None
    css_styles = None

    await page.setJavaScriptEnabled(True)
    print('javascipt started')
    try:
        response = await page.goto(url, options)
    except TimeoutError:
        print("Navigation timeout occurred.")

    # Bad request
    if response.status >= 400:
        print(' * Bad Request, Closing Broswer')
        await browser.close()
    await page.coverage.startCSSCoverage({'reportAnonymousScript':True})
    await asyncio.sleep(2)
    coverage = await page.coverage.stopCSSCoverage()

    css_styles= await extract_css(page,class_name,coverage)  


    with open('css-extraction.css','w') as file:
        file.write(css_styles)
    await browser.close()
    print(' * Broswer is Closed')
    
asyncio.get_event_loop().run_until_complete(mainn())