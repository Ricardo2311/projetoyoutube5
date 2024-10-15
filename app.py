import requests
from datetime import datetime
import schedule
from email.message import EmailMessage
from infos import EMAIL_PASSWORD, EMAIL_ADDRESS
import smtplib
from time import sleep
def precoEuro():
    api_cotacoes = 'https://economia.awesomeapi.com.br/last/EUR-BRL'

    requisicao = requests.get(api_cotacoes)

    preco_euro = requisicao.json()['EURBRL']['bid']
    
    return preco_euro


def send_email():
    if float(precoEuro()) <= 6.00:
        mail = EmailMessage()
        mail['Subject'] = 'ALERTA!!! PREÇO DO EURO ESTÁ ABAIXO DE R$6,00!!!'
        mensagem = f'''
        ATENÇÃO, O PREÇO DO EURO NO HORÁRIO {datetime.now().strftime("%H:%M:%S")} ESTÁ {precoEuro()}!!! FIQUE ATENTO PARA COMPRAR!!!
        '''
        mail['From'] = EMAIL_ADDRESS
        mail['To'] = 'rbofarullclaveria@gmail.com'
        mail.add_header('Content-Type','text/html')
        mail.set_payload(mensagem.encode('utf-8'))
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as email:
            email.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            email.send_message(mail)
            print('Email enviado com sucesso!!!')
    else:
        print('Euro ainda está muito caro!!!')

schedule.every(10).seconds.do(precoEuro)
schedule.every(10).seconds.do(send_email)

while True:
    schedule.run_pending()
    sleep(1)





