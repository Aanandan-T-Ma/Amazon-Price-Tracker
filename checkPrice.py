import scrap, creds
import pymongo
import smtplib

def priceReduced(url, price):
    d = scrap.getDetails(url)
    if d[1] < price:
        return d[1]
    return False

def sendMail(toMail, link):
    fromMail = 'aanandan.tma@gmail.com'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromMail, creds.password)

    subject = 'Amazon Prices Came Down!'
    body = f'Check out the link {link}'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(fromMail, toMail, msg)
    #print('Email sent!')
    server.quit()

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['price_tracker']
trackers = db['trackers']

print('Tracking Started...')

while True:
    products = trackers.find()
    for p in products:
        reduced = priceReduced(p['link'], p['price'])
        if reduced:
            p['price'] = reduced
            sendMail(p['email'], p['link'])
            x = trackers.find_one_and_update({ '_id': p['_id'] }, { '$set': { 'price': reduced } })
            #print(x)