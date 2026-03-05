import asyncio
import requests
import aiosqlite
from datetime import date
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = "8383539672:AAHrMHQobXR8LptpiLpdD5kDwPsUxV2rQIU"  # Tokeningizni bu yerga qo'ying
ADMIN_ID = 6713905538  # sizning telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== DATABASE ==================
async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            region TEXT
        )
        """)
        await db.commit()

async def add_user(user_id):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)",(user_id,))
        await db.commit()

async def set_region(user_id, region):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("UPDATE users SET region=? WHERE user_id=?",(region,user_id))
        await db.commit()

async def get_region(user_id):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT region FROM users WHERE user_id=?",(user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "Toshkent"

async def get_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            return [row[0] async for row in cursor]

# ================== MENUS ==================
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🕌 Namoz vaqtlari")],
        [KeyboardButton(text="🔢 Ramazon kun sanog‘i")],
        [KeyboardButton(text="🌙 Saharlik Iftorlik")],
        [KeyboardButton(text="📿 Saharlik duosi"), KeyboardButton(text="📿 Iftorlik duosi")],
        [KeyboardButton(text="🤲 Namoz duolari")],
        [KeyboardButton(text="ℹ️ Bot haqida")]
    ],
    resize_keyboard=True
)

# ================== API ==================
def get_times(region):
    url=f"https://islomapi.uz/api/present/day?region={region}"
    data=requests.get(url).json()
    return data["times"]

def get_prayer_times(city):
    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country=Uzbekistan&method=2"
    response = requests.get(url).json()
    timings = response["data"]["timings"]
    return timings

# ================== START ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer(
        "Assalomu alaykum🙂\nBizning botga hush kelibsiz!\nQuyidagi tugmalardan tanlang:", 
        reply_markup=menu
    )

# ================== BOT HAQIDA ==================
@dp.message(lambda m: m.text=="ℹ️ Bot haqida")
async def bot_haqida(message: types.Message):
    text = (
        "Assalomu alaykum! 🤖\n\n"
        "Ushbu bot sizga quyidagilarni taqdim etadi:\n"
        "🕌 Namoz vaqtlari\n"
        "🔢 Ramazon kun sanog‘i\n"
        "📿 Saharlik va Iftorlik duolari\n"
        "🤲 Namoz duolari\n"
        "Bot 24/7 ishlaydi va qo'shimcha ma'lumot kerak bo'lsa @reall_javohir ga murojaat qilishingiz mumkin."
    )
    await message.answer(text)

# ================== NAMOZ ==================
@dp.message(lambda m: m.text=="🕌 Namoz vaqtlari")
async def namoz_vaqti(message: types.Message):
    city = await get_region(message.from_user.id)
    times = get_prayer_times(city)
    text = (
        f"📍 {city} namoz vaqtlari:\n\n"
        f"Bomdod: {times['Fajr']}\n"
        f"Peshin: {times['Dhuhr']}\n"
        f"Asr: {times['Asr']}\n"
        f"Shom: {times['Maghrib']}\n"
        f"Xufton: {times['Isha']}"
    )
    await message.answer(text)

# ================== ROZA ==================
@dp.message(lambda m:m.text=="🌙 Saharlik Iftorlik")
async def roza(message: types.Message):
    text=f"""🗓 Xorazm – 2026 Ramazon saharlik va iftorlik jadvali\n
№   Kun     Saharlik  Iftorlik
1   18‑fev  \t06:14   18:33
2   19‑fev  \t06:13   18:34
3   20‑fev  \t06:12   18:35
4   21‑fev  \t06:11   18:37
5   22‑fev  \t06:09   18:38
6   23‑fev  \t06:08   18:39
7   24‑fev  \t06:06   18:40
8   25‑fev  \t06:05   18:41
9   26‑fev  \t06:03   18:43
10  27‑fev  \t06:02   18:44
11  28‑fev  \t06:00   18:45
12  1 ‑mart \t05:59   18:46
13  2 ‑mart \t05:57   18:47
14  3 ‑mart \t05:56   18:48
15  4 ‑mart \t05:54   18:50
16  5 ‑mart \t05:53   18:51
17  6 ‑mart \t05:51   18:52
18  7 ‑mart \t05:49   18:53
19  8 ‑mart \t05:48   18:54
20  9 ‑mart \t05:46   18:55
21  10‑mart \t05:45   18:56
22  11‑mart \t05:43   18:58
23  12‑mart \t05:41   18:59
24  13‑mart \t05:39   19:00
25  14‑mart \t05:38   19:01
26  15‑mart \t05:36   19:02
27  16‑mart \t05:34   19:03
28  17‑mart \t05:32   19:04
29  18‑mart \t05:31   19:05
30  19‑mart \t05:29   19:06"""
    await message.answer(text)

# ================== RAMAZON KUN ==================
RAMAZON_START=date(2026,2,18)
@dp.message(lambda m:m.text=="🔢 Ramazon kun sanog‘i")
async def count(message:types.Message):
    today=date.today()
    diff=(today-RAMAZON_START).days+1
    if diff<=0:
        text="Ramazon hali boshlanmadi"
    elif diff>30:
        text="Ramazon tugagan"
    else:
        text=f"Bugun Ramazonning {diff}-kuni"
    await message.answer(text)

# ================== DUO ==================
@dp.message(lambda m:m.text=="📿 Saharlik duosi")
async def sahar(message: types.Message):
    text="""
