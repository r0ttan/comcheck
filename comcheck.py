import requests
import time
import sys

currstate = True
prevstate = currstate
statusrow = []

servers = ['http://www.msftncsi.com/ncsi.txt',
           'https://github.com/',
           'http://www.google.com/appsstatus#hl=sv&v=status',
           'https://status.aws.amazon.com/',
           'http://www.nasdaq.com/',
           'https://steamstat.us/',
           'https://worldofwarcraft.com/en-us/game/status',
           'https://twitter.com/',
           'https://www.instagram.com/']

def pingcheck(waddr):
    statusrow.clear()
    statusrow.append(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()))
    print("------PINGCHECK------")
    lanstat = ""
    try:
        r = requests.get("http://192.168.0.19")
        lanstat = "Status {} - LAN OK".format(r.status_code)
    except:
        lanstat = "LAN DOWN: {}".format(sys.exc_info()[0])
    statusrow.append(lanstat)
    print(lanstat)
    gatstat = ""
    try:
        r = requests.get("http://192.168.0.1")
        gatstat = "Status {} - Gateway OK".format(r.status_code)
    except:
        gatstat = "Gateway DOWN: {}".format(sys.exc_info()[0])
    statusrow.append(gatstat)
    print(gatstat)
    wanstat = ""
    try:
        r = requests.get(waddr)
        wanstat = "Status {} - WAN OK".format(r.status_code)
        if r.status_code != 200:
            currstate = False
    except ConnectionError as cerr:
        wanstat = "ConnectionError: {}".format(cerr)
    except:
        wanstat = "UnknownError: {}".format(sys.exc_info()[0])
    statusrow.append(wanstat)
    print(wanstat)


def statecheck():
    if currstate != prevstate:
        if currstate != True and prevstate:
            statusrow.append("Curr:{}, Prev:{} => {}".format(currstate, prevstate, "Offline"))
            print("Curr:", currstate, "\nPrev:", prevstate, "\nOffline")
        if currstate and prevstate != True:
            statusrow.append("Curr:{}, Prev:{} => {}".format(currstate, prevstate, "Back online"))
            print("Curr:", currstate, "\nPrev:", prevstate, "Back online")
    else:
        statusrow.append("Curr:{}, Prev:{} => {}".format(currstate, prevstate, "No change"))
        print("Curr:", currstate, "\nPrev:", prevstate, "\nNo change")

def logme(loglist):
    with open("comcheck.log", "a") as lf:
        lf.write(', '.join(loglist))
        lf.write('\n')

def storedown(filename):
    with open(filename, 'a') as f:
        pass
    return 0

if __name__ == "__main__":
    for i in range(500):
        for s in servers:
            print("Loop:{} Checking: {}".format(i, s))
            #'https://https://github.com'
            #http://www.msftncsi.com/ncsi.txt
            pingcheck(s)
            time.sleep(1)
            statecheck()
            logme(statusrow)
            print("===============")
            time.sleep(9)

#loop ping 3 addresses
