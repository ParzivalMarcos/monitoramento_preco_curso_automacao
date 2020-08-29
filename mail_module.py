import os
import smtplib
from email.message import EmailMessage
import imghdr
import time


class Emailer:
    def __init__(self, email_remetente, senha_email):

        # Configurando login
        self.email_remetente = email_remetente
        self.senha_email = senha_email


    def conteudo_email(self, assunto, lista_contatos, conteudo_email):

        self.msg = EmailMessage()
        self.msg['Subject'] = assunto
        self.msg['From'] = self.email_remetente
        self.msg['To'] = ', '.join(lista_contatos)
        self.msg.set_content(conteudo_email)

    
    def anexar_imagens(self, lista_imagens):
        
        for imagem in lista_imagens:
            with open(imagem, 'rb') as arquivo:
                dados = arquivo.read()
                extensao = imghdr.what(arquivo.name)
                nome_arquivo = arquivo.name
            self.msg.add_attachment(dados, maintype='image',
                                    subtype=extensao, filename=nome_arquivo)


    def anexar_arquivos(self, lista_arquivos):
        
        for arquivo in lista_arquivos:
            with open(arquivo, 'rb') as arquivo:
                dados = arquivo.read()
                nome_arquivo = arquivo.name
            self.msg.add_attachment(dados, maintype='application',
                                    subtype='octet-stream', filename=nome_arquivo)


    def enviar(self, intervalo=0):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email_remetente, self.senha_email)
            smtp.send_message(self.msg)
            time.sleep(intervalo)