Saharlik duosi
Allohumma inni laka sumtu
va bika aamantu
va a'layka tavakkaltu
"""
    await message.answer(text)

@dp.message(lambda m:m.text=="📿 Iftorlik duosi")
async def iftor(message: types.Message):
    text="""
Iftorlik duosi
Allohumma laka sumtu
va ala rizqika aftartu
"""
    await message.answer(text)

@dp.message(lambda m:m.text=="🤲 Namoz duolari")
async def duo(message: types.Message):
    text="""
1️⃣ Tahorat
Namozdan oldin tahorat olish shart.

2️⃣ Niyat
Ichki niyat qilinadi, og‘iz bilan ham aytish mumkin:
“Men bugun Bomdod / Peshin / Asr / Shom / Xufton namozini Alloh rizosi uchun o‘qishni niyat qildim.”

3️⃣ Takbir (Iqomat)
Allohu Akbar – qo‘llarni ko‘tarib boshing ustiga qo‘yiladi.

4️⃣ Qiyom (Tanaqo’)
Surah al-Fotiha (har rakatda)
Keyin bir qisqa sura (Ikhlas, Falaq, Nas va boshqalar)

5️⃣ Ruku
Allohu Akbar deb ruku qilinadi
Rukuda uch marta: “Subhana Rabbiyal Azeem”

6️⃣ Qiyamga qaytish
“Sami’Allahu liman hamidah”
Keyin: “Rabbana lakal hamd”

7️⃣ Sajda
Allohu Akbar deb sajda qilinadi
Sajdada uch marta: “Subhana Rabbiyal A‘la”

8️⃣ Jalsa (O‘tirish)
Sajda orasida o‘tirish (bir necha soniya)
Ikkinchi sajda ham xuddi shunday

9️⃣ Ikkinchi rakat
2-rakat ham xuddi 1-rakat kabi
2-rakatdan keyin Tashahhud o‘qiladi:
“At-tahiyatu lillahi… Muhammadun rasulullah…”
Agar 3 yoki 4 rakatli namoz bo‘lsa, o‘rta rakatda qisqa tashahhud, oxirida to‘liq tashahhud

🔟 Salom
O‘ngga va chapga qarab:
“Assalamu ‘alaykum wa rahmatullah”
Namozdan keyingi qisqa duolar:
Istig‘for: Astag‘firulloh (3 marta).
Salom duosi: Allohumma antas-salam va minkas-salam, tabarokta ya zal-jalali val-ikrom.
Robbana duosi: Robbana atina fid-dunya hasanatan va fil-axiroti hasanatan va qina azaban-nar.
Tasbehot: 33 marta Subhanalloh (Alloh pokdir), 33 marta Alhamdulillah (Allohga hamd bo‘lsin), 33 marta Allohu akbar (Alloh buyukdir).
"""
    await message.answer(text)

# ================== ADMIN ==================
@dp.message(Command("admin"))
async def admin(message:types.Message):
    if message.from_user.id!=ADMIN_ID:
        return
    users=await get_users()
    await message.answer(f"Admin panel\n\nFoydalanuvchilar: {len(users)}\n\nXabar yuborish:\n/send text")

@dp.message(Command("send"))
async def send(message:types.Message):
    if message.from_user.id!=ADMIN_ID:
        return
    text=message.text.replace("/send ","")
    users=await get_users()
    for user in users:
        try:
            await bot.send_message(user,text)
        except:
            pass
    await message.answer("Xabar yuborildi")

# ================== MAIN ==================
async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
