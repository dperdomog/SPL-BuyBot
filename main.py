from telegram.ext import ApplicationBuilder
from handlers import setup_handlers
from constants import TOKEN

def main():
    print("Bot Token:", TOKEN)  # Print token for verification
    application = ApplicationBuilder().token(TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == '__main__':
    main()
