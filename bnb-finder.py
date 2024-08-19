from modules import init
print("Compiling modules...")
init()
import hashlib
import random
import sys
import time
import requests
from colorama import Fore

def generate_bnb_address():
    private_key = ''.join(random.choice('0123456789abcdef') for i in range(64))
    keccak = hashlib.sha3_256()
    keccak.update(private_key.encode())
    keccak_digest = keccak.hexdigest()
    bnb_address = "0x" + keccak_digest[-40:]
    return private_key, bnb_address
while True:
    bnb_private_key, bnb_address = generate_bnb_address()
    api_key = 'WXWU1HKNC5VTA3R2C2GSXSFA9X28G1I7M2'
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={bnb_address}&tag=latest&apikey={api_key}'
    print(f"Private Key: {bnb_private_key}")
    print(f"Address: {bnb_address}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if the response contains the balance
        if data['status'] == '1':
            balance_bnb = float(data['result']) / 10 ** 18
            print(f"Balance {bnb_address}: {balance_bnb} BNB")
            if balance_bnb > 0.000000000001:
                file = open("data.txt", "w")
                file.write(bnb_address)
                file.write(bnb_private_key)
                file.write(balance_bnb)
                file.close()
                sys.exit()
            else:
                pass
        else:
            print(f"Error: {data['message']}")
    else:
        print("Error: Failed to retrieve data from Bscan API")
    time.sleep(0.4)
