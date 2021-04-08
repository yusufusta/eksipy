# eksipy

kutsal bilgi kaynağı için unofficial ve private ASYNC API, giriş yapabilir; ~~mesaj gönderebilir~~, entry gönderebilirsiniz.

![](https://img.shields.io/pypi/pyversions/eksipy?style=flat-square) ![](https://img.shields.io/pypi/v/eksipy?style=flat-square) ![PyPI - License](https://img.shields.io/pypi/l/eksipy?style=flat-square) ![](https://www.codefactor.io/repository/github/quiec/eksipy/badge) ![](https://deepsource.io/gh/Quiec/eksipy.svg/?label=active+issues&show_trend=true) ![DeepSource](https://deepsource.io/gh/Quiec/eksipy.svg/?label=resolved+issues&show_trend=true) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eksipy)

> bu proje mobil(rest) api veya herhangi bir api **kullanmamaktadır**. tamamen requests ile web'e istek gönderilmektedir. requests-html ile de (PyQuery) ile de parçalanmaktadır. _projenin temel amacı ekşi sözlükte ne yapabiliyorsanız bu kütüphane yapabilmektedir. v2.0 itibariyle çoğu fonksiyon desteklenmektedir._

> bu kütüphane **python 3.6** ve üstünde çalışmaktadır.

## 📦 Kurulum

[pip](https://pypi.org/) kullanarak kolay bir şekilde kurabilirsiniz:

```sh
pip install eksipy
```

## 🛠 Doküman

Dokümanlar `docs` klasöründedir.

## 🔷 Örnek Kullanımlar

[Burdaki klasöre bakabilirsiniz](https://github.com/yusufusta/eksipy/tree/master/examples)

> Ayrıca hemen birkaç örnek verelim.

**Başlık entrylerini getirelim:**

```python
import eksipy
import asyncio
import os


async def getTopic():
    eksi = eksipy.Eksi()
    topic = await eksi.getTopic("php")
    entrys = await topic.getEntrys()
    for entry in entrys:
        print("*" * 10)
        print(entry.text())
        print(entry.author.nick)
        print("*" * 10)

loop = asyncio.get_event_loop()
loop.run_until_complete(getTopic())
```

## ☑️ To-Do

- [ ] Kendi Exception sınıflarımız.
- [ ] Olay.
- [x] Daha iyi bir dokümantasyon.
- [ ] Tüm kullanıcı istatistikleri, görseller, sorunsallar...
- [ ] Zengin bir CLI uygulaması
- [ ] Özel mesaj
- [x] Async
- [ ] Testler
- [ ] Sorunsallar

## 💻 Contributors

Developer [Yusuf Usta](https://t.me/fusuf), yusuf@usta.email

## 📒 License

eksipy is available under the GPLv3 license. See the LICENSE file for more info.
