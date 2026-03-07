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
        "🌙 Saharlik va Iftorlik vaqti\n"
        "📿 Saharlik va Iftorlik duolari\n"
        "🤲 Namoz duolari\n"
        "Bot 24/7 ishlaydi va qo'shimcha ma'lumot kerak bo'lsa @reall_javohir ga murojaat qilishingiz mumkin."
    )
    await message.answer(text)

# ================== NAMOZ ==================
@dp.message(lambda m: m.text=="🕌 Namoz vaqtlari")
async def namoz_vaqti(message: types.Message):
    text = (
        f"📍 Xorazm namoz vaqtlari:\n\n"
        f"Bomdod:   06:01\n"
        f"Peshin:      13:10\n"
        f"Asr: 	         16:18\n"
        f"Shom:       18:48\n"
        f"Xufton:     20:15"
    )
    await message.answer(text)

# ================== ROZA ==================
@dp.message(lambda m:m.text=="🌙 Saharlik Iftorlik")
async def roza(message: types.Message):
    text=f"""🗓 Xorazm – 2026 Ramazon saharlik va iftorlik jadvali\n
Ramazon	  Sana	       Saharlik	  Iftorlik
1-kun	        19-fevral   06:23   18:41
2-kun	        20-fevral   06:22   18:43
3-kun	        21-fevral   06:20   18:44
4-kun	        22-fevral   06:19   18:45
5-kun	        23-fevral   06:17   18:47
6-kun	        24-fevral   06:16   18:48
7-kun	        25-fevral   06:14   18:49
8-kun	        26-fevral   06:13   18:51
9-kun	        27-fevral   06:11   18:52
10-kun	       28-fevral   06:09   18:54
11-kun	        1-mart	     06:08   18:55
12-kun	        2-mart	    06:06   18:56
13-kun	        3-mart	    06:05   18:58
14-kun	        4-mart	    06:03   18:59
15-kun	        5-mart	    06:01   19:00
16-kun	        6-mart	    05:59   19:02
17-kun	        7-mart	    05:58   19:03
18-kun	        8-mart	    05:56   19:04
19-kun	        9-mart	    05:54   19:06
20-kun	       10-mart	    05:53   19:07
21-kun	        11-mart	    05:51   19:08
22-kun	        12-mart	    05:49   19:10
23-kun	        13-mart	    05:48   19:11
24-kun	        14-mart	    05:46   19:12
25-kun	        15-mart	    05:44   19:14
26-kun         16-mart	    05:42   19:15
27-kun	        17-mart	    05:41   19:16
28-kun	        18-mart	    05:39   19:18
29-kun	        19-mart	    05:37   19:19
30-kun	        20-mart	    05:35   19:20"""
    await message.answer(text)

# ================== RAMAZON KUN ==================
RAMAZON_START=date(2026,2,19)
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
Saharlik duosi📿
Navaytu an asuma sovma shahri
ramazona minal fajri ilal mag‘ribi,
xolisan lillahi ta’ala. Allohu akbar.
"""
    await message.answer(text)

@dp.message(lambda m:m.text=="📿 Iftorlik duosi")
async def iftor(message: types.Message):
    text="""
Iftorlik duosi📿
Allohumma laka sumtu va bika amantu
va ’alayka tavakkaltu va ’ala rizqika aftartu, fag‘firli ya g‘offaru ma qoddamtu va ma axxortu.
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
