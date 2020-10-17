# eksipy
kutsal bilgi kaynağı için unofficial ve private API, giriş yapabilir; mesaj gönderebilir, entry gönderebilirsiniz. 

![](https://img.shields.io/pypi/pyversions/eksipy?style=flat-square) ![](https://img.shields.io/pypi/v/eksipy?style=flat-square) ![PyPI - License](https://img.shields.io/pypi/l/eksipy?style=flat-square) ![](https://www.codefactor.io/repository/github/quiec/eksipy/badge) ![](https://deepsource.io/gh/Quiec/eksipy.svg/?label=active+issues&show_trend=true) ![DeepSource](https://deepsource.io/gh/Quiec/eksipy.svg/?label=resolved+issues&show_trend=true)

> bu proje mobil(rest) api veya herhangi bir api **kullanmamaktadır**. tamamen bs4 ile web'e istek gönderilmektedir. _projenin temel amacı ekşi sözlükte ne yapabiliyorsanız bu kütüphane yapabilmektedir. v1.0 itibariyle çoğu fonksiyon desteklenmektedir._

> bu kütüphane **python 3.6** ve üstünde çalışmaktadır.
## 📦 Kurulum
[pip](https://pypi.org/) kullanarak kolay bir şekilde kurabilirsiniz:

```sh
pip install eksipy
```

## 🛠 Fonksiyonlar
### Sınıf: `Eksi`
|Fonksiyon|Parametre|Açıklama|Dönen Değer
|--|--|--|--|
|`__init__`|`session=None : Session`|Giriş yaptığınızda dönen Session'u buraya yazabilirsiniz.|`None`|
|`bugun`|`page=1` (Sayfa)|Bugün feed'ini döndürür. Tek sayfada (giriş yapmadıysanız) 50 tane başlık olmalıdır|`Liste[Topic]`|
|`gundem`|`page=1` (Sayfa)|Gündem feed'ini döndürür. Tek sayfada (giriş yapmadıysanız) 50 tane başlık olmalıdır|`Liste[Topic]`|
|`autocomplete`|`aranacak kelime`|Ekşi sözlük arama, autocomplete. |`JSON`|

### Sınıf: `Kullanici`
|Fonksiyon|Parametre|Açıklama|Dönen Değer
|--|--|--|--|
|`__init__`|`save_cookies=True`|True yazarsanız sonraki kullanımlarda giriş yapmak yerine cookies kaydeder|`None`|
|`login`|`email: str`, `password: str`|Eposta ve şifre ile giriş yapar|`User`|
|`send_entry`|`baslik: Topic`, `entry: str`|Entry gönderir, Başlık `Topic` modeli olmalıdır. |`Entry (modeli)`|
|`fav_entry`|`entry: int, Entry`|Entry favoriler, başarılı olursa son favori sayısını döndürür|`int`|
|`unfav_entry`|`entry: int, Entry`|Entry favori geri çeker, başarılı olursa son favori sayısını döndürür|`int`|
|`delete_entry`|`entry: int, Entry`|Entry siler, başarılı olursa True döner. |`boolean`|
|`get_messages`|`page: int`, `archive=False : boolean` |Mesaj kutunuzu Liste halinde döndürür. Arşivi almak isterseniz ikinci parametreyi True yapabilirsiniz. |`List[Message]`|
|`get_history`|`message: int, Message`|Kullanıcıyla yaptığınız mesajlaşmanın geçmişini getirir.|`List[MessageHistory]`|
|`delete_message`|`thread_id: int, Message`|Kullanıcıyla yaptığınız mesajlaşmanızı siler.|`Boolean`|
|`archive_message`|`thread_id: int, Message`|Kullanıcıyla yaptığınız mesajlaşmanızı arşivler.|`Boolean`|
|`search_message`|`keyword: str`, `page: int`|Mesajlaşma arar.|`List[Message]`|
|`send_message`|`user: User, str`, `message: str`|Belirttiğiniz kişiye mesaj gönderir.|`Boolean`|
|`upvote`|`entry: Entry`|Entry Upvote'lar.|`Boolean`|
|`downvote`|`entry: Entry`|Entry Downvote'lar.|`Boolean`|
|`get_user`|`user: str`|Kullanıcı getirir.|`User`|
|`get_user_entrys`|`user: str, User`, `page: int`|Kullanıcının entrylerini getirir.|`List[Entry]`|
|`logout`||Çıkış yapar.|`None`|

### Sınıf: `Baslik`
|Fonksiyon|Parametre|Açıklama|Dönen Değer
|--|--|--|--|
|`__init__`|`baslik: str`, `page: int`, `session: Session`|Başlığın sayfasını getirir.|`None`|
|`get_topic`||`Topic` olarak başlığı döndürür.|`Topic`|
|`get_entrys`|`a = None : str`|Entryleri getirir. `a` parametresi `popular` gibi a değişkenleri olabilir ya da boş bırakabilirsiniz. |`List[Entry]`|
|`autocomplete`|`aranacak kelime`|Ekşi sözlük arama, autocomplete. |`JSON`|

### Sınıf: `Giri`
|Fonksiyon|Parametre|Açıklama|Dönen Değer
|--|--|--|--|
|`__init__`|`entry: int`, `session: Session`|Entry sayfasını getirir.|`None`|
|`get_entry`||`Entry` olarak entryi döndürür.|`Entry`|

## 🛠 Modeller
### Sınıf: `Message`
|Değişken|Açıklama|
|--|--|
|`id`|Mesajlaşma numarası|
|`from_user`|Mesajı gönderen kişinin nick'i|
|`message`|Mesaj sayısı|
|`preview`|En son gönderilen mesaj|
|`date`|En son mesaj atılma zamanı|
|`read`|Mesajı okuduysanız True döndürür|
|`unread`|Mesajı okumadıysanız True döndürür|
|`thread_id`|Mesajı silmek veya arşivlemek için gerekli olan değişken|

### Sınıf: `MessageHistory`
|Değişken|Açıklama|
|--|--|
|`incoming`|Mesaj size geldiyse True döner|
|`outcoming`|Mesajı siz attıysanız True döner|
|`message`|Mesaj|
|`date`|Mesajın tarihi|

### Sınıf: `Topic`
|Değişken|Açıklama|
|--|--|
|`id`|Başlık numarası|
|`title`|Başlık|
|`giri`|Entry sayısı|
|`current_page`|Şu anki sayfanız|
|`max_page`|Maksimum sayfa|

|Fonksiyon|Açıklama|
|--|--|
|`url`|Başlığın adresini döndürür|
|`slug`|Başlığın slug halini döndürür|

### Sınıf: `Entry`
|Değişken|Açıklama|
|--|--|
|`id`|Entry numarası|
|`author`|Entry yazarı|
|`date`|Entry gönderilme tarihi (Unix)|
|`edited`|Düzenlendiyse Unix olarak düzenlenme zamanı döndürür|
|`fav`|Favori sayısını döndürür|
|`author_id`|Yazarın numarasını döndürür|
|`comment`|Yorum sayısını döndürür|
|`topic`|Başlığı döndürür|
|`entry`|Entry'i döndürür _(bununla almayın)_|

|Fonksiyon|Açıklama|
|--|--|
|`dict`|Entry'i dict olarak döndürür|
|`url`|Entry adresini döndürür|
|`text`|Entry yazı olarak döndürür|
|`md`|Markdown olarak entryi döndürür **(Önerilen)**|
|`html`|HTML olarak entryi döndürür|

### Sınıf: `User`
|Değişken|Açıklama|
|--|--|
|`id`|Kullanıcı numarası|
|`nick`|Kullanıcı adı|
|`total_entry`|Toplam entry sayısı|
|`last_month`|Geçen ay gönderdiği entry|
|`last_week`|Geçen hafta gönderdiği entry|
|`today`|Bugün gönderdiği entry|
|`last_entry`|En son entry gönderdiği zaman|
|`pinned_entry`|Başa tutturulan Entry.|
|`badges`|Profil rozetleri|

|Fonksiyon|Açıklama|
|--|--|
|`url`|Kullanıcının adresini döndürür|

## 🔷 Örnek Kullanımlar
Burdaki dosyada örnek kullanımları anlatmaya çalıştım.
> Ayrıca hemen birkaç örnek verelim.

**Başlık entrylerini getirelim:**
```python
import eksipy

# Başlığı getirelim
Entryler = eksipy.Baslik('php').get_entrys()
print(f'{Entryler[0].topic.title}\n')
for entry in Entryler:
    print(10 * '*')
    print(entry.text())
    print('Yazar: ' + entry.author)
```

**Giriş yapıp entry gönderelim:**
```python
import eksipy

User = eksipy.Kullanici()
User.login('eposta', 'sifre)
User.send_entry(eksipy.Baslik('php').get_topic(), 'dunyanin en iyi programlama dili')
```

## ☑️ To-Do
- [ ] Kendi Exception sınıflarımız.
- [ ] Olay.
- [ ] Daha iyi bir dokümantasyon (Bence şu anki gayet ii).
- [ ] Tüm kullanıcı istatistikleri, görseller, sorunsallar...
- [ ] Zengin bir CLI uygulaması

## 💻 Contributors
Developer [Quiec](https://t.me/fusuf), yusuf@quiec.tech

Idea [SelaxG](https://t.me/SelaxG),
## 📒 License
eksipy is available under the GPLv3 license. See the LICENSE file for more info.
