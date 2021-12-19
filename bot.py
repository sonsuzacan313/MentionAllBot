import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "**Salam 👋❤️ Mən @DBMBOSSdu tərəfindən yaradılmış tağ botuyam**, Qrupda və Kanallarda Hamını tağ edə bilərəm 👻🌹\nToxun **/help** daha çox məlumatı əldə edə bilərsiniz",
    link_preview=False,
    buttons=(
      [
        Button.url('🇦🇿 Qrup', 'https://t.me/OSCAR_sohbett'),
        Button.url('⚜️ Sahib', 'https://t.me/DBMBOSSdu')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**🔐Botun menyusuna xoş gəlmisiniz**\n\nKomandalar: /all\n__Bu komandanı Tağ etmək səbəbi ilə işlədə bilərsiniz.__\n`Məsələn: /all Sabahınız xeyir!`\n__Bu komandanı kiməsə yanıt olaraq istifadə edin və yaxud tağ səbəbini yazın__."
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('🇦🇿 Qrup', 'https://t.me/OSCAR_sohbett'),
        Button.url('⚜️ Sahib', 'https://t.me/DBMBOSSdu')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__📢Bu komanda yalnız Qrup və Kanallarda istifadə edilə bilər!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__💎Yalnız adminlər tağ edə bilərlər!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__⛓️Tağ sebebini yaz!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__📍Mən köhnə mesajları tağ edə bilmirəm! (Mən qrupa əlavə edilməmişdən əvvəl göndərilən mesajlar)__")
  else:
    return await event.respond("__❕Hansısa bir mesajı yanıtla və yaxud tağ səbəbini yaz!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__🚫Heç bir proses baş vermir...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__❌Dayandırıldı.__')

print(">> BOT STARTED <<")
client.run_until_disconnected()
