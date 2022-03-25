#Flavio Kenzo Nishiyama TIA: 32031890
#Nicolas Kanamaru de Oliveira TIA: 32050631

import socket
import threading
import time

PORT = 32031 
FORMATO = 'utf-8' 
SERVER = "192.168.86.25" 
ADDR = (SERVER, PORT) 

#faz a conexão com o servidor

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

'''Essa função serve como resposta de confirmação do servidor 
para as mensagens enviadas pelo própio usuário e de outros também.
Ela mostra quem mandou a mensagem e o seu conteúdo em si'''

def handle_mensagens():
    while(True):

        #recebe resposta do servidor e se respondido, imprime a mensagem

        msg = client.recv(1024).decode() 
        if msg:
            mensagem_splitada = msg.split("=")
            print(mensagem_splitada[1] + " mandou a seguinte mensagem: " + mensagem_splitada[2])

'''As funções enviar_mensagem e enviar_nome, como o própio nome diz,
faz o envio da mensagem e do remetente ao servidor usando a função 
enviar para codificar para o formato UTF-8. A função iniciar_envio,
inicializa essas duas funções'''

def enviar(mensagem):
    client.send(mensagem.encode(FORMATO))

def enviar_mensagem():
    mensagem = input("Digite uma mensagem: ")
    enviar("msg=" + mensagem)

def enviar_nome():
    nome = input('Digite seu nome: ')
    enviar("nome=" + nome)

def iniciar_envio():
    enviar_nome()
    enviar_mensagem()

'''A função iniciar faz todo o processo do cliente funcionar,
ele primeiro inicializa as threads e atribui as funções handle_mensagens
e iniciar_envio, e então roda essas duas threads'''

def iniciar():
    thread1 = threading.Thread(target=handle_mensagens)
    thread2 = threading.Thread(target=iniciar_envio)
    thread1.start()
    thread2.start()

#inicializa o código todo do cliente

iniciar()