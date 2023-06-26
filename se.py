import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
from twilio.rest import Client

# 设置网站URL和要搜索的价格元素class
url = 'https://studentexperience.com/studios?countryId=166'

def email_alert(message):
    sender_email = "your email"
    receiver_email = "your email"
    password = "your password"
    smtp_server = "smtp of your email"
    # for example, if it's outlook email, than the smtp is "smtp.office365.com"
    # if it's gmail, smtp is "smtp.gmail.com"
    port = your email port number
    # for example, if it's outlook, than the port number is 587
    # if it's gmail, port number is 465

    server = smtplib.SMTP(smtp_server, port)
    server.connect(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()

def text_alert(message):
    # this part is achived by twilio

    account_sid = 'your twilio account sid'
    auth_token = 'your twilio auth token'
    from_number = 'your twilio number'
    to_number = 'your actual number'

    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
                body=message,
                from_=from_number,
                to=to_number
        )

# the program stops when it finds vailable studios
found = False

def job():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    filter_group = soup.find_all('div', {'class': 'filter-group'})
    filter = filter_group[1].find_all('div', {'class': 'filter'})
    amount = int(filter[1].find('span', {'class': 'amount'}).text)
    
    if amount == 0 : print('nothing')
    if amount > 0:
        subject = "New Studio Alert!"
        body = "The available number is" + str(amount) + "\n"
            
        body += "click the url:" + url + "\n"
        message = f"Subject: {subject}\n\n{body}"
        message = message.encode('utf-8') 
        email_alert(message)
        text_alert(message) 

        global found 
        found = True

# program runs every 3 seconds
schedule.every(3).seconds.do(job)

while not found:
    schedule.run_pending()