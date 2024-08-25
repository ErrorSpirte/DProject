import discord, os
from discord.ext import commands
import random, requests
from bs4 import BeautifulSoup

print(os.listdir('images'))

# Настройки бота
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Событие при запуске бота
@bot.event
async def on_ready():
    print("Bot is online!")  # Сообщение в консоли
    for guild in bot.guilds:
        for channel in guild.text_channels:
            await channel.send('Bot is online! Use "/commands" to see commands.')

# Факты о глобальном потеплении
climate_facts = [
    "Средняя глобальная температура выросла на 1,1°C c конца 19 века.",
    "Уровень мирового океана повысился на 20 см за последние 100 лет.",
    "Арктический лед тает co скоростью 13% за десятилетие.",
    "Климатические изменения усиливают экстремальные погодные явления.",
    "Океаны поглощают около 30% антропогенного CO2, что приводит к их подкислению.",
    "97% климатологов соглашаются, что глобальное потепление — результат человеческой деятельности.",
    "Изменение климата угрожает биоразнообразию и экосистемам.",
    "Потепление на 2°C может привести к исчезновению 99% коралловых рифов.",
    "B последние 30 лет мы видим наиболее интенсивное потепление.",
    "Парижское соглашение ставит цель удержать глобальное потепление на уровне ниже 2°C."
]

# Функция для получения новостей о климате
def get_climate_news():
    url = "https://www.bbc.com/news/science_and_environment"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')
    news = [headline.get_text() for headline in headlines[:5]]
    return news

# Команда для случайного факта о глобальном потеплении
@bot.command(name='climate_facts')
async def send_climate_facts(ctx):
    fact = random.choice(climate_facts)
    await ctx.send(f"🌍 {fact}")

# Команда для получения последних новостей о климате
@bot.command(name='climate_news')
async def send_climate_news(ctx):
    news = get_climate_news()
    news_message = "\n".join([f"🔗 {headline}" for headline in news])
    await ctx.send(f"📰 Последние новости о климате:\n{news_message}")

# Команда для объяснения глобального потепления
@bot.command(name='what_is_global_warming')
async def what_is_global_warming(ctx):
    await ctx.send(
        "🌡️ Глобальное потепление — это долговременное увеличение средней температуры Земли из-за выбросов парниковых газов. "
        "Эти газы, такие как CO2 и метан, создают парниковый эффект, задерживая тепло в атмосфере."
    )

# Команда для объяснения важности проблемы
@bot.command(name='why_important')
async def why_important(ctx):
    await ctx.send(
        "🔥 Глобальное потепление важно, потому что оно вызывает изменение климата, "
        "которое может привести к экстремальным погодным условиям, поднятию уровня моря, "
        "снижению урожайности и разрушению экосистем."
    )

# Команда для совета по борьбе с проблемой
@bot.command(name='how_to_mitigate')
async def how_to_mitigate(ctx):
    await ctx.send(
        "♻️ Чтобы бороться c глобальным потеплением, вы можете:\n"
        "1. Сократить потребление энергии.\n"
        "2. Перейти на возобновляемые источники энергии.\n"
        "3. Минимизировать использование пластика.\n"
        "4. Поддерживать устойчивые практики.\n"
        "5. Сократить количество выбросов углерода, используя общественный транспорт или велосипеды."
    )

# Команда для задания эко-челленджа
@bot.command(name='eco_challenge')
async def eco_challenge(ctx):
    challenges = [
        "🚶 Пройди 10 000 шагов вместо использования транспорта.",
        "🌳 Посади дерево.",
        "💡 Выключи свет, когда не используешь eгo.",
        "📦 Минимизируй использование пластика на один день.",
        "🚲 Используй велосипед вместо автомобиля сегодня."
    ]
    challenge = random.choice(challenges)
    await ctx.send(f"🌱 Ваш эко-челлендж на сегодня: {challenge}")

# Команда для отслеживания цели
user_goals = {}

@bot.command(name='track_goal')
async def track_goal(ctx, *, goal):
    user_goals[ctx.author.id] = goal
    await ctx.send(f"🎯 Цель установлена: {goal}")

# Команда для показа прогресса пользователя
@bot.command(name='progress')
async def progress(ctx):
    goal = user_goals.get(ctx.author.id, None)
    if goal:
        await ctx.send(f"📈 Ваша текущая цель: {goal}")
    else:
        await ctx.send("❗ У вас нет установленной цели. Используйте /track_goal, чтобы установить её.")

@bot.command(name='commands')
async def send_commands_list(ctx):
    commands_list = """
    📜 Список доступных команд:
    /climate_facts - Отправляет случайный факт o глобальном потеплении.
    /climate_news - Делится последними новостями o климате.
    /what_is_global_warming - Объясняет, что такое глобальное потепление.
    /why_important - Говорит, почему это важно.
    /how_to_mitigate - Дает советы, как бороться c проблемой.
    /eco_challenge - Предлагает простое эко-задание.
    /track_goal - Пользователь устанавливает цель, бот отслеживает её выполнение.
    /progress - Показывает прогресс пользователя.
    /meme - отправляет мемы (пока нету)
    /commands - Показывает список всех команд.
    """
    await ctx.send(commands_list)

# Команда для отправки случайного мема из папки 'images'
@bot.command(name='meme')
async def send_meme(ctx):
    await ctx.send("тут пока нету мемов ☹️")

@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("🛑 Bot is shutting down...")
    await bot.close()

# Запуск бота
bot.run('paste token here')
