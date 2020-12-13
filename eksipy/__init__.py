# Unofficial Ekşi Sözlük private API.

# Copyright (C) 2020 Yusuf Usta
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List
from requests import Session, utils
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from datetime import datetime
from time import mktime
import os
import http
from eksipy.models import *

EKSI_URL = "https://eksisozluk.com/"
USER_AGENT = UserAgent().random

class Eksi:
    def __init__(self, session: Session = None):
        if session == None:
            self.session = Session()
        else:
            if type(session) == Session:
                self.session = session
            else:
                self.session = Session()

    def bugun(self, page = 1):
        bugun = self.session.get(
            EKSI_URL + f'basliklar/bugun/{page}&_=0',
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            }
        )
        
        soup = BeautifulSoup(
            bugun.text, 'lxml'
        )

        topics = soup.find('ul', {'class': 'topic-list'}).find_all('li')
        basliklar = []

        for topic in topics:
            topic_id = topic.find('a')
            if not topic_id == None:
                if topic_id.find('small'):
                    giri_sayi = topic_id.find('small').text.strip()
                    topic_id.find('small').decompose()
                else:
                    giri_sayi = None
                baslik = topic_id.text[:-1]
                topic_id = int(topic_id['href'].split('?day=')[0].split('--')[1])
            else:
                continue

            basliklar.append(
                Topic(
                    id = topic_id,
                    title = baslik,
                    giri = giri_sayi
                )
            )
        return basliklar

    def gundem (self, page = 1):
        gundem = self.session.get(
            EKSI_URL + f'basliklar/gundem?p={page}&_=0',
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            }
        )

        soup = BeautifulSoup(
            gundem.text, 'lxml'
        )

        topics = soup.find('ul', {'class': 'topic-list'}).find_all('li')
        basliklar = []

        for topic in topics:
            topic_id = topic.find('a')
            if not topic_id == None:
                giri_sayi = topic_id.find('small').text.strip()
                topic_id.find('small').decompose()
                baslik = topic_id.text[:-1]
                topic_id = int(topic_id['href'][1:][:-10].split('--')[1])
            else:
                continue
            

            basliklar.append(
                Topic(
                    id = topic_id,
                    title = baslik,
                    giri = giri_sayi
                )
            )
        return basliklar

    def autocomplete(self, text):
        istek = self.session.get(
            EKSI_URL + f'autocomplete/query?q={text}&_=0',
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            }
        )
        return istek.json()

