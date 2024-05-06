import telebot 
from telebot import types
import random
import re
bot = telebot.TeleBot('7058621710:AAGIgWsRii3evWl_pBBEqlbsNjuPG3wSfOg')

user_info = {}

email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
phone_pattern = re.compile(r'^\d{10,15}$')

# تابع ماشین حساب
def calculate(expression):
    try:
        # ارزیابی عبارت ریاضی
        result = eval(expression, {'__builtins__': None}, {})
        return result
    except Exception as e:
        # در صورت وجود خطا، پیام خطا را برگردان
        return str(e)

# تعریف دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, "سلام! لطفا نام خود را وارد کنید.")
    bot.register_next_step_handler(msg, process_name_step)
    
def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user_info[chat_id] = {'name': name}
        msg = bot.reply_to(message, "نام خانوادگی خود را وارد کنید.")
        bot.register_next_step_handler(msg, process_surname_step)
    except Exception as e:
        bot.reply_to(message, 'خطایی رخ داده است.')

def process_surname_step(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        user_info[chat_id]['surname'] = surname
        msg = bot.reply_to(message, "سن خود را وارد کنید.")
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'خطایی رخ داده است.')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, "لطفا سن خود را به صورت عدد وارد کنید.")
            bot.register_next_step_handler(msg, process_age_step)
            return
        user_info[chat_id]['age'] = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('مرد', 'زن', 'ترجیح می‌دهم نگویم')
        msg = bot.reply_to(message, "جنسیت خود را انتخاب کنید.", reply_markup=markup)
        bot.register_next_step_handler(msg, process_gender_step)
    except Exception as e:
        bot.reply_to(message, 'خطایی رخ داده است.')

def process_gender_step(message):
    try:
        chat_id = message.chat.id
        gender = message.text
        user_info[chat_id]['gender'] = gender
        msg = bot.reply_to(message, "ایمیل خود را وارد کنید.")
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'خطایی رخ داده است.')

def process_email_step(message):
    try:
        chat_id = message.chat.id
        email = message.text
        if not re.fullmatch(email_pattern, email):
            msg = bot.reply_to(message, "لطفا یک ایمیل معتبر وارد کنید.")
            bot.register_next_step_handler(msg, process_email_step)
            return
        user_info[chat_id]['email'] = email
        msg = bot.reply_to(message, "شماره تلفن خود را وارد کنید.")
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message, 'خطایی رخ داده است.')

def process_phone_step(message):
    try:
        chat_id = message.chat.id
        phone = message.text
        if not re.fullmatch(phone_pattern, phone):
            msg = bot.reply_to(message, "لطفا یک شماره تلفن معتبر وارد کنید.")
            bot.register_next_step_handler(msg, process_phone_step)
            return
        user_info[chat_id]['phone'] = phone
        msg = bot.reply_to(message, "چگونه با شرکت ما آشنا شدید؟")
        bot.register_next_step_handler(msg, process_acquaintance_step)
    except Exception as e:
        bot.reply_to(message, 'خطایی رخ داده است.')

def process_acquaintance_step(message):
    try:
        username = message.from_user.username
        chat_id = message.chat.id
        acquaintance = message.text
        user_info[chat_id]['acquaintance'] = acquaintance
        # اختصاص دادن کد رهگیری تصادفی
        tracking_code = random.randint(0, 1000000)
        user_info[chat_id]['tracking_code'] = tracking_code
        # اینجا می‌توانید اطلاعات را در دیتابیس ذخیره کنید
        bot.send_message(chat_id, f"نام: {user_info[chat_id]['name']}\nنام خانوادگی: {user_info[chat_id]['surname']}\nسن: {user_info[chat_id]['age']}\nجنسیت: {user_info[chat_id]['gender']}\nایمیل: {user_info[chat_id]['email']}\nشماره تلفن: {user_info[chat_id]['phone']}\nنحوه آشنایی با شرکت: {user_info[chat_id]['acquaintance']}\nکد رهگیری: {tracking_code}\n آیدی شما: {chat_id}\n آیدی تلگرام شما: @{username}\n لطفا با زدن دکمه سوال ، سوال خود را بپرسید!")
    except Exception as e:
        bot.reply_to(message, 'خطایی رخ داده است.')


# کامند ماشین حساب
@bot.message_handler(commands=['banana_calculator'])
def banana_calculator_command(message):
    msg = bot.reply_to(message, "لطفا عبارت ریاضی خود را وارد کنید.")
    bot.register_next_step_handler(msg, process_calculation)

def process_calculation(message):
    try:
        chat_id = message.chat.id
        expression = message.text
        # تأیید عبارت ریاضی
        if not re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expression):
            bot.send_message(chat_id, "لطفا فقط از اعداد و عملگرهای ریاضی استفاده کنید.")
            return
        result = calculate(expression)
        bot.send_message(chat_id, f"نتیجه: {result}")
    except Exception as e:
        bot.send_message(chat_id, f"خطا: {e}")

#کامند ثبت شکایت
@bot.message_handler(commands=['banana'])
def submit_complaint(message):
    msg = bot.reply_to(message, "لطفا شکایت خود را وارد کنید.")
    bot.register_next_step_handler(msg, process_complaint)

def process_complaint(message):
    try:
        chat_id = message.chat.id
        complaint = message.text
        # اینجا می شود اقدامات لازم برای ثبت در دیتابیس را انجام داد
        # ...
        bot.send_message(chat_id, "ممنون از انتقاد شما. این موضوع پیگیری می‌شود.")
    except Exception as e:
        bot.send_message(chat_id, f"خطا در ثبت شکایت: {e}")



