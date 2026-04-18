import time
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import main
import create_database
import config
import urllib.parse
import pandas as pd
import io

# Load Configuration
tg_token, tg_chat = config.Config.get_telegram_config()

def start(update, context):
    update.message.reply_text("🚀 *InvestorTimes Bot is Online!*\n\nSend me a Stock Symbol (e.g., RELIANCE) or upload a .txt file to start scraping.", parse_mode='Markdown')

def handle_message(update, context):
    text = update.message.text.strip().upper()
    if not text: return

    # Check if it looks like a symbol
    symbols = [s.strip() for s in text.replace(",", " ").split() if s.strip()]
    
    if symbols:
        update.message.reply_text(f"🔍 *Received symbols:* {', '.join(symbols)}\nStarting process...", parse_mode='Markdown')
        
        # We need a driver. Since this is a separate service, we'll get a fresh one.
        from processdriver import getedgedriver
        driver = getedgedriver()
        
        for symbol in symbols:
            update.message.reply_text(f"🔄 *Trying {symbol}...*")
            try:
                # Trigger the scrape
                import screenerpage
                screenerpage.search_screener1(driver, symbol)
                
                # Fetch result for feedback
                doc = create_database.comp_metadata_col.find_one({"code_names": symbol})
                last_q = doc.get('metadata', {}).get('recent_quarter', "Unknown")
                update.message.reply_text(f"✅ *{symbol}:* Got results for {last_q}!")
            except Exception as e:
                update.message.reply_text(f"❌ *{symbol}:* Failed! Error: {str(e)[:50]}...")
        
        driver.quit()
        update.message.reply_text("🏁 *Batch Process Completed.*")

def handle_document(update, context):
    file = context.bot.get_file(update.message.document.file_id)
    content = file.download_as_bytearray().decode("utf-8")
    
    symbols = []
    for line in content.splitlines():
        parts = line.split(",")
        symbols.extend([s.strip().upper() for s in parts if s.strip()])
    
    if symbols:
        update.message.reply_text(f"📂 *File received!* Found {len(symbols)} symbols. Starting batch scrape...", parse_mode='Markdown')
        # Reuse same logic
        from processdriver import getedgedriver
        driver = getedgedriver()
        for symbol in symbols:
            try:
                import screenerpage
                screenerpage.search_screener1(driver, symbol)
                update.message.reply_text(f"✅ {symbol} processed.")
            except:
                update.message.reply_text(f"❌ {symbol} failed.")
        driver.quit()
        update.message.reply_text("✅ *File processing complete.*")

def main_bot():
    updater = Updater(tg_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), handle_document))

    print("InvestorTimes Telegram Bot is listening...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main_bot()
