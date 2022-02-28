import socket, requests, json
from flask import Flask, request

app = Flask(__name__)

@app.route('/fibonacci')
def get_num():
    x = request.args.get('number')
    if x.isnumeric():
        x= int(x)
        return str(fib(x)), 200
    else:
        return "Bad Format", 400
    
def fib(x):
    if x==0:
        return 0
    elif x==1 or x==2:
        return 1
    else:
        return fib(x-1) + fib(x-2)
    

@app.route('/register', methods=['PUT'])
def register():
    hostname = request.args.get('hostname')
    FSip = request.args.get('ip')
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port'))

    data = {
        "TYPE" : "A",
        "NAME" : hostname,
        "VALUE" : FSip,
        "TTL" : 10
    }

    data = json.dumps(data)
    print(" request to register sent")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(data.encode(),(as_ip,as_port))
    message , addr = client.recvfrom(2048)

    message = message.decode()
    if message == '201':
        return "Registration with AS successfull", 201
    else:
        return "Error, something is wrong", 500

app.run(host='0.0.0.0',
        port=9090)