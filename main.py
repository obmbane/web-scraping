import requests as rq
import selectorlib
import smtplib, ssl, os

URL = "https://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_html_source_code(url):
    
    response = rq.get(url,headers=HEADERS)
    source_code = response.text

    return source_code

def scrape_html(source_code):

    scraper = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = scraper.extract(source_code)['tours']

    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = 'obmbanetraining@gmail.com'
    password = 'jrsg cigg dafz csci'
    receiver = 'obmbanetraining@gmail.com'

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:

        server.login(username,password)
        server.sendmail(username, receiver, message)

#print('email sent')

def store_scraped_values(data):

    with open('data.txt','a') as file:
        file.write(data + '\n')

def data_check(data_file):

    with open(data_file,'r') as file:
        content = file.read()
        return content

if __name__ == "__main__":  

    html = get_html_source_code(URL)
    scraped_data = scrape_html(html)
    print(type(scraped_data))

    data_store = store_scraped_values(scraped_data)
    email_message = "Subject: Latest Tour"\
        + '\n' + scraped_data
        
    email_message = email_message.encode("utf-8")
    file_content = data_check('data.txt')

    if scraped_data != "No upcoming tours":
        if scraped_data not in file_content:
            send_email(email_message)
            print('email sent')