import requests
import time
import json
import threading

config = json.load(open('./config.json',))

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = config["cookie"]

Threshold = config["threshold"]

class Rolimons:
    values = {}

    def getItemValue(self, ID):
        return self.values[str(ID)]

    def updateValues(self):
        Request = requests.get("https://www.rolimons.com/itemapi/itemdetails")
        self.values = Request.json()["items"]

    def loop(self):
        while True:
            print("<=> Updating Values")
            self.updateValues()
            time.sleep(60*15)

    def __init__(self):
        threading.Thread(target=self.loop).start()

def rblxrequest(method, url, **pars):
    method=method.lower()
    if method in ["post","put","patch","delete","get"]:
        request = session.request(method, url, **pars)
        if "X-CSRF-TOKEN" in request.headers:
            if "errors" in request.json():
                if request.json()["errors"][0]["message"] == "Token Validation Failed":
                    session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
                    request = session.request(method, url, **pars)

        return request

Rolimon = Rolimons()

cachedTrades = []
def removeLater(Value):
    cachedTrades.remove(Value)

while True:
    Trades = rblxrequest("GET", "https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit=100")
    Trades = Trades.json()["data"]

    for Trade in Trades:
        TradeId = Trade["id"]
        if TradeId in cachedTrades:
            continue

        Receive = 0
        Ask = 0

        TradeDetails = rblxrequest("GET", f"https://trades.roblox.com/v1/trades/{TradeId}")
        if TradeDetails.status_code == 429: 
            continue

        TradeDetails = TradeDetails.json()["offers"]

        for Item in TradeDetails[0]["userAssets"]:
            Receive += Rolimon.getItemValue(Item["assetId"])[4]

        for Item in TradeDetails[1]["userAssets"]:
            Ask += Rolimon.getItemValue(Item["assetId"])[4]

        Ratio = 1/Ask*Receive

        print(f"<==> TradeID: {TradeId} | Ratio: {Ratio}")

        if Ratio < Threshold:
            rblxrequest("POST",f"https://trades.roblox.com/v1/trades/{TradeId}/decline")
        else:
            cachedTrades.append(TradeId)
            threading.Timer(60*15, removeLater, [TradeId]).start()

    time.sleep(20)