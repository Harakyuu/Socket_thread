#Flavio Kenzo Nishiyama TIA: 32031890
#Nicolas Kanamaru de Oliveira TIA: 32050631

import socket
import threading
import time

SERVER_IP = "192.168.86.25"
PORT = 32031
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

#estabelece como servidor

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []
mensagens = []

'''Essa função tem como finalidade, imprimir o nome dos usuários e as mensagens
que enviaram para o shell do servidor e identificar quem está enviando mensagens
para o servidor no momento'''

def enviar_mensagem_individual(conexao):
    print(f"[RECEBENDO] Agora, recebendo mensagens de " + conexao['nome'])

    #percorre a lista das mensagens e imprime a mensagem que o usuário digitou

    for i in range(conexao['last'], len(mensagens)):
        mensagem_splitada = mensagens[i].split("=")
        print(mensagem_splitada[0] + ": " + mensagem_splitada[1])
        conexao['last'] = i + 1

'''Esta função é a responsável por enviar as respostas do servidor para o cliente'''

def confirmar_mensagem_individual():
    for conexao in conexoes: #percorre a lista de conexoes

        '''efetua a mesma coisa que na função acima, porém ela agora 
        envia os dados da mensagem e usuário para o cliente'''

        for i in range(conexao['last'], len(mensagens)):
            mensagem_de_envio = "msg=" + mensagens[i]
            conexao['conn'].send(mensagem_de_envio.encode())
            conexao['last'] = i + 1 

'''Esta função vai gerenciar a chegada dos dados da mensagem'''

def handle_clientes(conn, addr):
    print(f"[NOVA CONEXAO] Um novo usuario se conectou pelo endereço {addr}")
    global conexoes
    global mensagens
    nome = False

    while(True):

        #recebe os dados

        msg = conn.recv(1024).decode(FORMATO)
        if(msg):

            '''Se o dado for o nome do usuário, ela pega o nome do usuário, a conexao 
            e endereço definidos e passa para uma variável chamada mapa_de_conexao,
            ela então chama a função enviar_mensagem_inidicidual passando
            como parâmetro, essa variavel'''

            if(msg.startswith("nome=")):
                mensagem_separada = msg.split("=")
                nome = mensagem_separada[1]
                mapa_da_conexao = {
                    "conn": conn,
                    "addr": addr,
                    "nome": nome,
                    "last": 0
                }
                conexoes.append(mapa_da_conexao)
                enviar_mensagem_individual(mapa_da_conexao)

                '''Se o dado for a mensagem em si, ela pega a mensagem e atribui ao 
                usuario que digitou ela e salva na variável mensagem, após isso, ela 
                chama a função confirmar_mensagem_individual'''

            elif(msg.startswith("msg=")):
                mensagem_separada = msg.split("=")
                mensagem = nome + "=" + mensagem_separada[1]
                mensagens.append(mensagem)
                confirmar_mensagem_individual()
                
'''Essa função ela é responsável por inicializar o servidor, estabelecer a conexão
entre o cliente e o servidor e inicializar a thread que rodará a função de handle_cliente'''

def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

#inicializa o servidor
 
start()