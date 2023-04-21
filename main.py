import argparse
import random
import time
import base64
import requests
from faker import Faker
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import speech_recognition as sr
from pydub import AudioSegment
# from bs4 import BeautifulSoup
# from emails import MAIL_GENERATION_WEIGHTS
from selenium import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from transformers import pipeline
from proxy import get_proxies
import cv2 as cv
import pytesseract as tesseract

# model = pipeline("text-generation", model="gpt2")
tesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

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


def start_driver(url, proxy):

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
        # if proxy != "":
        #     options.add_argument(f'--proxy-server={proxy}')
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

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Dropdown-1"))
        )
    except:
        print("proxy failed. normal cause i'm a cheap boy")
        return

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


def test_success(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Dropdown-1"))
        )
        return False
    except:
        return True


r = sr.Recognizer()


# def most_frequent(List):
#     try:
#         return max(set(List), key=List.count)
#     except:
#         return '0'


# def at_lest_5(string):
#     return len(string) == 5


def audio_to_text(file):

    with sr.AudioFile(file) as source:
        r.adjust_for_ambient_noise(source)
        # r.energy_threshold = 150
        # r.adjust_for_ambient_noise()
        audio_text = r.record(source, offset=6)
        try:
            text = r.recognize_google(audio_text, show_all=True)
            print(f'Converting audio transcripts into text ...')
            return(text)
        except Exception as e:
            print(e)
            print(f'Sorry.. run again...')


def img_fill_test(fake_identity, driver, gen_text):

    # img_src = driver.find_element(By.XPATH,
    #                               '/html/body/main/div[2]/div[1]/div/div/form/div[11]/div[1]/img').get_attribute('src')

    # # print(img_src)
    # file_decode = base64.b64decode(
    #     img_src.split("data:image/png;base64,")[1])
    # file_result = open('file.png', 'wb')
    # file_result.write(file_decode)

    gray = cv.imread('file.png', 0)
    # cv.threshold(gray, gray, 231, 255, cv.THRESH_BINARY)
    # api = tesseract.TessBaseAPI()
    # api.Init(".", "eng", tesseract.OEM_DEFAULT)
    # api.SetVariable("tessedit_char_whitelist",
    #                 "0123456789abcdefghijklmnopqrstuvwxyz")
    # api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    # tesseract.SetCvImage(gray, api)
    # print(api.GetUTF8Text())
    print(tesseract.image_to_string(gray))


def test_fill_out_form(fake_identity, driver, gen_text):

    done = False

    while not done:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/main/div[2]/div[1]/div/div/form/div[11]/div[1]/audio"))
        )

        audio_src = driver.find_element(By.XPATH,
                                        '/html/body/main/div[2]/div[1]/div/div/form/div[11]/div[1]/audio').get_attribute('src')
        # content = requests.get(audio_src).content

        print('saving...')
        final = []

        file_decode = base64.b64decode(
            audio_src.split("data:audio/wav;base64,")[1])
        file_result = open('file.wav', 'wb')
        file_result.write(file_decode)

        song = AudioSegment.from_wav("file.wav")

        # but let's make him *very* quiet
        song = song + 15 + song

        # save the output
        song.export("loud.wav", "wav")

        answer = audio_to_text('loud.wav')
        # print(answer)
        final = []
        for a in answer['alternative']:
            newstring = ''
            AAAA = a['transcript'].lower()

            AAAA = AAAA.replace('pop up', 'papa')
            AAAA = AAAA.replace('pop-up', 'papa')
            AAAA = AAAA.replace('climate', 'lima')
            AAAA = AAAA.replace('for', '4')
            AAAA = AAAA.replace('four', '4')
            AAAA = AAAA.replace('x-ray', 'xray')
            AAAA = AAAA.replace('x ray', 'xray')

            # print(AAAA)

            for i in AAAA.split(' '):
                if i.isalpha():
                    newstring += i[0][0].upper()
                elif i.isnumeric() or i.isalnum():
                    for x in i.split():  # [2, 7]
                        if x.isnumeric():
                            newstring += x

            last_key = list(newstring)
            # y = last_key.pop(0)
            # last_key.append(y)

            final.append("".join(last_key))

        # final.append(last_key)
        # print(final)
        # final = []
        # a = answer.split(' ')  # [Hotel, 27, Zulu, Echo]
        # newstring = ''
        # for i in a:
        #     if i.isalpha():
        #         newstring += i[0][0]
        #     elif i.isnumeric():
        #         for x in i.split():  # [2, 7]
        #             print(x)
        #             newstring += x

        #   final.append(newstring)
        if at_lest_5(most_frequent(final)):

            print(most_frequent(final))
            done = True
        else:
            print(most_frequent(final))
            print('not done')

    time.sleep(10000)


def fill_out_form(fake_identity, driver, gen_text):

    # Select Education Level

    data_fields = ['Textbox-1', 'Textbox-2', 'Textbox-3', 'Textbox-4',
                   'Textbox-5', 'Textbox-6', 'Textbox-7', 'Textarea-1']

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Dropdown-1"))
        )
    except:
        print("proxy failed. normal cause i'm a cheap boy")
        return False

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


def gen_text():
    gen_text = ''

    model = pipeline("text-generation", model="gpt2")

    sentence = model("There is a Transgender Center in {}, {} doing ".format(rand_city, rand_zip),
                     do_sample=True, top_k=50,
                     temperature=0.9, max_length=100,
                     num_return_sentences=2)

    print("Generated Text: :", sentence[0]['generated_text'])
    gen_text = str(sentence[0]["generated_text"])
    return gen_text


def get_cap_data(driver):

    return {driver.find_element(
        By.XPATH, "//*[contains(@name,'captcha-ca')]").get_attribute('value'),
        driver.find_element(
        By.XPATH, "//*[contains(@name,'captcha-iv')]").get_attribute('value'),
        driver.find_element(
        By.XPATH, "//*[contains(@name,'captcha-k')]").get_attribute('value')}


if __name__ == "__main__":

    total_forms = 0

    print("Generating Text")
    # gen_text = gen_text()
    gen_text = ''
    proxy = ''
    # proxies = get_proxies()

    proxies = ['1', 2, 3, 4, 5]

    for proxy in proxies:

        print('starting new form')
        # driver = start_driver(
        #     url, proxy)
        driver = ''

        fake_identity = createFakeIdentity()
        time.sleep(1)

        print('filling out form now')
        if img_fill_test(fake_identity, driver, gen_text):
            time.sleep(10000)
            print('Thank you: {} {} for filling out this form'.format(
                fake_identity['first_name'], fake_identity['last_name']))
            total_forms += 1
            print(f"Total Forms: {total_forms}")
            time.sleep(1)
            # updateFormNumber(fake_identity)
        else:
            print(
                "Failed to send, Your IP may have already been registered as filling out the form. No fix at present :(")
        try:
            driver.close()
        except:
            pass
        time.sleep(1)
