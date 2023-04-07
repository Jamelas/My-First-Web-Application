import socket
import _thread
import analysis
import json


class HTTPRequest:
    def __init__(self, cmd, path, prot, headers, payload):
        self.cmd = cmd
        self.path = path
        self.prot = prot
        self.payload = payload
        self.headers = headers


hsep = '\r\n'
authkey = 'MjAwMTk4Mjk6MjAwMTk4Mjk='


def parse(request):
    headers =[]
    reqline = request.decode().split(hsep).pop(0)
    if request.decode():
        headers = request.decode().split(hsep)
        if headers:
            headers.pop()  #remove payload
        if headers:
            headers.pop() #remove empty line
        if headers:
            headers.pop(0)  #remove request line
    payload = request.decode().split(hsep).pop()
    try:
        cmd, path, prot = reqline.split()
    except ValueError:
        cmd = ''
        path = ''
        prot = ''
    return HTTPRequest(cmd, path, prot, headers, payload)


def http_sts(conn, status):
    """Write and send a status line"""
    conn.send(('HTTP/1.1 ' + status + hsep).encode())


def deliver_200(conn):
    http_sts(conn, '200 OK')


def deliver_404(conn):
    http_sts(conn, '404 Not found')


def http_hdr(conn, hdrline):
    """Send the header line input as Python string instance"""
    conn.send((hdrline + hsep).encode())


def http_bdy(conn, payload):
    """Send payload given as byte string"""
    conn.send(hsep.encode())
    conn.send(payload)


def gobble_file(filename, binary=False):
    """General utility to read entire content of file that could be binary"""
    if binary:
        mode = 'rb'
    else:
        mode = 'r'
    with open(filename, mode) as fin:
        content = fin.read()
    return content


def deliver_html(conn, filename):
    """Deliver content of HTML file"""
    deliver_200(conn)
    content = gobble_file(filename)
    http_hdr(conn, 'Content-Type: text/html')
    http_bdy(conn, content.encode())
    print(" - delivering " + filename + " text/html")


def deliver_jpeg(conn, filename):
    """Deliver content of JPEG image file"""
    deliver_200(conn)
    content = gobble_file(filename, binary=True)
    http_hdr(conn, 'Content-Type: image/jpeg')
    http_hdr(conn, 'Accept-Ranges: bytes')
    http_bdy(conn, content)
    print(" - delivering " + filename + " image/jpeg")


def deliver_json(conn, filename):
    """Deliver content of JSON file"""
    deliver_200(conn)
    '''############## Method incomplete - ONLY WORKS WITH input.json ##################'''
    http_hdr(conn, 'Content-Type: application/json')
    http_bdy(conn, json.dumps(analysis.get_data()).encode())
    print(" - delivering " + " application/json")


def deliver_json_str(conn, string):
    deliver_200(conn)
    http_hdr(conn, 'Content-Type: application/json')
    print(string)
    http_bdy(conn, string.encode())

def deliver_js(conn, filename):
    """Deliver content of JavaScript file"""
    deliver_200(conn)
    content = gobble_file(filename)
    http_hdr(conn, 'Content-Type: text/javascript')
    http_bdy(conn, content.encode())
    print(" - delivering " + filename + " text/javascript")


# Confirm if authentication hash matches authentication key
def authorized(headers):
    for line in headers:
        substring = ": "
        if substring not in line:
            continue
        if line == "":
            continue
        k, v = line.split(": ")
        if k == "Authorization":
            v = v.split()
            v = v[1]  # Removes 'Basic' from the authkey
            if v == authkey:
                print("User authorized")
                return True
            else:
                return False


def testrq(httprq, cmd, path):
    if httprq.cmd == cmd and httprq.path == path:
        return True
    else:
        return False


def do_request(connectionSocket):
    request = connectionSocket.recv(11024)
    httprq = parse(request)

    if authorized(httprq.headers):
        print(httprq.cmd, httprq.path)

        if testrq(httprq, 'GET', '/'):
            deliver_html(connectionSocket, 'index.html')

        elif testrq(httprq, 'GET', '/form'):
            deliver_html(connectionSocket, 'psycho.html')

        elif testrq(httprq, 'POST', '/analysis'):
            analysis.save_input(httprq.payload)
            analysis.create_profile()
            deliver_json_str(connectionSocket, '{"status": "success"}')

        elif testrq(httprq, 'GET', '/view/profile'):
            deliver_json(connectionSocket, 'data/input.json')

        elif testrq(httprq, 'GET', '/view/profile'):
            deliver_json(connectionSocket, 'data/profile.json')

        elif testrq(httprq, 'GET', '/doit.js'):
            deliver_js(connectionSocket, 'doit.js')

        elif testrq(httprq, 'GET', '/view/input'):
            deliver_json(connectionSocket, '\\data\\input.json')

        # ... otherwise deliver "Not found" response
        else:
            deliver_404(connectionSocket)

    # Authentication has not been confirmed
    else:
        connectionSocket.send(b'HTTP/1.1 401 Unauthorized\r\n')
        connectionSocket.send(b'WWW-Authenticate: Basic realm="MjAwMTk4Mjk6MjAwMTk4Mjk="')
        print("User not authorized")

    connectionSocket.close()


def main(serverPort):
    # Create the server socket object
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the server socket to the port
    mySocket.bind(('', serverPort))

    # Start listening for new connections
    mySocket.listen()
    print('The server is ready to receive messages on port:', serverPort)

    while True:
        # Accept a connection from a client
        connectionSocket, addr = mySocket.accept()

        # Handle each connection in a separate thread
        _thread.start_new_thread(do_request, (connectionSocket,))