class Kullanici:
    def __init__(self, save_cookies=True):
        self.save_cookies = save_cookies
        self.session = Session()
            
    def login(self, user, sifre):
        if self.save_cookies:
            if not os.path.exists('./cookies'):
                os.makedirs('cookies')

            self.session.cookies = http.cookiejar.LWPCookieJar(filename=f'./cookies/{user}.txt')
            if os.path.exists(f'./cookies/{user}.txt'):
                self.session.cookies.load()

            if 'a' in utils.dict_from_cookiejar(self.session.cookies):
                homepage = self.session.get(
                    EKSI_URL,
                    headers={
                        'User-Agent': USER_AGENT
                    }
                )
        
                homepage = BeautifulSoup(
                    homepage.text, 'lxml'
                )

                nick = homepage.find('li', {'class': 'not-mobile'}).find('a')['title']
                return self.get_user(nick)

        self.kullanici = user
        self.sifre = sifre

        loginpage = self.session.get(
            EKSI_URL + 'giris',
            headers={
                'User-Agent': USER_AGENT
            }
        )
        
        loginsoup = BeautifulSoup(
            loginpage.text, 'lxml'
        )
        ReqVerTok = loginsoup.find('input', {'name': '__RequestVerificationToken'})['value']
        
        sayfa = self.session.post(
            EKSI_URL + 'giris',
            headers={
                'User-Agent': USER_AGENT
            },
            data = {
                'UserName': self.kullanici,
                'Password': self.sifre,
                '__RequestVerificationToken': ReqVerTok,
                'ReturnUrl': 'https://eksisozluk.com/',
                'RememberMe': 'true'
            }
        )

        kukis = utils.dict_from_cookiejar(self.session.cookies) if self.save_cookies else utils.dict_from_cookiejar(self.session.cookies)
        if 'a' in kukis:
            if self.save_cookies:
                self.session.cookies.save()
            homepage = self.session.get(
                    EKSI_URL,
                    headers={
                        'User-Agent': USER_AGENT
                    }
                )
        
            homepage = BeautifulSoup(
                    homepage.text, 'lxml'
                )


            nick = homepage.find('li', {'class': 'not-mobile'}).find('a')['title']
            return self.get_user(nick)
        else:
            raise Exception(f"{sayfa.status_code}: giriş başarısız.")
    
    def send_entry(self, baslik : Topic, entry : str, gizli = False):
        loginpage = self.session.get(
            EKSI_URL + baslik.title + '--' + baslik.id,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        
        loginsoup = BeautifulSoup(
            loginpage.text, 'lxml'
        )

        ReqVerTok = loginsoup.find('input', {'name': '__RequestVerificationToken'})['value']
        Title = loginsoup.find('input', {'name': 'Title'})['value']
        Id = loginsoup.find('input', {'name': 'Id', 'type': 'hidden'})['value']
        InputStartTime = loginsoup.find('input', {'name': 'InputStartTime', 'type': 'hidden'})['value']

        istek = self.session.post(
            EKSI_URL + "entry/ekle",
            headers={
                'User-Agent': USER_AGENT
            },
            data = {
                'Title': Title,
                'Id': Id,
                '__RequestVerificationToken': ReqVerTok,
                'ReturnUrl': '',
                'Content': entry,
                'InputStartTime': InputStartTime
            },
            allow_redirects = False
        )

        if istek.status_code == 302:
            entry = istek.headers['Location'].split('/')[2]
            return Giri(entry).get_entry()
        else:
            raise Exception(f"{istek.status_code}: bir hata oluştu.")
    
    def fav_entry (self, entry):
        anaistek = self.session.post(
            EKSI_URL + "entry/favla",
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            },
            data = {
                'entryId': entry.id if type(entry) == Entry else entry
            },
            allow_redirects = False
        )

        istek = anaistek.json()
        if istek['Success'] == True:
            return istek['Count']
        else:
            raise Exception(f'{anaistek.status_code}: {istek["ErrorMessage"]}')

    def unfav_entry (self, entry):
        anaistek = self.session.post(
            EKSI_URL + "entry/favlama",
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            },
            data = {
                'entryId': entry.id if type(entry) == Entry else entry
            },
            allow_redirects = False
        )

        istek = anaistek.json()
        if istek['Success'] == True:
            return istek['Count']
        else:
            raise Exception(f'{anaistek.status_code}: {istek["ErrorMessage"]}')

    def delete_entry (self, entry):
        istek = self.session.post(
            EKSI_URL + "entry/sil",
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            },
            data = {
                'id': entry.id if type(entry) == Entry else entry
            },
            allow_redirects = False
        )

        if istek.status_code == 200:
            return True
        else:
            raise Exception(f'{istek.status_code}: kesinlikle bir şeyler oldu.')
        
    def get_messages (self, page = 1, archive = False):
        istek = self.session.get(
            EKSI_URL + (f"mesaj?p={page}" if not archive else f"mesaj/arsiv?p={page}"),
            headers={
                'User-Agent': USER_AGENT
            },
            allow_redirects = False
        )

        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        sec = soup.find('div', {'id': 'content'}).find('section').find('form')
        token = sec.find('input', {'name': '__RequestVerificationToken'})['value']
        sec = sec.find('ul', {'id': 'threads'})
        messages = sec.find_all('li')
        mesajlar = []

        for message in messages:
            article = message.find('article')
            threadid = article.find('input', {'name': 'threadId'})['value']
            a = article.find('a')
            mid = a['href'].split('/')[2]
            count = int(a.find('h2').find('small').text.strip())
            a.find('h2').find('small').decompose()
            user = a.find('h2').text.strip()
            msgpre = a.find('p').text.strip()
            zaman = article.find('time')['title']

            mesajlar.append(Message(
                id = mid,
                from_user=user,
                message=count,
                preview=msgpre,
                unread = True if article.has_attr('class') else False,
                read = False if article.has_attr('class') else True,
                date = mktime(datetime.strptime(zaman, "%d.%m.%Y %H:%M" if ':' in zaman else "%d.%m.%Y").timetuple()),
                thread_id=threadid
            ))
        return mesajlar

    def get_history(self, message):
        istek = self.session.get(
            EKSI_URL + "mesaj/" + message.id if type(message) == Message else message,
            headers={
                'User-Agent': USER_AGENT
            },
            allow_redirects = False
        )

        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        messages = soup.find('div', {'id': 'message-thread'}).find_all('article')
        mesajlar = []
        for message in messages:
            msg = message.find('p').text
            zaman = message.find('footer').find('time').text
            mesajlar.append(
                MessageHistory(
                    message=msg,
                    incoming=True if message['class'] == 'incoming' else False,
                    outcoming=False if message['class'] == 'incoming' else True,
                    date=mktime(datetime.strptime(zaman, "%d.%m.%Y %H:%M" if ':' in zaman else "%d.%m.%Y").timetuple())
                )
            )
        return mesajlar

    def delete_message(self, message):
        istek = self.session.get(
            EKSI_URL + f"mesaj?p=1",
            headers={
                'User-Agent': USER_AGENT
            },
            allow_redirects = False
        )

        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        sec = soup.find('div', {'id': 'content'}).find('section').find('form')
        token = sec.find('input', {'name': '__RequestVerificationToken'})['value']
        sil = self.session.post(
            EKSI_URL + "mesaj/processthread",
            headers={
                'User-Agent': USER_AGENT
            },
            data = {
                '__RequestVerificationToken': token,
                'threadId': message.thread_id if type(message) == Message else message,
                'p': '',
                'action': 'delete'
            },
            allow_redirects = False
        )

        if sil.status_code == 302:
            return True
        else:
            raise Exception(f'{sil.status_code}: silemedik abi.')

    def archive_message(self, message):
        istek = self.session.get(
            EKSI_URL + f"mesaj?p=1",
            headers={
                'User-Agent': USER_AGENT
            },
            allow_redirects = False
        )

        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        sec = soup.find('div', {'id': 'content'}).find('section').find('form')
        token = sec.find('input', {'name': '__RequestVerificationToken'})['value']
        sil = self.session.post(
            EKSI_URL + "mesaj/processthread",
            headers={
                'User-Agent': USER_AGENT,
            },
            data = {
                '__RequestVerificationToken': token,
                'threadId': message.thread_id if type(message) == Message else message,
                'p': '',
                'action': 'archive'
            },
            allow_redirects = False
        )

        if sil.status_code == 302:
            return True
        else:
            raise Exception(f'{sil.status_code}: silemedik abi.')
    
    def search_message (self, keyword, page = 1):
        istek = self.session.get(
            EKSI_URL + f"mesaj/ara?keywords={keyword}&p={page}",
            headers={
                'User-Agent': USER_AGENT
            },
            allow_redirects = False
        )

        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        sec = soup.find('div', {'id': 'content'}).find('section')
        sec = sec.find('ul', {'id': 'threads'})
        messages = sec.find_all('li')
        mesajlar = []

        for message in messages:
            article = message.find('article')
            threadid = article.find('input', {'name': 'threadId'})['value']
            a = article.find('a')
            mid = a['href'].split('/')[2]
            count = int(a.find('h2').find('small').text.strip())
            a.find('h2').find('small').decompose()
            user = a.find('h2').text.strip()
            msgpre = a.find('p').text.strip()
            zaman = article.find('time')['title']

            mesajlar.append(Message(
                id = mid,
                from_user=user,
                message=count,
                preview=msgpre,
                unread = True if article.has_attr('class') else False,
                read = False if article.has_attr('class') else True,
                date = mktime(datetime.strptime(zaman, "%d.%m.%Y %H:%M" if ':' in zaman else "%d.%m.%Y").timetuple()),
                thread_id=threadid
            ))
        return mesajlar

    def send_message (self, user, message):
        istek = self.session.get(
            EKSI_URL + f"mesaj?p=1",
            headers={
                'User-Agent': USER_AGENT
            },
            allow_redirects = False
        )

        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        sec = soup.find('div', {'id': 'content'}).find('section').find('form')
        token = sec.find('input', {'name': '__RequestVerificationToken'})['value']

        istek = self.session.post(
            EKSI_URL + f"mesaj/yolla",
            headers={
                'User-Agent': USER_AGENT
            },
            data={
                'To': user.nick if type(user) == User else user ,
                'Message': message,
                '__RequestVerificationToken': token
            },
            allow_redirects = False
        )

        if istek.status_code == 302:
            # TODO return Message
            return True
        else:
            raise Exception(f'{istek.status_code}: gönderemedik abi.')

    def upvote (self, entry: Entry):
        istek = self.session.post(
            EKSI_URL + f"entry/vote",
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            },
            data={
                'id': entry.id,
                'rate': 1,
                'owner': entry.author_id
            },
            allow_redirects = False
        )
        istek = istek.json()

        if istek['Success'] == True:
            return True
        else:
            raise Exception(f'{istek.status_code}: {istek["Message"]}')

    def downvote (self, entry: Entry):
        istek = self.session.post(
            EKSI_URL + f"entry/vote",
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            },
            data={
                'id': entry.id,
                'rate': -1,
                'owner': entry.author_id
            },
            allow_redirects = False
        )
        istek = istek.json()

        if istek['Success'] == True:
            return True
        else:
            raise Exception(f'{istek.status_code}: {istek["Message"]}')
    
    def get_user_entrys(self, user, page = 1) -> List:
        user = user.nick if type(user) == User else user
        istek = self.session.get(
            EKSI_URL + f"son-entryleri?nick={user}&p={page}&_=0",
            headers={
                'User-Agent': USER_AGENT,
                'x-requested-with': 'XMLHttpRequest'
            },
            allow_redirects = False
        )
        
        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        if soup.find('input', {'type': 'hidden', 'id': 'no-more-data'}):
            raise Exception('404: bilinmez sayfanın ufkundayım')

        entrys = soup.find('div', {'id': 'topic'}).find_all('div', {'class': 'topic-item'})
        giriler = []
        for entry in entrys:
            title = entry.find('h1')
            baslik = title['data-title']
            baslik_id = title['data-id']

            giri = entry.find('ul', {'id': 'entry-item-list'}).find('li')
            date = giri.find('footer').find('div', {'class': 'info'}).find('a', {'class': 'entry-date permalink'}).text
            if '~' in date:
                parcalama = date.split('~')
                parcalama[0] = parcalama[0].strip()
                parcalama[1] = parcalama[1].strip()

                tarih = round(
                    mktime(datetime.strptime(parcalama[0], "%d.%m.%Y %H:%M" if ':' in parcalama[0] else "%d.%m.%Y").timetuple())  
                )
                
                if '.' in parcalama[1]:
                    duzenleme = round(
                        mktime(datetime.strptime(parcalama[1], "%d.%m.%Y %H:%M" if ':' in parcalama[1] else "%d.%m.%Y").timetuple())  
                    )
                else:
                    duzenleme = round(
                        mktime(datetime.strptime(f"{parcalama[0].split(' ')[0]} {parcalama[1]}", "%d.%m.%Y %H:%M").timetuple())  
                    )
            else:
                duzenleme = None
                tarih = mktime(datetime.strptime(date, "%d.%m.%Y %H:%M" if ':' in date else "%d.%m.%Y").timetuple())

            giriler.append(
                Entry(
                    id = giri['data-id'],
                    author = giri['data-author'],
                    author_id = giri['data-author-id'],
                    fav = giri['data-favorite-count'],
                    comment = giri['data-comment-count'],
                    entry = giri.find('div'),
                    topic = Topic(
                        id = baslik_id,
                        title = baslik
                    ),
                    date = tarih,
                    edited = duzenleme

                )
            )
        return giriler
    
    def get_user(self, user):
        istek = self.session.get(
            EKSI_URL + f"biri/{user}",
            headers={
                'User-Agent': USER_AGENT
            },
            allow_redirects = False
        )
        soup = BeautifulSoup(
            istek.text, 'lxml'
        )

        if istek.status_code == 404:
            raise Exception('404: böyle birisi yok ki.')
        else:
            a = soup.find('a', {'class': 'relation-link'})
            try:
                user_id = a['data-add-url'].split('/')[3].split('?')[0]
            except TypeError:
                user_id = None
            badge = soup.find('ul', {'id': 'user-badges'}).find_all('li')
            if not badge:
                badge = []
            stats = soup.find('ul', {'id': 'user-entry-stats'}).find_all('li')
            pinned = soup.find('blockquote')
            if pinned == None:
                pinned_topic = None
                pinned_entry = None
                pinned_id = None
                pinned_date = None
                duzenleme = None
                tarih = None
                son_entry = None
            else:
                pinned_topic = pinned.find('h2').text.split()
                pinned_entry = pinned.find('p')
                pinned_id = pinned.find('footer').find('a')['href'].split('/')[2]
                pinned_date = pinned.find('footer').find('a').text
                son_entry = stats[4].text.strip()
                if '~' in pinned_date:
                    parcalama = pinned_date.split('~')
                    parcalama[0] = parcalama[0].strip()
                    parcalama[1] = parcalama[1].strip()

                    tarih = round(
                        mktime(datetime.strptime(parcalama[0], "%d.%m.%Y %H:%M" if ':' in parcalama[0] else "%d.%m.%Y").timetuple())  
                    )
                    
                    if '.' in parcalama[1]:
                        duzenleme = round(
                            mktime(datetime.strptime(parcalama[1], "%d.%m.%Y %H:%M" if ':' in parcalama[1] else "%d.%m.%Y").timetuple())  
                        )
                    else:
                        duzenleme = round(
                            mktime(datetime.strptime(f"{parcalama[0].split(' ')[0]} {parcalama[1]}", "%d.%m.%Y %H:%M").timetuple())  
                        )
                else:
                    duzenleme = None
                    tarih = mktime(datetime.strptime(pinned_date, "%d.%m.%Y %H:%M" if ':' in pinned_date else "%d.%m.%Y").timetuple())

            return User(
                id = user_id,
                nick = user,
                total_entry = int(stats[0].text.strip()),
                last_month = int(stats[1].text.strip()),
                last_week = int(stats[2].text.strip()),
                today = int(stats[3].text.strip()),
                last_entry = son_entry,
                badges = [bad.text for bad in badge],
                pinned_entry = Entry(
                    id = pinned_id,
                    entry = pinned_entry,
                    author = user,
                    author_id = user_id,
                    date = tarih,
                    edited = duzenleme,
                    topic = Topic(
                        title = pinned_topic
                    )
                )
            )
    
    def logout(self):
        if os.path.exists('./cookies/eksi.txt'):
            os.remove('./cookies/eksi.txt')
