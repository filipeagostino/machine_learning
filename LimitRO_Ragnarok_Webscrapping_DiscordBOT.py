import discord
import asyncio
import time
import schedule
from urllib.request import urlopen,Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


token = 'YOUR_DISCORD_BOT_TOKEN'

url = 'https://www.limitragnarok.com/vending/items/'
url2 = 'https://www.limitragnarok.com/vending/items/?p='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
try:
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

except HTTPError as e:
    print(e.status, e.reason)

except URLError as e:
    print(e.reason)

client = discord.Client()

@client.event
async def on_ready():
    print('Coe menor! o pai ta on!')


@client.event
async def on_message(message):
    if message.content.lower().startswith('!lojas'):

        contpg = 0
        shopname = []
        vendorname = []
        position = []
        itemname = []
        card0 = []
        card1 = []
        card2 = []
        card3 = []
        options = []
        price = []
        amount = []
        listao = {}

        get = soup.find('p', {'class': 'info-text'}).getText().split(' ')
        get2 = get.index('page(s).')
        get3 = get[get2 - 1]
        pgn = int(get3)
        print(f'No momento existem {pgn} paginas de lojas')

        while contpg < pgn:
            req = Request(f'{url2}{contpg + 1}', headers=headers)
            response = urlopen(req)
            html = response.read().decode('utf-8')
            soup2 = BeautifulSoup(html, 'html.parser')
            contpg += 1
            print(f'este é contpg: {contpg}')

            qtditem = 0
            for i in soup2.find('table', {'class': 'horizontal-table'}).findAll('td'):
                print(i.getText().replace(' ', '').upper())
                qtditem += 1
                print(f'A Quantidade de Itens é:  {qtditem}')

            cont = 0
            for i in soup2.find('table', {'class': 'horizontal-table'}).findAll('td'):
                print(i.getText().replace(' ', '').upper())
                cont += 1

                # CAPTURA NOME DE LOJA

                if cont in range(1, qtditem, 11):
                    shopname.append(i.getText().replace('\n', '').upper())

                # CAPTURA NOME DO VENDEDOR

                if cont in range(2, qtditem, 11):
                    tempvendorname = i.getText().replace('\n', '').upper()
                    tempvendorname = tempvendorname.rstrip()
                    tempvendorname = tempvendorname.lstrip()
                    vendorname.append(tempvendorname)

                # CAPTURA LOCALIZAÇÃO

                if cont in range(3, qtditem, 11):
                    temposition = i.getText().replace('\n', '').upper()
                    temposition = temposition.rstrip()
                    temposition = temposition.lstrip()
                    position.append(temposition)

                # CAPTURA NOME DO ITEM

                if cont in range(4, qtditem, 11):
                    itemname.append(i.getText().replace('\n', '').upper())

                # CAPTURA CARTA 0

                if cont in range(5, qtditem, 11):
                    card0.append(i.getText().replace('\n', '').upper())

                # CAPTURA CARTA 1

                if cont in range(6, qtditem, 11):
                    card1.append(i.getText().replace('\n', '').upper())

                # CAPTURA CARTA 2

                if cont in range(7, qtditem, 11):
                    card2.append(i.getText().replace('\n', '').upper())

                # CAPTURA CARTA 3

                if cont in range(8, qtditem, 11):
                    card3.append(i.getText().replace('\n', '').upper())

                # CAPTURA OPTION

                if cont in range(9, qtditem, 11):
                    options.append(i.getText().replace('\n', '').upper())

                # CAPTURA PREÇO

                if cont in range(10, qtditem, 11):
                    temprice = i.getText().replace('\n', '').upper()
                    temprice = temprice.lstrip()
                    temprice = temprice.rstrip()
                    price.append(temprice)

                # CAPTURA TOTAL

                if cont in range(11, qtditem + 1, 11):
                    tempamount = i.getText().replace('\n', '').upper()
                    tempamount = tempamount.replace(' ', '')
                    amount.append(tempamount)

                else:
                    print(f'fodeo mano olha isso: {i.getText()}')


        listao['SHOPNAME'] = shopname
        listao['VENDORNAME'] = vendorname
        listao['POSITION'] = position
        listao['ITEMNAME'] = itemname
        listao['CARD0'] = card0
        listao['CARD1'] = card1
        listao['CARD2'] = card2
        listao['CARD3'] = card3
        listao['OPTIONS'] = options
        listao['PRICE'] = price
        listao['AMOUNT'] = amount

        global dt

        dt = pd.DataFrame(listao)

        await message.channel.send(f'Olá!, No momento existem {pgn} paginas de lojas')
        sleep(1)
        await message.channel.send('-=' * 20)
        sleep(0.5)
        await message.channel.send(f'totalizando {dt.shape[0]} itens a venda')
        sleep(1)
        await message.channel.send('-=' * 20)
        sleep(0.5)



    if message.content.lower().startswith('#'):
        msg = message.content.upper().replace('#', '')
        print(f' Mensagem: {msg}')
        print(dt[dt['ITEMNAME'].str.contains(msg)])
        testedt = dt[dt['ITEMNAME'].str.contains(msg)]
        testedt = testedt.sort_values('PRICE', ascending=True)
        pd.set_option('display.max_columns', None)

        await message.channel.send(f"```{testedt}```")


    if message.content.lower().startswith('!botfilpz'):
        await message.channel.send('```Olá!, use !lojas para atualizar base de lojas, '
                                   'Use #NOME DO ITEM para pesquisar determinado item!```')


client.run(token)