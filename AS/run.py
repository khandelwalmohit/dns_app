import socket, requests, json

port = 53533
address =''

AS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
AS.bind((address, port))

while True:
    print("server is running on", port)
    message, clientaddr = AS.recvfrom(2048)

    message = json.loads(message.decode())

    if len(message) == 2:
        print("dns query")
        with open("dns.json", "r") as dns:
            dns_dict = json.load(dns)
        resp = dns_dict[message["NAME"]]
        data = json.dumps(resp)
        AS.sendto(data.encode(),clientaddr)
    
    elif len(message)==4:
        print("register")
        data = {message["NAME"]: message}         
        data = json.dumps(data)
        with open("dns.json", "w") as dns:
            dns.write(data)
        AS.sendto(str(201).encode(), clientaddr)
    
    else:
        AS.sendto(str(500).encode(), clientaddr)


