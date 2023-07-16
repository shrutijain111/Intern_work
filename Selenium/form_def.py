from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://www.instagram.com/?hl=en")

# Wait for the page to load completely
wait = WebDriverWait(driver, 15)  # Wait for a maximum of 10 seconds
wait.until(lambda driver: driver.execute_script("return document.readyState") == 'complete')
time.sleep(10)

fields = driver.execute_script('''

    function getLabel(element,form) {
        let value;
        if (element instanceof HTMLButtonElement) {
            value = element.textContent?.trim();
        } else if (element.id) {
            const label = form.querySelector(`label[for=${element.id}]`);
            value = label?.textContent?.trim();
        }
        return value || element?.name;
    }

    function handleCheckBox(element,labelIncludedMap,form,fields) {
        if (element.type === 'checkbox' || element.type === 'radio') {
            if (!labelIncludedMap.has(element.name)) {
            const label = form.querySelector(`label[for="${element.name}"]`);
                if (label) {
                    const field = {
                    Name: '',
                    Type: 'fieldset',
                    Description: '',
                    Placeholder: '',
                    Label: label?.textContent?.trim(),
                    'Read Only': '',
                    Mandatory: '',
                    Pattern: '',
                    Step: undefined,
                    Min: undefined,
                    Max: undefined,
                    Value: '',
                    Options: '',
                    };
                    labelIncludedMap.set(element.name, true);
                    fields.push(field);
                }
            }
        }
    }

  function handleHiddenValue(element, field) {
        if (element?.type === 'hidden') {
            field.Value = element?.value;
        }
    }

  function handleSelectElement(element, field) {
    if (element instanceof HTMLSelectElement) {
      field.Type = 'select';
      field.Options = [];
      field.OptionNames = [];
      [...element.options].forEach((option) => {
        field.Options.push(option.value);
        field.OptionNames.push(option.text?.trim());
      });
      field.Options = field.Options.join(',');
    }
  }

    function generateFromForm(form) {
        fields = [];
        labelIncludedMap = new Map();
        if (form && form.elements) { //<input>  , <select>  , <textarea> , <button>  , <fieldset> , <keygen>  , <output>  , <object> 
            [...form.elements].forEach((element) => {
                if (element instanceof HTMLInputElement || element instanceof HTMLSelectElement || element instanceof HTMLTextAreaElement || element instanceof HTMLButtonElement) {
                    const name = element?.name?.trim();
                    const id = element?.id?.trim();
                    const field = {
                    Name: name || id,
                    Type: element?.type,
                    Description: element?.title?.trim(),
                    Placeholder: element?.placeholder?.trim() || '',
                    Label: getLabel(element,form),
                    'Read Only': element.readOnly || '',

                    Mandatory: element?.required || element.getAttribute('aria-required') === 'true' || '',
                    Pattern: element?.pattern,
                    Step: element?.step || undefined,
                    Min: element?.minLength || element?.min || undefined,
                    Max: element?.maxLength || element?.max || undefined,
                    Value: element.value,
                    Options: '',
                    };
                    handleHiddenValue(element, field);
                    handleSelectElement(element, field);
                    handleCheckBox(element,labelIncludedMap,form,fields);
                    fields.push(field);
                }
            });
        }
        return fields;
    }
                               

    const forms = document.querySelectorAll('form');
    const formsDefs = {};
                               
    if (forms) {
        forms.forEach((form, index) => {
        const name = form.id || form.name || `Form-${index}`;
        formsDefs[name] = generateFromForm(form);
    });
    } else {
        console.log('No form found in main page');
    } 
    return formsDefs;

  ''')


with open('form_defs.json','w') as file:
        json.dump(fields,file)