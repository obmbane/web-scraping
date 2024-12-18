import requests as rq
import selectorlib
import smtplib, ssl, os, time
import sqlite3 as sq

URL = "https://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event():

    def get_html(self, url):
        
        response = rq.get(url,headers=HEADERS)
        source_code = response.text

        return source_code

    def scrape_html(self, source_code):

        scraper = selectorlib.Extractor.from_yaml_file('extract.yaml')
        value = scraper.extract(source_code)['tours']

        return value


class Email():

    def send(self, message):
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


class DatabaseSQL():

    def __init__(self,db_name):

        self.connection = sq.connect(f'/mnt/c/Users/olwethu.mbane/Documents/{db_name}.db')

    def write(self, table, data):

        data_list = data.split(',')
        clean_data_list = [item.strip() for item in data_list]
        band, city, date = clean_data_list

        query = f"INSERT INTO {table} VALUES (?,?,?)"

        cur = self.connection.cursor()
        cur.executemany(query, [(band, city, date)])
        self.connection.commit()
        
    def read(self, table, data):

        data_list = data.split(',')
        clean_data_list = [item.strip() for item in data_list]
        band, city, date = clean_data_list

        query = f" SELECT * FROM {table} WHERE band = ? AND city = ? AND date = ? "

        cur = self.connection.cursor()
        cur.execute(query, (band, city, date))
        result = cur.fetchall()

        return result


if __name__ == "__main__":
    
    db_name = 'test'
    table_name = 'events'
    conn = sq.connect(f'/mnt/c/Users/olwethu.mbane/Documents/{db_name}.db')

    while True:
        event = Event()
        source_code = event.get_html(URL)
        event_data = event.scrape_html(source_code)
        print(type(event_data))
    
        if event_data != 'No upcoming tours':
            db = DatabaseSQL(db_name)
            print(event_data)
            read_db_data = db.read(table=table_name, data=event_data)
            
            if  not read_db_data:
                print('test2')
                db.write(table=table_name,data=event_data )
                
                email_message = "Subject: Latest Tour"\
                + '\n' + event_data

                email_message = email_message.encode("utf-8")
                email = Email()
                email.send(email_message)

        time.sleep(2)        