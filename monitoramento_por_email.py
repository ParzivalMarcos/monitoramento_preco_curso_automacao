from selenium import webdriver
import schedule
import time
import os
from mail_module import Emailer
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chromedriver = os.environ.get('CHROMEDRIVER_PATH')


# Configurações para deploy no heroku
chrome_options.add_argument('--headless')  # Roda sem o navegador aberto
chrome_options.add_argument('--disable-dev-shm-usage')  # Roda em maquinas leves
chrome_options.add_argument('--no-sandbox')  # Para servidores linux
driver = webdriver.Chrome(executable_path=chromedriver)

# Acessando site para monitorar
driver.get('https://cursoautomacao.netlify.app/dinamico')


def verificar_mudancas():
    # driver.get(driver.current_url)
    preco = driver.find_element_by_xpath("//li[@id='BasicPlan']")

    if preco.text != 'R$ 9.99 / ano':
        mensagem = f'O preço foi alterado para {preco.text}'
        enviar_email(mensagem)

    elif preco.text == 'R$ 9.99 / ano':
        print('O preço continua o mesmo')


def enviar_email(mensagem):
    mail = Emailer(email_remetente=os.environ.get('EMAIL_REMETENTE'),
                        senha_email=os.environ.get('SENHA_EMAIL'))
    lista_contatos = ['marcosmarinhodev@gmail.com']    
    mail.conteudo_email('O preço foi ALTERADO!',lista_contatos, mensagem)
    mail.enviar(1)


schedule.every(2).minutes.do(verificar_mudancas)

while True:
    schedule.run_pending()
    time.sleep(1)

