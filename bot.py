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

api_id = int(os.environ.get("10705499"))
api_hash = os.environ.get("36eb83e16913a7b06e935bc31eddc486")
bot_token = os.environ.get("2112481927:AAFNCS70I8FjvMvQUMQSsPhH-4yyWq123Yc")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**Salam 👋 Men @DBMBOSSdu 🖤 terefinden yaradılmış tağ botuyam**, Qrupda Bütün userleri tağ ede bilerem 👻**/help** basaraq elave melumat elde ede bilersiniz.
    link_preview=False,
    buttons=(
      [
        Button.url('🇦🇿 Qrup', 'https://t.me/DBMsohbet'),
        Button.url('⚜️ Sahib', 'https://t.me/DBMBOSSdu')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Tağ botunun Kömek Menyusuna xoş gelmisiniz**\n\nKomandalar: /all\n__Bu komanda tağ sebeb meqsedile nezerde tutulmuşdur.__\n`Meselen: /all Sabahınız xeyir!`\n__Bu emri istenilen mesaja cavab olaraq vere bilersiniz. Bot istifadeçileri hemin cavablandırılan mesaja işareleyecek"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('🇦🇿 Qrup', 'https://t.me/DBMsohbet'),
        Button.url('⚜️ Sahib', 'https://t.me/DBMBOSSdu')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__Bu kamanda yalnız Qruplarda ve Kanallada Keçerlidir!__")
  
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
    return await event.respond("__Yalnız adminler tağ ede bilerler!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Mene arqument verin!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__Men köhne mesajlara göre tağ etmirem! (Men qrupa elave edilmemişden evvel gönderilen mesajlar)__")
  else:
    return await event.respond("__Mesaja cavab verin yada tağ sebebini yazın!__")
  
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
    return await event.respond('__Burada heç bir proses baş vermir...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Dayandırıldı.__')

print(">> BOT STARTED <<")
client.run_until_disconnected()