#پاسخ به کامند امتیاز دهی
@bot.message_handler(commands=['banana_rate'])
def send_banana(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("⭐")
    item2=types.KeyboardButton("⭐⭐")
    item3=types.KeyboardButton("⭐⭐⭐")
    item4=types.KeyboardButton("⭐⭐⭐⭐")
    item5=types.KeyboardButton("⭐⭐⭐⭐⭐")
    item6=types.KeyboardButton("/banana_question")
    markup.add(item1,item2,item3,item4,item5,item6)
    bot.send_message(message.chat.id,"لطفا به این مکالمه امتیاز دهید!",reply_markup=markup)
#پاسخ به کامند پاسخ سوالات
@bot.message_handler(commands=['banana_question'])
def send_banana(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("راه های ارتیاطی")
    item2=types.KeyboardButton("آدرس دفتر مرکزی شما کجاست؟")
    item3=types.KeyboardButton("مدیر عامل شرکت شما کیست؟")
    item4=types.KeyboardButton("شما موز های خود را از کجا وارد می کنید؟")
    item5=types.KeyboardButton("آیا برای واردات موز از ارز نیمایی استفاده می کنید؟")
    item6=types.KeyboardButton("ارز نیمایی چقدر است؟")
    item7=types.KeyboardButton("برای همکاری با شرکت موز گستر پارسیان باید چه ویژگی های داشته باشم؟")
    item8=types.KeyboardButton("موز های شما در هنگام واردات چه رنگی هستند؟")
    item9=types.KeyboardButton("در چه کشور هایی دفتر فروش دارید؟")
    item10=types.KeyboardButton("سوالم در بین گزینه ها نیست!")
    item11=types.KeyboardButton("/banana_rate")
    markup.add(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11)
    bot.send_message(message.chat.id,"سوال خود را انتخاب کنید!",reply_markup=markup)

#پاسخ به سوالات
@bot.message_handler(func=lambda message:True)
def handle_other_message(message):
    if message.text == "راه های ارتیاطی":
        website = "www.mozgoster.ir"
        email = "mozgostar.com"
        phone = "02145673287"
        telegram = "@mozgostar"
        contact_info = f":راه های ارتباطی \n وب سایت:{website}\n ایمیل:{email}\n شماره تماس:{phone}\n آیدی تلگرام:{telegram}"
        bot.send_message(message.chat.id , contact_info)
    elif message.text == "آدرس دفتر مرکزی شما کجاست؟" :
        bot.send_message(message.chat.id , "آدیسا بابا جنب کوچهء ششم پلاک 8756")
    elif message.text == "مدیر عامل شرکت شما کیست؟" :
        bot.send_message(message.chat.id , "آقای موزیان (پسر آقای موزیان بزرگ) که با رانت پدر این شرکت را راه اندازی کرده اند")
    elif message.text == "شما موز های خود را از کجا وارد می کنید؟" :
        bot.send_message(message.chat.id , "شرکت موز گستر پارسیان موز هایش را از کشور های اندونزی ، فیلیپین ، کامبوج ، سیبری و  آمریکا وارد می کند!")
    elif message.text == "آیا برای واردات موز از ارز نیمایی استفاده می کنید؟" :
        bot.send_message(message.chat.id , "بله ، با کمک آقای موزیان بزرگ توانسته ایم به افتخار دست پیدا کنیم اما به صورت اسلامی استفاده می کنیم!")
    elif message.text == "ارز نیمایی چقدر است؟" :
        bot.send_message(message.chat.id , "من صرفا یک بات هستم و از قیمت ارز در کشور شما اطلاعی ندارم!")
    elif message.text == "برای همکاری با شرکت موز گستر پارسیان باید چه ویژگی های داشته باشم؟" :
        bot.send_message(message.chat.id , "یا باید خوشگل باشید یا فامیل آقای موزیان")
    elif message.text == "موز های شما در هنگام واردات چه رنگی هستند؟" :
        bot.send_message(message.chat.id , "موز های شرکت موز گستر پارسیان در هنگام بارگیری سبز و در هنگام تحویل زرد رنگ می باشند")
    elif message.text == "در چه کشور هایی دفتر فروش دارید؟" :
        bot.send_message(message.chat.id , "در کشور هایی نظیر ایران ، عراق ، مکزیک ، آمریکا ،آلمان ، اسپانیا و کامبوج")
    elif message.text == "سوالم در بین گزینه ها نیست!" :
        bot.send_message(message.chat.id , "به آیدی موجود در بخش راه های ارتباطی پیام بدهید!")
    elif message.text == "بازگشت":
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id , "شما بازگشتیده شدید")
    elif message.text == "ممنونم" :
        bot.send_message(message.chat.id , "ممنان")
    elif message.text == "آقای قربانیان" :
        bot.send_message(message.chat.id , "به شدت معلم خوش سیما و خوش صدا اصلا یه پا صداسیما با مدیریت آقای محمودی")
    elif message.text == "⭐" :
        bot.send_message(message.chat.id , "مشکل داری؟ ما داریم اینجا زحمت می کشیم!")
    elif message.text == "⭐⭐" :
        bot.send_message(message.chat.id , "از آقای قربانیان خجالت بکش")
    elif message.text == "⭐⭐⭐" :
        bot.send_message(message.chat.id , "آقا موزیان میاد سراغت")
    elif message.text == "⭐⭐⭐⭐" :
        bot.send_message(message.chat.id , "ممنان")
    elif message.text == "⭐⭐⭐⭐⭐" :
        bot.send_message(message.chat.id , "یک عدد موز طلایی خدمت شما")
    else:
        bot.send_message(message.chat.id , "من یک ربات هستم و متوجه صحبت شما نمی شوم!")
if __name__=='__main__':
    bot.polling()