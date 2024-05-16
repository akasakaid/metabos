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
from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import RequestWebViewRequest
from telethon.errors import SessionPasswordNeededError
from phonenumbers import is_valid_number as valid_number, parse as pp
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

    def login(self, phone):
        session_folder = "session"
        api_id = 2040
        api_hash = "b18441a1ff607e10a989891a5462e627"

        if not os.path.exists(session_folder):
            os.makedirs(session_folder)

        if not valid_number(pp(phone)):
            self.log(f"{merah}phone number invalid !")
            sys.exit()

        client = TelegramClient(
            f"{session_folder}/{phone}", api_id=api_id, api_hash=api_hash
        )
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
                code = input(f"{putih}input login code : ")
                client.sign_in(phone=phone, code=code)
            except SessionPasswordNeededError:
                pw2fa = input(f"{putih}input password 2fa : ")
                client.sign_in(phone=phone, password=pw2fa)

        me = client.get_me()
        first_name = me.first_name
        last_name = me.last_name
        username = me.username
        self.log(f"{putih}Login as {hijau}{first_name} {last_name}")
        res = client(
            RequestWebViewRequest(
                peer=self.peer,
                bot=self.peer,
                platform="Android",
                url="https://game.metaboss.xyz/test/",
                from_bot_menu=False,
            )
        )
        tg_data = unquote(res.url.split("#tgWebAppData=")[1]).split(
            "&tgWebAppVersion="
        )[0]

        dict_data = {}
        for i in unquote(tg_data).split("&"):
            key, value = i.split("=")
            dict_data[key] = value

        data = {
            "id": me.id,
            "username": f"{first_name} {last_name}",
            "hash": dict_data["hash"],
        }
        open("data.json", "w").write(json.dumps(data, indent=4))
    
    def main(self):
        banner = f"""
    {hijau}METABOS AUTO DEFEAT BOS

    {putih}By: t.me/AkasakaID
    Github: @AkasakaID

    {kuning}Warning !
    All risks are borne by user !
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        if not os.path.exists("data.json"):
            open("data.json", "w").write(
                json.dumps({"id": "", "username": "", "hash": ""}, indent=4)
            )
            phone = input(f"{biru}input telegram phone number : ")
            self.login(phone)

        data = json.loads(open("data.json", "r").read())
        if len(str(data["id"])) <= 0 or len(data["username"]) <= 0 or len(data["hash"]) <= 0:
            phone = input(f"{biru}input telegram phone number : ")
            self.login(phone)
            
        data = json.loads(open("data.json", "r").read())
        while True:
            try:
                data = json.loads(open("data.json", "r").read())
                data_login_ws = {
                    "code": 1,
                    "type": 2,
                    "data": {
                        "id": data["id"],
                        "username": data["username"],
                        "hash": data["hash"],
                        "timeAuth": int(time.time()),
                    },
                }

                ws = websocket.WebSocket()
                ws.connect("wss://api.metaboss.xyz:2000/game",timeout=10)
                ws.send(json.dumps(data_login_ws))
                result = ws.recv()
                res = json.loads(result)
                coin = None
                name = None
                if "data" not in res.keys():
                    self.log(f'{merah}something wrong !')
                    self.log(f'{merah}"data" not found !')
                    self.log(f'{merah}{res}')
                    sys.exit()

                data = res["data"]
                if "coin" in data.keys():
                    coin = data["coin"]
                if "name" in data.keys():
                    name = data["name"]
                self.log(f"{hijau}Name : {putih}{name}")
                self.log(f"{putih}Your coin : {hijau}{coin}")
                print("~" * 50)
                if name is None or coin is None:
                    print("your name is none or coin is none, maybe your data is invalid !")
                    sys.exit()

                while True:
                    ws_data = {"code":1,"type":7,"data":{}}
                    ws.send(json.dumps(ws_data))
                    result = ws.recv()
                    res = json.loads(result)
                    if "data" not in res.keys():
                        self.log(f'{merah}something wrong !')
                        self.log(f'{merah}"data" not found !')
                        self.log(f'{merah}{res}')
                        sys.exit()

                    data = res["data"]
                    if "remain" in data.keys():
                        remain = data["remain"]
                        if remain != 0:
                            self.log(f'{kuning}there no boss to defeat !')
                            print("~" * 50)
                            if len(str(remain)) == 6:
                                countdown = "".join(list(str(remain))[0:3])
                            if len(str(remain)) == 7:
                                countdown = "".join(list(str(remain))[0:4])
                            self.countdown(int(countdown))
                            break

                        while True:
                            ws_data = {"code":1,"type":3,"data":{}}
                            ws.send(json.dumps(ws_data))
                            result = ws.recv()
                            res = json.loads(result)
                            if "data" in res.keys():
                                data = res["data"]
                                if "hpBoss" in data.keys():
                                    hp_boss = data["hpBoss"]
                                if "coin" in data.keys():
                                    coin = data["coin"]
                                self.log(f'{hijau}current hp bos : {putih}{hp_boss}')
                                self.log(f'{hijau}your coin : {putih}{coin}')
                                if hp_boss <= 0:
                                    self.log(f"{kuning}the bos has defeat !")
                                    print("~" * 50)
                                    break
                                
                                print("~" * 50)
                                time.sleep(2)
            except (TimeoutError,websocket._exceptions.WebSocketTimeoutException):
                self.log(f'{merah}connection timeout,{kuning}reconnecting !')
                print("~" * 50)
                continue

if __name__ == "__main__":
    try:
        MetaBossBot().main()
    except KeyboardInterrupt:
        sys.exit()

