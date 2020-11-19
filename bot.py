
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'runner' # change to what you need
#BOT_OWNER_ROLE_ID = "778999965451288616"
  

oot_channel_id_list =[
    "778780076354437161", #SwagBucks Sparks
    "756445815001710632", #SwagBucks TRIVIA Bot
    "729535056594337812", #SwagBucks Trivia Viper King
    "774605363114803230", #SwagBucks Trivia Eagle
    "743339722444636251", #Swagbucks Magic text
    "755080891004354630", #SwagBucks Trivia Challenge
    "747500994316992613", #SwagBucks Smart world
    "747465526728720554", #SwagBucks Trivia Time
    "773602513597235231", #SwagBucks DRAGON World
    "776648141315112970", #SwagBucks Phoneix Trivia
    "748859081737109595", #SWAGBUCKS BRIGHT TRIVIA
    "773390146406055937", #SwagBucks Trivia Galaxy
    "772056500217577515", #SwagBucks Google Pro
    "740581485462945894", #SwagBucks Trivia Velocity
    "774436021244788787", #SwagBucks Gaming Community
    "773336365311590431", #SwagBucks Imperio
    "774480600010457108", #SwagBucks UKT
]


answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf|c)?(\?)?$', re.IGNORECASE)

apgscore = 402
nomarkscore = 348
markscore = 252

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Trivia Library Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', ' ').replace(" ", " ")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="**Connected With Crowd**", description="", color=0xADFF2F)
        self.embed.set_author(name ='Trivia Company Pvt Ltd',url=' ',icon_url='https://cdn.discordapp.com/attachments/765487385885671425/765850682535706645/IMG_20201014_134652.png')
        self.embed.add_field(name="**``Option 1``**", value="**0**", inline=False)
        self.embed.add_field(name="**``Option 2``**", value="**0**", inline=False)
        self.embed.add_field(name="**``Option 3``**", value="**0**", inline=False)
        self.embed.set_footer(text=f"© Developed by The Badshah Company", \
            icon_url="https://cdn.discordapp.com/attachments/765487385885671425/765850682535706645/IMG_20201014_134652.png")
        self.embed.set_thumbnail(url ='https://www.gstatic.com/allo/stickers/pack-8/v5/xxhdpi/7.gif')
        # await bot.add_reaction(message = "self.embed",emoji = ":white_check_mark:")
        # await self.bot.add_reaction(embed,':rtlogo:')



    async def clear_results(self):
        for i in range(len(self.answer_scores)):
          self.answer_scores[i]=0

    async def update_embeds(self):

         

        one_check = ""
        two_check = ""
        three_check = ""
        

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)
#         lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
         

        if highest > 0:
            if answer == 1:
                one_check = " :one::white_check_mark:  "
            if answer == 2:
                two_check = " :two::white_check_mark:  "
            if answer == 3:
                three_check = " :three::white_check_mark: "
                
#         if lowest < 0:
#             if answer == 1:
#                 one_check = " :x:  "
#             if answer == 2:
#                 two_check = " :x:  "
#             if answer == 3:
#                 three_check = " :x:  "            
 
        self.embed.set_field_at(0, name="**``Option 1``**", value="{0}{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="**``Option 2``**", value="{0}{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="**``Option 3``**", value="{0}{1}".format(lst_scores[2], three_check))
        if self.embed_msg is not None:
           await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("ROYAL TRIVIA")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        await self.change_presence(activity=discord.Game(name=' With Developed by 𝕿𝖍𝖊 ẞ𝖆𝖉𝖘𝖍𝖆𝖍'))

    async def on_message(self, message):
        global id1,msgid
        # if message is private
        if message.author == self.user or message.guild == None:
            return
       # if message.content.lower() == "-channel":
          #  pd = message.content 
          #  id1 = pd[9:] 
          #  await message.channel.send(f'channel <#{id1}> selected.')

        if message.content.lower() == "+":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**make ``runner`` role and taken self** ")
            return

        if message.content.startswith('-help'):
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="Help Commands", description="**How Run Bot**", color=0x00ff00)
           embed.add_field(name="Support Game", value="**Loco\nBrainbaazi\nPollbaazi\nSwag-iq\nThe-Q\nConfett-India\nCash-Quiz-Live\nHQ Tivia**", inline=False)
           embed.add_field(name="when Question come put command", value="** ``.``  is command work for all support game**", inline=False)
           await message.channel.send(embed=embed)

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', ' ').replace(" ", " ")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('Nzc4OTk5OTY1NDUxMjg4NjE2.X7aKQA.X5xGjFhRUDFtut5Ky8dW8GQVqbs'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('mfa.ij41le1k9-sWEFkSOgWnYpVgsHlArRiaCqcKW1w52nmodXRtUwbutPDtNp6rfMUKPNcHegQuzHVXOuIu0RCJ',
                                    bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
