import eksipy
import os

print('-- ekşicli --')
print('giriş yap')
eposta = input('e-postanız: ')

if not os.path.exists(f'./cookies/{eposta}.txt'):
    sifre = input('şifreniz: ')
else:
    sifre = ''

User = eksipy.Kullanici()
Login = User.login(eposta, sifre)
print(f'{Login.nick} olarak giriş yapıldı!')
os.system('clear')
istek = 0

while not istek == '5':
    print(f"""
kullanıcı: {Login.nick}

ne yapmak istersiniz?
    1-) gündem getir
    2-) entry gönder
    3-) mesaj gönder
    4-) mesaj kutusu

    5-) çık
    """)
    istek = input(':')
    if istek == '1':
        i = 0
        gundem = eksipy.Eksi(session=User.session).gundem()
        for baslik in gundem:
            print('*' * 10)
            print(f'({i}) {baslik.title} ({baslik.giri})')
            i += 1

        baslik = int(input('\nhangi başlığa girmek istersiniz: '))
        if baslik <= 49:
            print(gundem[baslik].title + '\n')

            for entry in eksipy.Baslik(gundem[baslik].title).get_entrys('popular'):
                print('-' * 10)
                print(f"""({entry.id}) {entry.md()} 
({entry.date}) ({entry.author})""")
    elif istek == '2':
        baslik = input('başlık: ')
        entry = input('entry: ')

        Entry = User.send_entry(eksipy.Baslik(baslik).get_topic(), entry)
        print(f'Entry Gönderildi! URL: {Entry.url()}')
    elif istek == '3':
        user = input('kullanıcı: ')
        mesaj = input('mesaj: ')

        Mesaj = User.send_message(user, mesaj)
        if Mesaj:
            print(f'Mesaj Gönderildi!')
    elif istek == '4':
        Box = User.get_messages()
        for Mesaj in Box:
            print('*' * 10)
            print(f"""{Mesaj.from_user} ({Mesaj.message})
{Mesaj.preview}
{Mesaj.date}""")
            print('*' * 10)
