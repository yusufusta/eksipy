import eksipy
import asyncio
import os


async def login():
    eksi = eksipy.Eksi()
    await eksi.login("eposta", "şifre")
    location = eksi.saveSession()
    return location


async def main():
    eksi = eksipy.Eksi()

    if os.path.exists("sessions") and len(os.listdir("sessions")) == 1:
        eksi.loadSession(os.path.join("sessions", os.listdir("sessions")[0]))
        if (await eksi.isLogged()):
            bugun = (await eksi.bugun())[0]
            entry = await bugun.sendEntry("bugün feedindeki ilk başlık.")
            await entry.fav()
            print("Entry Gönderildi! " + entry.url())
            # await entry.delete()
            #print("Entry silindi!")
        else:
            await login()
    else:
        await login()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
