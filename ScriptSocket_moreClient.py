import socket
import threading
import sys

server_ip = ''
server_port = 1024

def leggi(client_socket):
    while True:
        risposta = client_socket.recv(1024).decode()

        if not risposta:
            print("Connessione terminata per", client_socket.getpeername())
            break

        print(risposta)

def scrivi(client_socket):
    while True:
        messaggio = input()

        if messaggio.lower() == "exit":
            print("Connessione terminata per", client_socket.getpeername())
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
            break

        client_socket.send(messaggio.encode())

def gestisci_connessione(client_socket):
    print("Connessione accettata da", client_socket.getpeername())

    leggi_thread = threading.Thread(target=leggi, args=(client_socket,))
    scrivi_thread = threading.Thread(target=scrivi, args=(client_socket,))

    leggi_thread.start()
    scrivi_thread.start()

    leggi_thread.join()
    scrivi_thread.join()

    client_socket.close()

def avvia_server():
    global server_ip
    global server_port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print("Server in ascolto su", server_ip, "porta", server_port)

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=gestisci_connessione, args=(client_socket,))
        client_thread.start()

def avvia_client():
    global server_ip
    global server_port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    leggi_thread = threading.Thread(target=leggi, args=(client_socket,))
    scrivi_thread = threading.Thread(target=scrivi, args=(client_socket,))

    leggi_thread.start()
    scrivi_thread.start()

    leggi_thread.join()
    scrivi_thread.join()

    client_socket.close()

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

#Main
if __name__ == "__main__":
    scelta = input("Sei il server (S) o il client (C)? ")

    if scelta.lower() == "s":
        server_ip = get_local_ip()
        avvia_server()
    elif scelta.lower() == "c":
        server_ip = '192.168.50.66'
        avvia_client()
    else:
        print("Scelta non valida.")
