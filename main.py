from telebot import *
import _info

bot = TeleBot(_info.TOKEN)

global talkChatId
global requestChatId
global reportChatId

talkChatId = set()
requestChatId = set()
reportChatId = set()
blackList = {"хуй", "пиздец", "блять"}


@bot.message_handler(commands=['become_talk'])
def become_talk(message):
    if message.from_user.id in [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]:
        if message.chat.id not in talkChatId:
            talkChatId.add(message.chat.id)
            reportChatId.discard(message.chat.id)
            requestChatId.discard(message.chat.id)
            bot.send_message(message.chat.id, "It's talk chat now!")
        else:
            bot.send_message(message.chat.id, "It's talk chat already!")
    else:
        bot.send_message(message.chat.id, "У вас недостаточно прав.")


@bot.message_handler(commands=['become_report'])
def become_report(message):
    if message.from_user.id in [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]:
        if message.chat.id not in reportChatId:
            talkChatId.discard(message.chat.id)
            reportChatId.add(message.chat.id)
            requestChatId.discard(message.chat.id)
            bot.send_message(message.chat.id, "It's report chat now!")
        else:
            bot.send_message(message.chat.id, "It's report chat already!")
    else:
        bot.send_message(message.chat.id, "У вас недостаточно прав.")


@bot.message_handler(commands=['become_request'])
def become_request(message):
    if message.from_user.id in [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]:
        if message.chat.id not in requestChatId:
            talkChatId.discard(message.chat.id)
            reportChatId.discard(message.chat.id)
            requestChatId.add(message.chat.id)
            bot.send_message(message.chat.id, "It's request chat now!")
        else:
            bot.send_message(message.chat.id, "It's request chat already!")
    else:
        bot.send_message(message.chat.id, "У вас недостаточно прав.")


@bot.message_handler(content_types=['text'])
def listen(message):
    if message.chat.id in talkChatId:
        for word in message.text.split():
            if word.lower() in blackList:
                bot.send_message(message.chat.id, f"@{message.from_user.username}, не выражайся!")
                bot.delete_message(message.chat.id, message.id)
                for chat_id in reportChatId:
                    bot.send_message(chat_id, f"Чат: {message.chat.title}\n"
                                              f"Пользователь: @{message.from_user.username}\n"
                                              f"Текст: {message.text}")
        if "@KlarkSimpleChatBot" in message.text:
            for chat_id in requestChatId:
                bot.send_message(chat_id, f"Поступило сообщение\n"
                                          f"Беседа: {message.chat.title}/{message.chat.id}\n"
                                          f"Пользователь: {message.from_user.username}")
                bot.forward_message(chat_id, message.chat.id, message.id)

    if message.chat.id in requestChatId:
        if message.reply_to_message is not None:
            bot.send_message(message.reply_to_message.forward_from.id, f"Поступил ответ на ваш вопрос:\n"
                                                                       f"{message.reply_to_message.text}\n"
                                                                       f"Ответ:\n"
                                                                       f"{message.text}")


if __name__ == '__main__':
    bot.polling()
