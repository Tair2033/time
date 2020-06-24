import requests
import telebot
import time
import random
import schedule
from file_facts import facts
from telebot import types
from datetime import date
from bs4 import BeautifulSoup
from multiprocessing.context import Process

token = '1073333652:AAHTlqSt2qDztOF2I7z0YG5Tda1xVTiQUrY'
bot = telebot.TeleBot(token)
url1='https://coronavirusstat.ru/country/samarskaya_oblast/250028/'
url2='https://www.worldometers.info/coronavirus/'
url3='https://www.samru.ru/spravka/pogoda/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
page1=requests.get(url1, headers)
page2=requests.get(url2, headers)
page3=requests.get(url3, headers)
soup1=BeautifulSoup(page1.content, 'html.parser')
soup2=BeautifulSoup(page2.content, 'html.parser')
soup3=BeautifulSoup(page3.content, 'html.parser')


#новые заболевшие
newinfected=soup1.findAll('span', {'class':'font-weight-bold','class':'text-text-dark' })
#Общее количесво зараженных в Самаре
allpeopleinfected=soup1.findAll('div', {'class':'col col-6 col-md-3 pt-4', 'class':'h2'})
#Всего в мире
allworld=soup2.findAll('div', {'class':'maincounter-number'})
#Температура
temp=soup3.findAll('div', {'style':'float:left;padding:10px;font-size:24px'})
#Дата
date=date.today()

#Ежедневная отправка сообщений
def send_covid_message():
    bot.send_message(-1001403887404 ,str(date) +"\n"+"Заболевших в Самаре за день: " + newinfected[0].text + "\n" + "Всего Заболевших в Самаре: " + allpeopleinfected[0].text + "\n" + "Всего заболевший в мире: " + allworld[0].text + 2*"\n" + "Температура сегодня: " + temp[0].get_text("|", strip=True))
def send_fact_message():
    num=random.randint(0, len(facts))
    bot.send_message(-1001403887404, "Вечерний факт: " + facts[num])
schedule.every().day.at("09:00").do(send_covid_message)
schedule.every().day.at("17:00").do(send_fact_message)
while True:
    schedule.run_pending()
    time.sleep(1)


#запуск
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        print("Error")
