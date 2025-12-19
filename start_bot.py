# start_bot.py - запуск только бота
import sys
import os

# Добавляем текущую папку в путь Python
sys.path.append(os.path.dirname(__file__))

print("🤖 ЗАПУСК TELEGRAM БОТА")
print("=" * 40)

# Импортируем и запускаем
try:
    from telegram_bot import main
    main()
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nУбедитесь, что:")
    print("1. Файл telegram_bot.py в той же папке")
    print("2. Установлен python-telegram-bot: pip install python-telegram-bot")
    input("\nНажмите Enter...")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    input("\nНажмите Enter...")

