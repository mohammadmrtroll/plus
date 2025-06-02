admin_bot = ["u0FrdRR00f23f8590735e10a9bfe3948" , "u0DxF7B0f62176f405a9a1afa47f64bd" , "u0IGkrw0e7e9abe034815c5bceed52e4"]

from rubpy import Client , filters
from rubpy.types import Update
import json
import os
import re
from time import time
import asyncio
import aiohttp
import time
import jdatetime
import datetime
import random

bot = Client("chatbot")




last_replied = {}
last_reply_time = {}




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


# لود لیست VIP Group GUID
VIP_FILE = "vip_groups.json"
def load_vip_groups():
    if os.path.exists(VIP_FILE):
        with open(VIP_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

VIP_GROUPS_FILE = 'vip_groups.json'

def load_vip_groups():
    if os.path.exists(VIP_GROUPS_FILE):
        with open(VIP_GROUPS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

vip_groups = load_vip_groups()

VIP_GROUPS_FILE = 'vip_groups.json'

def load_vip_groups():
    if os.path.exists(VIP_GROUPS_FILE):
        with open(VIP_GROUPS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

vip_groups = load_vip_groups()

# ذخیره لیست VIP Group GUID
def save_vip_groups(vip_groups):
    with open(VIP_FILE, "w", encoding="utf-8") as f:
        json.dump(vip_groups, f, indent=4, ensure_ascii=False)

# تایع خودم
def load_admins():
    with open("admins.json", "r") as f:
        return json.load(f)  # فرض بر اینه که admins.json لیستی از گویدهاست

def save_admins(admins):
    with open("admins.json", "w") as f:
        json.dump(admins, f, indent=2)


# YAD

memory_file = "memory.json"

# بارگذاری حافظه (یکبار در ابتدای فایل اصلی رباتت بذار)
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}



@bot.on_message_updates()
async def handle_message(m: Update):
    global groups ,admins , vip_groups , memory_file , last_reply_time ,last_time 

    user_guid = str(m.author_guid)
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
    
    # بقیه کد ادامه پیدا کنه



    if text.startswith("حذف ادمین "):
        if str(m.author_guid) not in admin_bot:
            await m.reply("شما اجازه حذف ادمین را ندارید.✘")
            return

        admins = load_admins()
        parts = text.split(" ", 2)
        if len(parts) < 3:
            await m.reply("✘ فرمت صحیح: حذف ادمین [گوید]")
            return

        user_guid = parts[2].strip()

        try:
            user_info = await bot.get_user_info(user_guid)
            user_name = f"{user_info.first_name} {user_info.last_name}".strip() or user_info.username or "کاربر ناشناس"
        except:
            user_name = "کاربر ناشناس"

        if user_guid not in admins:
            await m.reply(f"کاربر 「{user_name}」 در لیست ادمین‌ها نیست.✘")
        else:
            admins.remove(user_guid)
            save_admins(admins)
            await m.reply(f"کاربر 「{user_name}」 از لیست ادمین‌ها حذف شد.")

    # دستور افزودن ادمین
    elif text.startswith("ادمین "):
        if str(m.author_guid) not in admin_bot:
            await m.reply("شما اجازه افزودن ادمین را ندارید.✘")
            return

        parts = text.split(" ", 1)
        if len(parts) < 2:
            await m.reply("✘ فرمت صحیح: ادمین [گوید]")
            return

        user_guid = parts[1].strip()

        admins = load_admins()

        try:
            user_info = await bot.get_user_info(user_guid)
            user_name = f"{user_info.first_name} {user_info.last_name}".strip() or user_info.username or "کاربر ناشناس"
        except:
            user_name = "کاربر ناشناس"

        if user_guid in admins:
            await m.reply(f"کاربر 「{user_name}」 قبلاً ادمین است.✘")
        else:
            admins.append(user_guid)
            save_admins(admins)
            await m.reply(f"کاربر 「{user_name}」 به لیست ادمین‌ها اضافه شد.")


        user_guid = parts[1].strip()
        admins = load_admins()

        # دریافت اسم کاربر بر اساس گوید
        try:
            user_info = await bot.get_user_info(user_guid)
            user_name = f"{user_info.first_name} {user_info.last_name}".strip() or user_info.username or "کاربر ناشناس"
        except:
            user_name = "کاربر ناشناس"

        if user_guid in admins:
            await m.reply(f" کاربر「{user_name}」قبلاً در لیست ادمین‌ها وجود دارد.✓ ")
        else:
            admins.append(user_guid)
            save_admins(admins)
            await m.reply(f" کاربر「{user_name}」به لیست ادمین‌ها اضافه شد.✓ ")


    if m.text.strip() == "گوید":
        if m.reply_message_id:
            reply_user = await m.get_reply_author()
            await m.reply(f"گوید کاربر: {reply_user.user_guid}")
        else:
            await m.reply(" لطفاً این دستور را روی پیام کاربر موردنظر ریپلای بزنید.✘")


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




    user_id = m.author_guid
    now = time.time()

    # محدودیت پاسخ هر 10 ثانیه به یک کاربر
    if user_id in last_replied and (now - last_replied[user_id]) < 15:
        return

    elif m.text.startswith("بگو"):
        if not m.is_group:
            await m.reply(":x: این دستور فقط در گروه قابل استفاده است.")
            return
        text = m.text[3:].strip()
        if text:
            last_replied[user_id] = now  # ذخیره زمان آخرین پاسخ

            await asyncio.sleep(0.2)  # تاخیر 2 ثانیه
            await m.reply(text)



    # چک کن پیام توی گروه هست
    if m.text.strip() == "گوید":
        if text.lower() in ["ادمین", "admins"]:
            try:
                with open("admins.json", "r") as f:
                    admins_list = json.load(f)  # این لیست ساده‌ست مثل ["guid1", "guid2"]
                
                if not admins_list:
                    await m.reply(":warning: هیچ ادمینی ثبت نشده است.")
                else:
                    msg = ":small_orange_diamond: لیست ادمین‌های ربات:\n\n"
                    for i, admin in enumerate(admins_list, 1):
                        msg += f"{i}. {admin}\n"
                    await m.reply(msg)
            
            except Exception as e:
                await m.reply(f":x: خطا در دریافت لیست ادمین‌ها:\n{e}")



    if text.startswith("VIP "):
        if str(m.author_guid) not in admin_bot:
            await m.reply("❌ شما اجازه استفاده از این دستور را ندارید.")
            return

        if not m.is_private:
            await m.reply("❌ این دستور فقط در پی‌وی قابل استفاده است.")
            return

        match = re.match(r"^VIP\s+(https?://\S+)", text)
        if not match:
            await m.reply("❌ فرمت لینک صحیح نیست. لطفا به صورت زیر ارسال کنید:\nVIP <لینک>")
            return

        vip_link = match.group(1)

        try:
            # استخراج کد جوین از لینک
            link_code = vip_link.split("/")[-1]

            join_result = await bot.join_group(link_code)
            group_guid = join_result.group_guid

            vip_groups = load_vip_groups()
            if group_guid in vip_groups:
                await m.reply("✅ این گروه قبلا به لیست VIP اضافه شده است.")
            else:
                vip_groups.append(group_guid)
                save_vip_groups(vip_groups)
                await m.reply(f"✅ گروه به لیست VIP اضافه شد.\nGUID: {group_guid}")

        except Exception as e:
            await m.reply(f"❌ خطا در عضویت در گروه:\n{e}")









# vip cod












    if m.is_group:
        if str(m.object_guid) not in vip_groups:
            return  # فقط در گروه‌های VIP کار می‌کند
    if text.startswith("یاد بگیر در جواب ") and " بگو " in text:
        try:
            parts = text.split(" بگو ")
            trigger = parts[0].replace("یاد بگیر در جواب ", "").strip()
            response = parts[1].strip()

            if trigger in memory:
                await m.reply(f"برای '{trigger}' قبلاً یاد گرفتم، نمیتونی تغییرش بدی.")
                return

            memory[trigger] = response

            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(memory, f, ensure_ascii=False, indent=2)

            await m.reply(f"یاد گرفتم که در جواب '{trigger}' بگویم '{response}'.")
        except Exception:
            await m.reply("دستور رو درست وارد کن مثل: یاد بگیر در جواب سلام بگو خوبی")
        return

    # پاسخ دادن به پیام‌هایی که قبلا یاد گرفته شده
    for trigger in memory:
        if trigger in text:
            # چک کردن فاصله زمانی پاسخ قبلی به این کاربر
            last_time = last_reply_time.get(user_id, 0)
            if now - last_time < 7:  # کمتر از 7 ثانیه گذشته
                return  # پاسخ نده

            # اگر 7 ثانیه گذشته بود پاسخ بده و زمان را به روز کن
            last_reply_time[user_id] = now
            await asyncio.sleep(.5)  # تاخیر 5 ثانیه قبل از پاسخ
            await m.reply(memory[trigger])
            return


bot.run()
    # بقیه دستورات...