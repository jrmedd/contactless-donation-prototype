import binascii, datetime, requests
import Adafruit_PN532 as PN532

CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()

server_ip = "192.168.2.1"
server_url = "http://%s:5000/payment" % (server_ip)

wait_between_payments = 3

card_holder_preset_value = {'4bac6f3f':'5', 'b3de1b6c':'10', '43e4146c':'1'} #preset values for demo-ing with multiple cards
standard_amount = 1

card_holder = None
next_valid_time = datetime.datetime.now() + datetime.timedelta(seconds=wait_between_payments)

while True:
    try:
        uid = pn532.read_passive_target() #try/except here prevents none MiFare cards from crashing the script
    except:
        uid = None
    if uid is None:
        continue
    print "READ"
    card_holder = binascii.hexlify(uid)
    if datetime.datetime.now() > next_valid_time:
        if card_holder != None:
            amount = card_holder_preset_value.get(card_holder)
            if amount == None:
                amount = standard_amount
            payment = requests.get("%s/%s/%s" % (server_url, card_holder, amount))
            next_valid_time = datetime.datetime.now() + datetime.timedelta(seconds=wait_between_payments)
