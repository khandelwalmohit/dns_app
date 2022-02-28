import socket, requests, json
from statistics import median
from flask import Flask, request

app = Flask(__name__)

@app.route('/fibonacci')
def fib():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")
    num = request.args.get('number')

    if hostname is None or fs_port is None or as_ip is None or as_port is None or num is None or not fs_port.isnumeric() or not as_port.isnumeric():
        return "Bad Request", 400
    
    fs_port = int(fs_port)
    as_port = int(as_port)

    dns_query = {"NAME": hostname, "TYPE":"A"}
    dns_query = json.dumps(dns_query)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(dns_query.encode(), (as_ip, as_port))
    message, addr = client.recvfrom(2048)

    dns_resp = json.loads(message.decode())
    ans = requests.get("http://"+dns_resp['VALUE']+":"+str(fs_port)+"/fibonacci?"+"number="+num)
    return ans.text, ans.status_code

app.run(host='0.0.0.0',
        port=8080)