class Baslik:
    def __init__(self, baslik, page = 1, session = None):
        self.baslik_id = 0
        self.baslik = baslik
        self.sayfa = page
        
        if session == None:
                self.session = Session()
        else:
            if type(session) == Session:
                self.session = session
            else:
                self.session = Session()

        sayfa = self.session.get(
            EKSI_URL + '?q=' + utils.quote(self.baslik),
            allow_redirects=False,
            headers={
                'User-Agent': USER_AGENT
            }
        )

        if sayfa.status_code == 404:
            raise Exception("404: böyle bir şey yok.")
        elif sayfa.status_code == 302:
            baslik = sayfa.headers['Location']
            self.baslik_id = baslik.split("--")[1]
            param = {
                'p': self.sayfa
            }
            sayfa = self.session.get(
                EKSI_URL + baslik,
                allow_redirects=False,
                params=param,
                headers={
                    'User-Agent': USER_AGENT
                }
            )

        self.soup = BeautifulSoup(
            sayfa.text, 'lxml'
        )
    
    def get_topic (self):
        div = self.soup.find_all('div', {'class': 'pager'})[0]
        return Topic(id = self.baslik_id, title = self.baslik, current_page=div['data-currentpage'], max_page=div['data-pagecount'])
            
    def get_entrys(self, a = None):
        if not a == None:
            param = {
                'p': self.sayfa
            }

            param['a'] = a
            page = self.session.get(
                self.get_topic().url(),
                allow_redirects=False,
                params=param,
                headers={
                    'User-Agent': USER_AGENT
                }
            )
            self.soup = BeautifulSoup(
                page.text, 'lxml'
            )

        ul = self.soup.select('ul#entry-item-list')
        if not len(ul) >= 1:
            raise Exception('404: muhtemelen böyle bir başlık yok veya erişim izniniz yok. ya da parametre yanlış.')
        ul = ul[0]
        entrys = ul.find_all(
            'li'
        )
        
        liste = []
        for entry in entrys:
            date = entry.find('footer').find('div', {'class': 'info'}).find('a', {'class': 'entry-date permalink'}).text
            if '~' in date:
                parcalama = date.split('~')
                parcalama[0] = parcalama[0].strip()
                parcalama[1] = parcalama[1].strip()

                tarih = round(
                    mktime(datetime.strptime(parcalama[0], "%d.%m.%Y %H:%M" if ':' in parcalama[0] else "%d.%m.%Y").timetuple())  
                )
                
                if '.' in parcalama[1]:
                    duzenleme = round(
                        mktime(datetime.strptime(parcalama[1], "%d.%m.%Y %H:%M" if ':' in parcalama[1] else "%d.%m.%Y").timetuple())  
                    )
                else:
                    duzenleme = round(
                        mktime(datetime.strptime(f"{parcalama[0].split(' ')[0]} {parcalama[1]}", "%d.%m.%Y %H:%M").timetuple())  
                    )
            else:
                duzenleme = None
                tarih = mktime(datetime.strptime(date, "%d.%m.%Y %H:%M" if ':' in date else "%d.%m.%Y").timetuple())

            div = self.soup.find_all('div', {'class': 'pager'})[0]
            liste.append(
                Entry(
                    id = entry['data-id'], 
                    author = entry['data-author'], 
                    author_id = entry['data-author-id'],
                    fav = entry['data-favorite-count'],
                    comment = entry['data-comment-count'],
                    entry = entry.find_all('div')[0],
                    date = tarih,
                    edited = duzenleme,
                    topic = Topic(
                        id = self.baslik_id,
                        title = self.baslik,
                        current_page=div['data-currentpage'],
                        max_page=div['data-pagecount']
                    )
                )
            )
        return liste

