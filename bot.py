import telebot
import os
import logging

# تنظیم لاگ برای دیدن خطاها
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# دریافت توکن از متغیر محیطی
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    logger.error("❌ خطا: BOT_TOKEN تنظیم نشده! لطفا در Render تنظیم کن.")
    exit()

# ایجاد ربات
bot = telebot.TeleBot(TOKEN)

print("=" * 50)
print("🤖 ربات تلگرام در حال راه‌اندازی...")
print("=" * 50)

# دستور /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = f"""
سلام {message.from_user.first_name}! 👋

من ربات شخصی شما هستم.

📌 **دستورهای موجود:**
/start - همین پیام
/help - راهنمایی
/about - درباره ربات

🎯 **کاری که من می‌کنم:**
هر فایل (ویدیو، عکس، سند) را برای من فوروارد کن، من لینک مستقیم آن را می‌دهم.

ساخته شده با ❤️ توسط شما!
"""
    bot.reply_to(message, welcome_text)

# دستور /about
@bot.message_handler(commands=['about'])
def about_bot(message):
    about_text = """
🤖 **ربات لینک‌ساز تلگرام**

ویژگی‌ها:
• تبدیل فایل به لینک مستقیم
• پشتیبانی از ویدیو، عکس، فایل
• اجرا روی سرور Render
• کدنویسی با Python
"""
    bot.reply_to(message, about_text)

# دریافت فایل‌ها
@bot.message_handler(content_types=['document', 'video', 'audio', 'photo'])
def handle_file(message):
    try:
        # اطلاع دادن به کاربر
        bot.send_chat_action(message.chat.id, 'typing')
        
        # تشخیص نوع فایل
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            file_name = message.document.file_name or "فایل ناشناس"
            file_type = "📄 سند"
        elif message.video:
            file_info = bot.get_file(message.video.file_id)
            file_name = "ویدیو.mp4"
            file_type = "🎬 ویدیو"
        elif message.audio:
            file_info = bot.get_file(message.audio.file_id)
            file_name = message.audio.file_name or "صوت.mp3"
            file_type = "🎵 صوت"
        elif message.photo:
            file_info = bot.get_file(message.photo[-1].file_id)
            file_name = "عکس.jpg"
            file_type = "🖼️ عکس"
        
        # ساخت لینک مستقیم
        direct_link = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
        
        # ارسال پاسخ
        response = f"""
{file_type} دریافت شد!

📁 نام: {file_name}
🔗 لینک مستقیم: `{direct_link}`

💡 برای دانلود سریع، لینک را در IDM یا مرورگر کپی کن.
"""
        bot.reply_to(message, response, parse_mode='Markdown')
        logger.info(f"فایل دریافت شد: {file_name}")
        
    except Exception as e:
        error_msg = f"⚠️ خطا در پردازش فایل: {str(e)}"
        bot.reply_to(message, error_msg)
        logger.error(f"خطا: {e}")

# پاسخ به پیام‌های متنی
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    response = f"شما نوشتید: '{message.text}'\n\nیک فایل برای من فوروارد کن تا لینک مستقیم آن را بدهم."
    bot.reply_to(message, response)

# اجرای ربات
if __name__ == '__main__':
    try:
        logger.info("ربات شروع به کار کرد...")
        bot.polling(none_stop=True, interval=2, timeout=60)
    except Exception as e:
        logger.error(f"خطا در اجرای ربات: {e}")
