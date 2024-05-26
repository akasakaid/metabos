"""
Metabos Auto Defeat Boss

Author: @AkasakaID
"""

import sys
import os
import json
import time
import requests
import random
import websocket
from urllib.parse import unquote
from colorama import *

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX


class MetaBossBot:
    def __init__(self):
        self.peer = "metaboss_2024_bot"

    def log(self, message):
        year, mon, day, hour, minute, second, a, b, c = time.localtime()
        mon = str(mon).zfill(2)
        hour = str(hour).zfill(2)
        minute = str(minute).zfill(2)
        second = str(second).zfill(2)
        print(f"{biru}[{year}-{mon}-{day} {hour}:{minute}:{second}] {message}")

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def main(self):
        banner = f"""
    {hijau}METABOS AUTO DEFEAT BOS

    {putih}By: t.me/AkasakaID
    Github: @AkasakaID

    {kuning}Warning !
    All risks are borne by user !
    
    {putih}Message: {hijau}don't forget to 'git pull', maybe i update the bot !
        """
        if "noclear" not in sys.argv:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        if not os.path.exists("data.json"):
            open("data.json", "w").write("# remove this line and paste your data !")
            self.log(f"{kuning}data.json is not found !")
            self.log(f"{kuning}please update your data.json !")
            sys.exit()

        data = json.loads(open("data.json", "r").read())
        if "remove this line" in json.dumps(data):
            self.log(f"{kuning}please update your data.json")
            sys.exit()

        while True:
            try:
                data = json.loads(open("data.json", "r").read())
                login_data = data
                ws = websocket.WebSocket()
                ws.connect("wss://api.metaboss.xyz:2000/game", timeout=10)
                ws.send(json.dumps(login_data))
                result = ws.recv()
                res = json.loads(result)
                coin = None
                name = None
                ton = None
                if "data" not in res.keys():
                    self.log(f"{merah}something wrong !")
                    self.log(f'{merah}"data" not found !')
                    self.log(f"{merah}{res}")
                    sys.exit()

                data = res["data"]
                if "coin" in data.keys():
                    coin = data["coin"]
                if "name" in data.keys():
                    name = data["name"]
                if "ton" in data.keys():
                    ton = data["ton"]
                self.log(f"{hijau}Name : {putih}{name}")
                self.log(f"{putih}Your coin : {hijau}{coin}")
                self.log(f"{putih}Your Ton : {hijau}{ton}")
                print("~" * 50)
                if name is None or coin is None:
                    print(
                        "your name is none or coin is none, maybe your data is invalid !"
                    )
                    sys.exit()
                resource = data["resource"]
                if "10" in resource.keys():
                    resource10 = data["resource"]["10"]
                    if int(resource10) > 0:
                        self.log(f"{hijau}open chest !")
                        while int(resource10):
                            data_claim = {"code":1,"type":11,"data":{"type":10}}
                            ws.send(json.dumps(data_claim))
                            for i in range(3):
                                result = ws.recv()
                                res = json.loads(result)
                                if res['code'] == 12:
                                    data = res["data"]
                                    reward = data["number"]
                                    reward_type = None
                                    if data["type"] == 1:
                                        reward_type = "coin"
                                    if data["type"] == 2:
                                        reward_type = "ton"
                                    self.log(f"{putih}get reward {hijau}{reward} {reward_type}")

                while True:
                    ws_data = {"code": 1, "type": 7, "data": {}}
                    ws.send(json.dumps(ws_data))
                    result = ws.recv()
                    res = json.loads(result)
                    if "data" not in res.keys():
                        self.log(f"{merah}something wrong !")
                        self.log(f'{merah}"data" not found !')
                        self.log(f"{merah}{res}")
                        sys.exit()

                    data = res["data"]
                    if "remain" in data.keys():
                        remain = data["remain"]
                        if remain != 0:
                            self.log(f"{kuning}there no boss to defeat !")
                            print("~" * 50)
                            if len(str(remain)) == 6:
                                countdown = "".join(list(str(remain))[0:3])
                            if len(str(remain)) == 7:
                                countdown = "".join(list(str(remain))[0:4])
                            self.countdown(int(countdown))
                            break

                        while True:
                            ws_data = {"code": 1, "type": 3, "data": {}}
                            ws.send(json.dumps(ws_data))
                            result = ws.recv()
                            res = json.loads(result)
                            if "data" in res.keys():
                                data = res["data"]
                                if "hpBoss" in data.keys():
                                    hp_boss = data["hpBoss"]
                                if "coin" in data.keys():
                                    coin = data["coin"]
                                self.log(f"{hijau}current hp bos : {putih}{hp_boss}")
                                self.log(f"{hijau}your coin : {putih}{coin}")
                                if hp_boss <= 0:
                                    self.log(f"{kuning}the bos has defeat !")
                                    print("~" * 50)
                                    break

                                print("~" * 50)
                                time.sleep(2)
            except (TimeoutError, websocket._exceptions.WebSocketTimeoutException):
                self.log(f"{merah}connection timeout,{kuning}reconnecting !")
                print("~" * 50)
                continue


if __name__ == "__main__":
    try:
        MetaBossBot().main()
    except KeyboardInterrupt:
        sys.exit()
