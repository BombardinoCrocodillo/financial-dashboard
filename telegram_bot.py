# telegram_bot.py - бот для дашборда "Процесс управления инвестициями"
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Конфигурация
TOKEN = "***"
DASHBOARD_URL = "http://127.0.0.1:8050/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - главное меню"""
    menu_text = (
        "📊 <b>Команды бота:</b>\n\n"
        "/start - Начать работу\n"
        "/help - Показать справку\n"
        "/dashboard - Получить ссылку на дашборд\n"
        "/status - Статус дашборда\n\n"
        "💡 <b>Дашборд «Процесс управления инвестициями» включает:</b>\n"
        "• Динамику портфеля\n"
        "• Распределение активов\n"
        "• Статистику по инвестициям\n"
        "• Анализ доходности"
    )

    await update.message.reply_text(menu_text, parse_mode='HTML')


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help - справка"""
    help_text = (
        "📋 <b>Справка по командам:</b>\n\n"
        "<b>/start</b> - Главное меню с описанием\n"
        "<b>/help</b> - Эта справка\n"
        "<b>/dashboard</b> - Получить прямую ссылку\n"
        "<b>/status</b> - Проверить доступность\n\n"
        "📈 <b>О системе:</b>\n"
        "Дашборд создан для мониторинга и управления инвестиционным портфелем."
    )

    await update.message.reply_text(help_text, parse_mode='HTML')


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /dashboard - ссылка на дашборд"""
    dashboard_text = (
        "🔗 <b>Ссылка на дашборд «Процесс управления инвестициями»:</b>\n\n"
        f"<code>{DASHBOARD_URL}</code>\n\n"
        "Нажмите на ссылку или скопируйте в браузер."
    )

    await update.message.reply_text(dashboard_text, parse_mode='HTML')


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status - проверка статуса"""
    import requests

    try:
        response = requests.get(DASHBOARD_URL, timeout=3)
        if response.status_code == 200:
            status_text = (
                "✅ <b>Статус:</b> Дашборд активен\n\n"
                "📊 Система «Процесс управления инвестициями» работает корректно\n"
                f"🔗 Доступен по адресу: {DASHBOARD_URL}"
            )
        else:
            status_text = (
                "⚠️ <b>Статус:</b> Дашборд отвечает с ошибкой\n\n"
                f"Код ответа: {response.status_code}\n"
                "Проверьте, запущен ли сервер."
            )
    except Exception:
        status_text = (
            "❌ <b>Статус:</b> Дашборд недоступен\n\n"
            "Сервер не отвечает.\n"
            "Запустите дашборд через VS Code или другую среду разработки."
        )

    await update.message.reply_text(status_text, parse_mode='HTML')


def main():
    """Запуск бота"""
    print("🤖 Запуск Telegram бота...")
    print("=" * 40)

    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("status", status))

    print("✅ Бот успешно запущен!")
    print("📱 Откройте Telegram и отправьте /start")
    print(f"📊 Дашборд: {DASHBOARD_URL}")
    print("=" * 40)

    # Запускаем бота
    app.run_polling()


if __name__ == "__main__":
    main()