import asyncio
import pyppeteer
import re
async def script(url):
    async def extract_css(page, classnames):
        # Enable CSS coverage
        await page.coverage.startCSSCoverage()

        # Click on the element to inspect it
        for selector in classnames:
            try:
                await asyncio.sleep(0.5)
                await page.click('.'+selector)
            except:
                pass
        # Wait for a brief moment to ensure styles are captured
        await asyncio.sleep(1)
        # Retrieve the CSS coverage
        coverage = await page.coverage.stopCSSCoverage()

        # Extract CSS rules for the selected element
        css_rules = set()
        for selector in classname:
            selector_regex = re.compile(r"\b" + re.escape(selector) + r"\b")
            for entry in coverage:
                for css_range in entry['ranges']:
                    css_text = entry['text'][css_range['start']:css_range['end']]
                    if selector_regex.search(css_text):
                        css_rules.add(css_text)

        css_styles = ''
        for item in css_rules:
            css_styles= css_styles + str(item) + '\n'
        print('CSS Extracted')
        return css_styles

    async def extract_dom(page, selector):
        # Extract the DOM of the element
        element_dom = await page.evaluate('''(selector) => {
            const element = document.querySelector(selector);
    if (element) {
        function traverse(element) {
            let html = "<" + element.tagName.toLowerCase();
            const attributenames = ['name','class','id','type']
            // Store the element's attributes
            for (const attr of element.attributes) {
                if(attributenames.includes(attr.name)){
                html += ` ${attr.name}="${attr.value}"`;
                }
            }

            html += ">";

            // Store the element's child nodes
            let childCount = 0;
            for (const child of element.childNodes) {
                if (child.nodeType === Node.ELEMENT_NODE) {
                    html += traverse(child);
                    childCount++;

                    // Limit the number of child elements for select tag
                    if (element.tagName.toLowerCase() === "select" && childCount >= 5) {
                        break;
                    }
                }
            }

                html += "</" + element.tagName.toLowerCase() + ">";

                return html;
            }

                return traverse(element);
            } else {
                return null;
            }
        }''', selector)
        print('ELement DOM Extracted')
        return element_dom

    async def extract_classname(page,selector):
        classnames = await page.evaluate('''(selector) => {
                const element_dom = document.querySelector(selector);
                var tags = element_dom.getElementsByTagName('*');
                const classnames = Array.from(element_dom.classList);
                const tagnames = [selector]
                for (var i = 0; i < tags.length; i++) {
                    classnames.push.apply(classnames,Array.from(tags[i].classList));
                    tagnames.push(tags[i].tagName.toLowerCase());
                }
                // classnames.push.apply(classnames,tagnames)
                const classname = Array.from(new Set(classnames));
                return classname;
            } ''',selector)
        print('Classname Extracted')
        return classnames

    selector = "form"
    options = {
            "waitUntil": 'networkidle0',
            "timeout": 200000,
            "origins": 'exclude',
            "inlineStyles": 'include'
        }

    browser = await pyppeteer.launch(handleSIGINT=False, handleSIGTERM=False,handleSIGHUP=False)

    page = await browser.newPage()

    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0')

    try:
        response = await page.goto(url, options)
    except TimeoutError:
        print("Navigation timeout occurred.")

        # Bad request
    if response.status >= 400:
        print('Bad Request, Closing Broswer')
        await browser.close()

        # await extract_css(page, xpath, browser, response)
    element_dom = await extract_dom(page, selector)
    classname = await extract_classname(page,selector)
    css_styles = await extract_css(page,classname)

    await browser.close()

    obj = {"element_dom":element_dom,"css_styles":css_styles}
    print('Browser closed')

    with open('element_dom.html','w') as file:
        file.write(element_dom)
    
    with open('css_styles.css','w') as file:
        file.write(css_styles)

    return obj

asyncio.get_event_loop().run_until_complete(script('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'))