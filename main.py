import requests as rq
import selectorlib
import smtplib, ssl, os, time
import sqlite3 as sq

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
        print("Email Sent")

#print('email sent')

def data_store(filename, data):

    with open(filename,'a') as file:
        file.write(data + '\n')

def data_read(data_file):

    with open(data_file,'r') as file:
        content = file.read()
        return content
    
def db_write(data_list):

    conn = sq.connect('/mnt/c/Users/olwethu.mbane/Documents/data.db')
    cur = conn.cursor()

    band, city, date = data_list

    query = """
INSERT INTO events
VALUES (?,?,?)
"""

    cur.executemany(query, [(band, city, date)])

    conn.commit()
    conn.close()
    
def db_read(data_list):

    conn = sq.connect('/mnt/c/Users/olwethu.mbane/Documents/data.db')
    cur = conn.cursor()

    band, city, date = data_list

    query = """
SELECT * FROM events
WHERE band = ? AND city = ? AND date = ?
"""
    cur.execute(query, (band, city, date))

    result = cur.fetchall()

    return result



if __name__ == "__main__":  
    while True:
        html = get_html_source_code(URL)
        scraped_data = scrape_html(html)
        print(scraped_data)

        scraped_data_list = scraped_data.split(',')
        scraped_data_tuple = tuple(scraped_data_list)
        scraped_data_tuple_list = [scraped_data_tuple]
    

        if scraped_data_list != ['No upcoming tours']:

            read_db_data = db_read(scraped_data_list)
            print(read_db_data)
            

            if  scraped_data_tuple_list != read_db_data:
                db_write(scraped_data_list)
                
                email_message = "Subject: Latest Tour"\
                + '\n' + scraped_data

                email_message = email_message.encode("utf-8")

                send_email(email_message)

        time.sleep(2)
            