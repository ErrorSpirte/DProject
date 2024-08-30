import discord
from discord.ext import commands
import random, requests
from bs4 import BeautifulSoup
from collections import Counter

# Настройки бота
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

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
    "Парижское соглашение ставит цель удержать глобальное потепление на уровне ниже 2°C.",
    "Изменение климата может увеличить частоту сильных штормов и ураганов.",
    "Таяние ледников и льдов Антарктиды угрожает прибрежным регионам.",
    "Повышение температуры приводит к увеличению количества лесных пожаров.",
    "Глобальное потепление способствует распространению болезней, таких как малярия.",
    "Океаны нагреваются быстрее, чем когда-либо за последние 50 лет."]

fact_counter = Counter()

# Получения шуток 1
def get_joke(type='general'):
    url = "https://www.anekdot.ru/last/good/" if type == 'general' else "https://www.anekdot.ru/last/black/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Поиск анекдотов на сайте
        jokes = soup.find_all('div', class_='text')
        if jokes:
            return random.choice(jokes).get_text(strip=True)
        else:
            return "He удалось найти шутки. Возможно, структура сайта изменилась."
    except requests.RequestException as e:
        return f"Ошибка при запросе шутки: {e}"
    except Exception as e:
        return f"Неизвестная ошибка: {e}"

# Получения шуток 2
@bot.command(name='joke')
async def joke(ctx, type='general'):
    joke_text = get_joke(type)
    await ctx.send(joke_text)

# Магический шар
@bot.command(name='magic')
async def magic(ctx, *, question=None):
    if question and len(question) > 2 and question.endswith('?'):
        # Проверка на наличие букв в вопросе
        if any(c.isalpha() for c in question):
            await ctx.send(magic_ball())
        else:
            await ctx.send("Извини уж, но это не вопрос")
    else:
        await ctx.send("Извини уж, но это не вопрос")

# Функция для магического шара
def magic_ball():
    responses = ["Да", "Нет", "Возможно", "He знаю"]
    return random.choice(responses)

# Команда для случайного факта о глобальном потеплении
@bot.command(name='climate_facts')
async def send_climate_facts(ctx):
    if len(fact_counter) == len(climate_facts):
        fact_counter.clear()  # Сброс счетчика после использования всех фактов
    fact = random.choice([f for f in climate_facts if fact_counter[f] < 2])
    fact_counter[fact] += 1
    await ctx.send(f"🌍 {fact}")

# Объяснения глобального потепления
@bot.command(name='what_is_global_warming')
async def what_is_global_warming(ctx):
    await ctx.send(
        "🌡️ Глобальное потепление — это долговременное увеличение средней температуры Земли из-за выбросов парниковых газов. "
        "Эти газы, такие как CO2 и метан, создают парниковый эффект, задерживая тепло в атмосфере.")

# Объяснения важности проблемы
@bot.command(name='why_important')
async def why_important(ctx):
    await ctx.send(
        "🔥 Глобальное потепление важно, потому что оно вызывает изменение климата, "
        "которое может привести к экстремальным погодным условиям, поднятию уровня моря, "
        "снижению урожайности и разрушению экосистем.")

# Советы по борьбе с проблемой
@bot.command(name='how_to_mitigate')
async def how_to_mitigate(ctx):
    await ctx.send(
        "♻️ Чтобы бороться c глобальным потеплением, вы можете:\n"
        "1. Сократить потребление энергии.\n"
        "2. Перейти на возобновляемые источники энергии.\n"
        "3. Минимизировать использование пластика.\n"
        "4. Поддерживать устойчивые практики.\n"
        "5. Сократить количество выбросов углерода, используя общественный транспорт или велосипеды.")

# Задание эко-челленджа
@bot.command(name='eco_challenge')
async def eco_challenge(ctx):
    challenges = [
        "🚶 Пройди 10 000 шагов вместо использования транспорта.",
        "🌳 Посади дерево.",
        "💡 Выключи свет, когда не используешь eгo.",
        "📦 Минимизируй использование пластика на один день.",
        "🚲 Используй велосипед вместо автомобиля сегодня."
        "♻️ Перейди на безотходное потребление на один день.",
        "🛒 Купи продукцию местного производства."
    ]
    challenge = random.choice(challenges)
    await ctx.send(f"🌱 Ваш эко-челлендж на сегодня: {challenge}")

# Отслеживания цели
user_goals = {}

@bot.command(name='track_goal')
async def track_goal(ctx, *, goal):
    user_goals[ctx.author.id] = goal
    await ctx.send(f"🎯 Цель установлена: {goal}")

# Показ прогресса пользователя
@bot.command(name='progress')
async def progress(ctx):
    goal = user_goals.get(ctx.author.id, None)
    if goal:
        await ctx.send(f"📈 Ваша текущая цель: {goal}")
    else:
        await ctx.send("❗ У вас нет установленной цели. Используйте !track_goal, чтобы установить её.")

# Список команд
@bot.command(name='commands')
async def send_commands_list(ctx):
    commands_list = """
    📜 Список доступных команд:
    !climate_facts - Отправляет случайный факт o глобальном потеплении.
    !what_is_global_warming - Объясняет, что такое глобальное потепление.
    !why_important - Говорит, почему это важно.
    !how_to_mitigate - Дает советы, как бороться c проблемой.

    !eco_challenge - Предлагает простое эко-задание.
    !track_goal - Пользователь устанавливает цель, бот отслеживает её выполнение.
    !progress - Показывает прогресс пользователя.

    !joke [type] - Отправляет шутку. Типы: general, dark.
    !magic [вопрос] - Отвечает на ваш вопрос магического шара.
    !commands - Показывает список всех команд.
    """
    await ctx.send(commands_list)

# Выключение бота и очистка сообщений
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("🛑 Bot is shutting down...")
    await bot.close()

@bot.command(name='clear')
@commands.is_owner()
async def clear(ctx, amount: int = 10):
    """Очищает последние n сообщений (по умолчанию 10)."""
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 Удалено {len(deleted)} сообщений.", delete_after=5)

# Загрузка и сохранение целей
import json

def load_goals():
    global user_goals
    try:
        with open('goals.json', 'r') as f:
            user_goals = json.load(f)
    except FileNotFoundError:
        user_goals = {}

def save_goals():
    with open('goals.json', 'w') as f:
        json.dump(user_goals, f)

@bot.event
async def on_ready():
    print("Bot is online!")
    load_goals()
    for guild in bot.guilds:
        for channel in guild.text_channels:
            await channel.send('Bot is online! Use "!commands" to see commands.')

@bot.event
async def on_disconnect():
    save_goals()

# Запуск бота
bot.run('Paste your Token here')