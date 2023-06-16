import socket
import threading
import sys
import time

server_ip = ''
server_port = 1024

def leggi(client_socket):
    while True:

        #riceviamo i dati
        risposta = client_socket.recv(1024).decode()  #accettiamo massimo un byte di messaggio

        #se l'altro termina la connessione
        if not risposta:
            print("Connessione terminata")
            break

        print("\r\033[K --> "+risposta)
    sys.exit()

def scrivi(client_socket):
    while True:
        #per inviare un messaggio
        messaggio = input() #scriviamo il testo del messaggio
        client_socket.send(messaggio.encode())

        #comando per terminare la connessione
        if messaggio.lower() == "exit":
            print("Hai terminato la connessione")
            break
    sys.exit()

def avvia_server():
    #riprendiamo le variabili globali
    global server_ip
    global server_port

    #socket del server, specificando che usiamo un indirizzo IPv4 e il protocollo TCP per i pacchetti
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #colleghiamo il socket a ip e porta
    server_socket.bind((server_ip, server_port))

    #avviamo l'ascolto delle connessioni in arrivo, ne accettiamo solo una
    server_socket.listen(1)
    print("In attesa di connessioni...")

    #accettiamo la connessione del client
    client_socket, client_address = server_socket.accept()
    print("Connessione accettata da ", client_address)

    p1 = threading.Thread(target=leggi, args=(client_socket,))
    p2 = threading.Thread(target=scrivi, args=(client_socket,))

    #dialogo in corso
    p1.start()
    p2.start()

def avvia_client():
    #riprendiamo le variabili globali
    global server_ip
    global server_port

    #socket del client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connettiamo il client al server
    client_socket.connect((server_ip, server_port))

    p1 = threading.Thread(target=leggi, args=(client_socket,))
    p2 = threading.Thread(target=scrivi, args=(client_socket,))

    #dialogo in corso
    p1.start()
    p2.start()

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

#Main
if __name__ == "__main__":
    scelta = input("Sei il server (S) o il client (C)? ")

    if scelta.lower() == "s":
        server_ip = get_local_ip()
        avvia_server()
    elif scelta.lower() == "c":
        server_ip = '192.168.50.70'
        avvia_client()
    else:
        print("Scelta non valida.")
