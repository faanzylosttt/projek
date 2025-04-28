import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7847987165:AAExaFfM8F2eWgJc_0TG8k3xx3uiQKAOZxE"

MENU_FILE = "menu.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya siap membantu!\nKetik /listmenu untuk melihat semua menu.")

async def listmenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(MENU_FILE, "r") as file:
            menu = json.load(file)
        text = "**Daftar Menu:**\n"
        for idx, item in enumerate(menu, 1):
            text += f"{idx}. {item['text']} (Password: {item['password']})\n"
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def addmenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Format salah!\nGunakan: /addmenu NamaMenu Link Password")
        return
    nama, link, password = context.args[0], context.args[1], context.args[2]
    try:
        with open(MENU_FILE, "r") as file:
            menu = json.load(file)
        menu.append({
            "text": nama,
            "url": link,
            "password": password
        })
        with open(MENU_FILE, "w") as file:
            json.dump(menu, file, indent=2)
        await update.message.reply_text("Menu berhasil ditambahkan!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def editmenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 4:
        await update.message.reply_text("Format salah!\nGunakan: /editmenu Nomor NamaBaru LinkBaru PasswordBaru")
        return
    try:
        nomor = int(context.args[0]) - 1
        nama, link, password = context.args[1], context.args[2], context.args[3]
        with open(MENU_FILE, "r") as file:
            menu = json.load(file)
        if nomor < 0 or nomor >= len(menu):
            await update.message.reply_text("Nomor menu tidak valid.")
            return
        menu[nomor] = {
            "text": nama,
            "url": link,
            "password": password
        }
        with open(MENU_FILE, "w") as file:
            json.dump(menu, file, indent=2)
        await update.message.reply_text("Menu berhasil diedit!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def deletemenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Format salah!\nGunakan: /deletemenu Nomor")
        return
    try:
        nomor = int(context.args[0]) - 1
        with open(MENU_FILE, "r") as file:
            menu = json.load(file)
        if nomor < 0 or nomor >= len(menu):
            await update.message.reply_text("Nomor menu tidak valid.")
            return
        hapus = menu.pop(nomor)
        with open(MENU_FILE, "w") as file:
            json.dump(menu, file, indent=2)
        await update.message.reply_text(f"Menu '{hapus['text']}' berhasil dihapus!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("listmenu", listmenu))
    app.add_handler(CommandHandler("addmenu", addmenu))
    app.add_handler(CommandHandler("editmenu", editmenu))
    app.add_handler(CommandHandler("deletemenu", deletemenu))

    app.run_polling()

if __name__ == "__main__":
    main()