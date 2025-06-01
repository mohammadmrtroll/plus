main_admin_guid = "u0FrdRR00f23f8590735e10a9bfe3948"  

from rubpy import Client
from rubpy.types import Update
import json
import os
import re

bot = Client("chatbot")


# گرفتن گروه
GROUPS_FILE = "groups.json"

def load_groups():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return json.load(f)
    return []

def save_groups(groups):
    with open(GROUPS_FILE, "w") as f:
        json.dump(groups, f, indent=2)

groups = load_groups()


# گرفتن ادمین

ADMINS_FILE = "admins.json"

def load_admins():
    if os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def save_admins(admins):
    with open(ADMINS_FILE, "w", encoding="utf-8") as f:
        json.dump(admins, f, ensure_ascii=False, indent=2)

admins = load_admins()

# input name 


async def get_name(bot, user_guid):
    try:
        user_info = await bot.get_user_info(user_guid)
        user = user_info.get('user', {})
        first_name = user.get('first_name', '')
        last_name = user.get('last_name', '')
        full_name = (first_name + ' ' + last_name).strip()
        return full_name if full_name else user.get('username', 'کاربر')
    except:
        return "کاربر"



@bot.on_message_updates()
async def handle_message(m: Update):
    global groups , admins
    if not m.text:
        return

    text = m.text.strip()

    # اگر پیام شامل دستور جوین هست
    match = re.match(r"^(جوین|join)\s+(https://rubika\.ir/joing/([a-zA-Z0-9]+))$", text)
    if match:
        link_code = match.group(3)
        try:
            join_result = await bot.join_group(link_code)
            group_guid = join_result.group_guid

            if group_guid not in groups:
                groups.append(group_guid)
                save_groups(groups)

            await m.reply(f"✅ عضو گروه شدم!\nGroup GUID: {group_guid}")
        except Exception as e:
            await m.reply(f"❌ خطا در عضویت در گروه:\n{e}")
        return
        

    

    if match:
        # اضافه کن شرط پیوی
        if not m.is_private:
            return  # اگر پیام تو گروه یا جایی غیر از پیوی بود کاری نکن
    
    # بقیه کد ادامه پیدا کنه
    ...

    # فقط اگر گروه هست و در لیست گروه‌ها عضو است
    if m.object_guid in groups:
        if "سلام" in text:
            await m.reply("سلام")




    elif text.startswith("ادمین "):
        if str(m.author_guid) != main_admin_guid:
            await m.reply("❌ شما اجازه افزودن ادمین را ندارید.")
            return

        parts = text.split(" ", 1)
        if len(parts) < 2:
            await m.reply("❌ فرمت صحیح: ادمین [گوید]")
            return

        user_guid = parts[1].strip()
        admins = load_admins()

        if user_guid in admins:
            await m.reply("✅ این گوید قبلاً اضافه شده.")
        else:
            admins.append(user_guid)
            save_admins(admins)
            await m.reply(f"✅ گوید {user_guid} به لیست ادمین‌ها اضافه شد.")


    if m.text.strip() == "گوید":
        if m.reply_message_id:
            reply_user = await m.get_reply_author()
            await m.reply(f"گوید کاربر: {reply_user.user_guid}")
        else:
            await m.reply("❌ لطفاً این دستور را روی پیام کاربر موردنظر ریپلای بزنید.")


    elif m.text.strip().lower() == "ad bot":
        if m.author_guid in admins:
            if m.reply_message_id:
                # گرفتن گوید کاربری که روش ریپلای شده
                message = await m.get_messages(m.object_guid, [m.reply_message_id])
                target_guid = message['messages'][0]['author_object_guid']

                # بررسی تکراری نبودن
                if target_guid not in admins:
                    admins.append(target_guid)
                    save_admins(admins)
                    await m.reply(f"✅ کاربر با گوید {target_guid} به لیست ادمین اضافه شد.")
                else:
                    await m.reply("⚠️ این کاربر قبلاً ادمین بوده.")
            else:
                await m.reply("❌ لطفاً روی پیام کاربر ریپلای کنید و دستور را بزنید.")
        else:
            await m.reply("🚫 شما دسترسی لازم برای استفاده از این دستور را ندارید.")

    # ادامه کدهای دیگر
bot.run()
    # بقیه دستورات...