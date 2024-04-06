from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(chrome_options = chrome_options)

#def

def get_who_takes(id):
    try:
        curr_url = f'https://clientsapi01w.bk6bba-resources.com/service-tv/mobile/mc?app_name=mobile_site&eventId={id}&lang=ru&sysId=22&page=field&scopeMarket=1600'
        driver.get(curr_url)
        soup = BeautifulSoup(driver.page_source)
        centers = soup.find_all("div",{"class":"center"})
        ind = 0
        while(len(centers) == 0 and ind < 10):
            ind += 1
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source)
        centers = soup.find_all("div",{"class":"center"})
        if(ind >= 10):
            return ''
        text = centers[0].find_all("div",{"class":"field__animation-transformer"})[1].text
        driver.switch_to.default_content();
        text = text.strip().replace('\n',' ').replace('\t',' ').split('МЕДИЦИНСКИЙ ТАЙМАУТ')[1].strip()
        return 'Взял(а): ' + text
    except:
        return ''
#code

# token from BotFather
TOKEN = <telegram bot token> 

# chat id
chat_id = <chat id> # add your bot to chat

# patterns
target = ['едицинский перерыв','ед. перерыв','edical timeout','ed. timeout']

# url
url = 'https://line55w.bk6bba-resources.com/events/list?lang=ru&scopeMarket=1600'

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

df_pairs_hist = pd.DataFrame([], columns=['tournament','teams','comment','id','sportId'])
messageId_dict = {}
while(True):
    try:
        json_res = json.loads((requests.get(url, headers=headers, timeout=5).content.decode('utf-8')).partition("customFactors")[0][:-2]+'}')
        MedTimeout_list = []
        for el in json_res['eventMiscs']:
            if('comment' in el):
                #if('медицинский перерыв' in el['comment']):
                if(any([med_el in el['comment'] for med_el in target])):
                    for el_id in json_res['events']:
                        if(el['id'] == el_id['id']):
                            MedTimeout_list.append([el['id'],el_id['sportId']])
        main_list = []
        for el_event in MedTimeout_list:
            event_list = []
            for el in json_res['sports']:
                if(el['id'] == el_event[1]):
                    event_list.append(el['name'])
            for el in json_res['events']:
                if(el['id'] == el_event[0]):
                    event_list.append(el['team1'] + ' — ' + el['team2'])
            for el in json_res['eventMiscs']:
                if(el['id'] == el_event[0]):
                    event_list.append(el['comment'])
            main_list.append(event_list+el_event)
        df_pairs = pd.DataFrame(main_list,columns=['tournament','teams','comment','id','sportId'])
        df_pairs = df_pairs[['tournament','teams','comment','sportId','id']]
        prev_pairs = df_pairs_hist[~df_pairs_hist['teams'].isin(df_pairs['teams'])]
        new_pairs = df_pairs[~df_pairs['teams'].isin(df_pairs_hist['teams'])]
        df_pairs_hist = df_pairs.copy()
        for i in range(len(new_pairs)):
            message = new_pairs.iloc[i].values[0]+'\n'+new_pairs.iloc[i].values[1]+'\n'+new_pairs.iloc[i].values[2]+' начался\nnew.fon.bet/live/tennis/'+str(new_pairs.iloc[i].values[3]) +'/'+str(new_pairs.iloc[i].values[4])
            who_takes_med = get_who_takes(new_pairs.iloc[i].values[4])
            message += '\n'+ who_takes_med
            messageTBot = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
            response = requests.get(messageTBot).json()
            print(response)
            messageId_dict[new_pairs.iloc[i].values[4]] = response['result']['message_id']
            print(message+'\n')
        for i in range(len(prev_pairs)):
            message = 'медицинский перерыв закончился'
            messageId = messageId_dict.pop(prev_pairs.iloc[i].values[4])
            messageTBot = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}&reply_to_message_id={messageId}"
            requests.get(messageTBot)
            print(message+'\n')
    except:
        print('Runtime error', time.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(5)
    time.sleep(1)