class Giri:
    def __init__(self, entry_id, session = None):
        self.entry_id = entry_id
        if session == None:
            self.session = Session()
        else:
            if type(session) == Session:
                self.session = session
            else:
                self.session = Session()

    def get_entry(self):
        sayfa = self.session.get(
            EKSI_URL + 'entry/' + str(self.entry_id),
            allow_redirects=False,
            headers={
                'User-Agent': USER_AGENT
            }
        )

        if sayfa.status_code == 200:
            self.soup = BeautifulSoup(
                sayfa.text, 'lxml'
            )

            ul = self.soup.select('ul#entry-item-list')[0]
            entry = ul.find_all(
                'li'
            )[0]
        
            date = entry.find('footer').find('div', {'class': 'info'}).find('a', {'class': 'entry-date permalink'}).text
            if '~' in date:
                parcalama = date.split('~')
                parcalama[0] = parcalama[0].strip()
                parcalama[1] = parcalama[1].strip()

                tarih = round(
                    mktime(datetime.strptime(parcalama[0], "%d.%m.%Y %H:%M" if ':' in parcalama[0] else "%d.%m.%Y").timetuple())  
                )
                
                if '.' in parcalama[1]:
                    duzenleme = round(
                        mktime(datetime.strptime(parcalama[1], "%d.%m.%Y %H:%M" if ':' in parcalama[1] else "%d.%m.%Y").timetuple())  
                    )
                else:
                    duzenleme = round(
                        mktime(datetime.strptime(f"{parcalama[0].split(' ')[0]} {parcalama[1]}", "%d.%m.%Y %H:%M").timetuple())  
                    )
            else:
                duzenleme = None
                tarih = mktime(datetime.strptime(date, "%d.%m.%Y %H:%M" if ':' in date else "%d.%m.%Y").timetuple())
            baslik = self.soup.find('h1', {'id': 'title'})

            return Entry(
                id = entry['data-id'], 
                author = entry['data-author'], 
                author_id = entry['data-author-id'],
                fav = entry['data-favorite-count'],
                comment = entry['data-comment-count'],
                entry = entry.find_all('div')[0],
                date = tarih,
                edited = duzenleme,
                topic = Topic(
                    id = baslik['data-id'],
                    title = baslik['data-title']
                )
            )
        else:
            raise Exception(f"{sayfa.status_code}: kesinlikle bir şeyler oldu.")
