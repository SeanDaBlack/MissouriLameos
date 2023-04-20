import requests
from main import createFakeIdentity, gen_text
import random
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

fake_identity = createFakeIdentity()

headers = {
    'authority': 'ago.mo.gov',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryp2tIeeBbk6vqBZkv',
    'dnt': '1',
    'origin': 'https://ago.mo.gov',
    'referer': 'https://ago.mo.gov/file-a-complaint/transgender-center-concerns?sf_cntrl_id=ctl00%24MainContent%24C001',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

params = {
    'sf_cntrl_id': 'ctl00$MainContent$C001',
}

data = '------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="TextFieldController_4"\r\n\r\n{fname}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="TextFieldController_5"\r\n\r\n{lname}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="TextFieldController_1"\r\n\r\n{address}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="TextFieldController_2"\r\n\r\n{city}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="DropdownListFieldController"\r\n\r\n{state}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="TextFieldController_6"\r\n\r\n{zip}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="TextFieldController_0"\r\n\r\n{email}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="TextFieldController_3"\r\n\r\n{phone_number}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="ParagraphTextFieldController"\r\n\r\n{prompt}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="captcha-a"\r\n\r\n{capt_a}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="captcha-ca"\r\n\r\n{captcha_ca}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="captcha-iv"\r\n\r\n{captcha_iv}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv\r\nContent-Disposition: form-data; name="captcha-k"\r\n\r\n{}\r\n------WebKitFormBoundaryp2tIeeBbk6vqBZkv--\r\n'.format(

    fname=fake_identity['first_name'],
    lname=fake_identity['last_name'],
    address=fake_identity['address'],
    state="MO",
    city=rand_city,
    zip=rand_zip,
    email=fake_identity['email'],
    phone_number=fake_identity['phone_number'],
    prompt=gen_text(),
    captcha_a='1HL4D',
    captcha_ca='dTKDRTbiLNz6mh5b8sdwn91',
    captcha_iv='WxJZLttR49PoiTyXsLP7wg==',
    captcha_k='kCxLS0o9Zk4f0UCRlt10OCmTENjml+jQK1x4A2jvwZbiHr4067yv0hVEcR2TFnyda91LXaeGQK5VrpslHv3MwA=='

)

response = requests.post(
    'https://ago.mo.gov/file-a-complaint/transgender-center-concerns',
    params=params,
    headers=headers,
    data=data,
)

with open('output.html', 'wb') as f:
    f.write(response.content)
