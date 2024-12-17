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

    username = os.getenv('MY_EMAIL')
    password = os.getenv('APP_PASSWORD')
    receiver = os.getenv('MY_EMAIL')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:

        server.login(username,password)
        server.sendmail(username, receiver, message)
        print("Email Sent")

#print('email sent')
    
def db_write(table, scraped_data):

    cur = conn.cursor()

    data_list = scraped_data.split(',')
    clean_data_list = [item.strip() for item in data_list]
    band, city, date = clean_data_list

    query = f"""
    INSERT INTO {table}
    VALUES (?,?,?)
    """
    cur.executemany(query, [(band, city, date)])

    conn.commit()
    
def db_read(table,scraped_data):

    cur = conn.cursor()

    data_list = scraped_data.split(',')
    clean_data_list = [item.strip() for item in data_list]
    band, city, date = clean_data_list

    query = f"""
    SELECT * FROM {table}
    WHERE band = ? AND city = ? AND date = ?
    """
    cur.execute(query, (band, city, date))
    result = cur.fetchall()

    return result


if __name__ == "__main__":

    db_name = 'music_events'
    db_table_name = 'events'
    conn = sq.connect(f'/mnt/c/Users/olwethu.mbane/Documents/{db_name}.db')
    while True:
        html = get_html_source_code(URL)
        scraped_data = scrape_html(html)
    
        if scraped_data != 'No upcoming tours':
            print(scraped_data)

            read_db_data = db_read(db_table_name, scraped_data)
            
            if  not read_db_data:
                print('test2')
                db_write(db_table_name, scraped_data)
                
                email_message = "Subject: Latest Tour"\
                + '\n' + scraped_data

                email_message = email_message.encode("utf-8")

                send_email(email_message)

        time.sleep(2)

    conn.close()        