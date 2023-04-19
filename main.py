import argparse
import random
import time
import requests
from faker import Faker
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# from bs4 import BeautifulSoup
# from emails import MAIL_GENERATION_WEIGHTS
from selenium import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from transformers import pipeline


model = pipeline("text-generation", model="gpt2")

CLOUD_DESCRIPTION = 'Puts script in a \'cloud\' mode where the Chrome GUI is invisible'
CLOUD_DISABLED = False
CLOUD_ENABLED = True
MAILTM_DISABLED = False
MAILTM_ENABLED = True
EPILOG = ''
SCRIPT_DESCRIPTION = ''

url = 'https://ago.mo.gov/file-a-complaint/transgender-center-concerns'


# Option parsing
parser = argparse.ArgumentParser(SCRIPT_DESCRIPTION, epilog=EPILOG)
parser.add_argument('--cloud', action='store_true', default=CLOUD_DISABLED,
                    required=False, help=CLOUD_DESCRIPTION, dest='cloud')

args = parser.parse_args()

fake = Faker()

cities_zips = {

    "Kansas City": [64101, 64102, 64105, 64106, 64108],
    "Saint Louis": [63101, 63102, 63103, 63104, 63105],
    "Springfield": [65619, 65721, 65801, 65802, 65803],
    "Independence": [64015, 64016, 6450, 64051, 64052],
    "Columbia": [65201, 65202, 65203, 65205, 65211],
    "Saint Joseph": [64501, 64502, 64503, 64504, 64505],
    "Saint Charles": [63301, 63302, 63303],
    "Saint Peters": [63301, 63303, 63304, 63376],
    "Florissant": [63031, 63032, 63033],
    "Blue Springs": [64013, 64014, 6415, 64029, 64057],
    "Chesterfield": [63005, 63006, 63011, 63017, 63141],
    "Joplin": [64801, 64802, 64803, 64804, 64870],
    "University City": [63105, 63124, 63130, 63132],
    "Oakville": [63129, 63151],
    "Cape Girardeau": [63701, 63702, 63703, 63780],


}

rand_city = random.choice(list(cities_zips.keys()))
rand_zip = random.choice(cities_zips[rand_city])


def start_driver(url):

    if (args.cloud == CLOUD_ENABLED):
        LOGGER.setLevel(logging.WARNING)
        #driver = geckodriver("./extensions/Tampermonkey.xpi")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        options.add_argument("window-size=1200x600")
        driver = webdriver.Chrome(
            'chromedriver', options=options)

    else:
        options = webdriver.ChromeOptions()
        options.add_argument(
            "--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument(  # Enable the WebGL Draft extension.
            '--enable-webgl-draft-extensions')
        options.add_argument('--disable-infobars')  # Disable popup
        options.add_argument('--disable-popup-blocking')  # and info bars.
        # chrome_options.add_extension("./extensions/Tampermonkey.crx")
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)

    driver.get(url)

    return driver


def gen_fake_number():
    return "".join(["{}-".format(random.randint(100, 999)), "{}-".format(random.randint(100, 999)), "{}".format(random.randint(100, 999))])


def createFakeIdentity():
    fake_identity = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "address": fake.street_address(),
        "phone_number": gen_fake_number()
    }

    return fake_identity


# def random_email(name=None):
#     if name is None:
#         name = fake.name()

#     mailGens = [lambda fn, ln, *names: fn + ln,
#                 lambda fn, ln, *names: fn + "_" + ln,
#                 lambda fn, ln, *names: fn[0] + "_" + ln,
#                 lambda fn, ln, *names: fn + ln +
#                 str(int(1 / random.random() ** 3)),
#                 lambda fn, ln, *names: fn + "_" + ln +
#                 str(int(1 / random.random() ** 3)),
#                 lambda fn, ln, *names: fn[0] + "_" + ln + str(int(1 / random.random() ** 3)), ]

#     return random.choices(mailGens, MAIL_GENERATION_WEIGHTS)[0](*name.split(" ")).lower() + "@" + requests.get(
#         'https://api.mail.tm/domains').json().get('hydra:member')[0].get('domain')


# def updateFormNumber(fake_identity):
#     # send post request to the server with the data to track the number of reviews
#     requests.post('http://datatracking-gz4c.com/studentloans')


def test_success(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Dropdown-1"))
        )
        return False
    except:
        return True


def fill_out_form(fake_identity, driver, gen_text):

    # Select Education Level

    data_fields = ['Textbox-1', 'Textbox-2', 'Textbox-3', 'Textbox-4',
                   'Textbox-5', 'Textbox-6', 'Textbox-7', 'Textarea-1']

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Dropdown-1"))
    )

    for data in data_fields:
        key_to_send = ''

        if data == 'Textbox-1':
            key_to_send = fake_identity['first_name']
        elif data == 'Textbox-2':
            key_to_send = fake_identity['last_name']
        elif data == 'Textbox-3':
            key_to_send = fake_identity['address']
        elif data == 'Textbox-4':
            key_to_send = rand_city
        elif data == 'Textbox-5':
            key_to_send = rand_zip
        elif data == 'Textbox-6':
            key_to_send = fake_identity['email']
        elif data == 'Textbox-7':
            key_to_send = fake_identity['phone_number']
        elif data == 'Textarea-1':
            key_to_send = gen_text

        # I wanted to be cool with the match/case statement but its not supported in colab :(((

        # match data:
        #     case 'Textbox-1':
        #         key_to_send = fake_identity['first_name']
        #     case 'Textbox-2':
        #         key_to_send = fake_identity['last_name']
        #     case 'Textbox-3':
        #         key_to_send = fake_identity['address']
        #     case 'Textbox-4':
        #         key_to_send = rand_city
        #     case 'Textbox-5':
        #         key_to_send = rand_zip
        #     case 'Textbox-6':
        #         key_to_send = fake_identity['email']
        #     case 'Textbox-7':
        #         key_to_send = fake_identity['phone_number']
        #     case 'Textarea-1':
        #         key_to_send = gen_text

        driver.find_element(
            By.ID, data).send_keys(key_to_send)

    state = Select(driver.find_element(
        By.ID, 'Dropdown-1'))

    state.select_by_value("MO")

    time.sleep(1)
    driver.find_element(
        By.XPATH, "//*[contains(@type,'submit')]").click()

    time.sleep(5)
    return test_success(driver)


if __name__ == "__main__":

    total_forms = 0

    print("Generating Text")

    while True:

        sentence = model("There is a Transgender Center in {}, {} doing ".format(rand_city, rand_zip),
                         do_sample=True, top_k=50,
                         temperature=0.9, max_length=100,
                         num_return_sentences=2)

        gen_text = ''

        print("Generated Text: :", sentence[0]['generated_text'])
        gen_text = str(sentence[0]["generated_text"])

        print('starting new form')
        driver = start_driver(
            url)

        fake_identity = createFakeIdentity()
        time.sleep(1)

        if fill_out_form(fake_identity, driver, gen_text):
            print('Thank you: {} {} for filling out this form'.format(
                fake_identity['first_name'], fake_identity['last_name']))
            total_forms += 1
            print(f"Total Forms: {total_forms}")
            time.sleep(1)
            # updateFormNumber(fake_identity)
        else:
            print(
                "Failed to send, Your IP may have already been registered as filling out the form. No fix at present :(")

        driver.close()
        time.sleep(1)
