import socket, random

def getPort(host):
    port = 5050
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_found = False
    while port_found == False:
        try:
            test_socket.bind((host, port))
            test_socket.close()
            port_found = True
            return port
        except:
            print(f"port {port} didn't work...")
            port = random.randint(1000, 6000)

HOST = "192.168.0.111" #socket.gethostbyname(socket.gethostname())
PORT = 5000


TEXT_FORMAT = "utf-8"

MESSAGE_WAS_SENT_SUCCESSFULLY = "1"
MESSAGE_WAS_FAILED_TO_RECEIVE = "2"

ENTITY_STATUS_NEUTRAL = "N"
ENTITY_STATUS_TAKE_DAMAGE = "TD"

NEW_LEVEL_COMING_TRUE = "NLT"
NEW_LEVEL_COMING_FALSE = "NLF"



