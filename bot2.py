
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'fetch' # change to what you need
#BOT_OWNER_ROLE_ID = "487951701827911681"
  
 
 
oot_channel_id_list =[
    "694528602586480722", #LOCO Galaxy
    "679260593005527041", #LOCO Trivia Eagle
    "675593117734535208", #LOCO Dark Trivia
    "681891490208677958", #LOCO The Best
    "681092218479575177", #LOCO Marvel
    "658225042231918603", #LOCO Trivia Nation
    "569420128794443776", #LOCO United Nation
    "694793854859083797", #LOCO Master Trivia
    "675925058094497792", #FLIPKART GALAXY
    "681891700377124906", #FLIPKART The Best
    "690524518669615185", #SwagIq Infinity
    "658225824482328586", #SwagIq Trivia Nation
    "686419754449371158", #SwagIQ Galaxy
    "690517716939046942", #Quipp QUIPP-bot
    "691340679187791872", #QUIPP Royal Trivia
    "679751812915789991", #QUIPP Dark Trivia
    "694084730022264852", #QUIPP Trivia Eagle
    "686419613898113092", #QUIPP Trivia Galaxy
    "681904686256619570", #QUIPP The Best
    "694957872081141811", #QUIPP Master Trivia
    "690524571966898196" #QUIPP Trivia Infinity
]


answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf|c)?(\?)?$', re.IGNORECASE)

apgscore = 500
nomarkscore = 350
markscore = 250

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
        print("Royal Trivia Self Bot")
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
        self.embed=discord.Embed(title="**CONNECTED TO SERVER**", description="** FINDING BEST ANSWER **", color=0xADFF2F)
        self.embed.set_author(name =' 😍 ©ROYAL TRIVIA OFFICIAL™ 🇮🇳',url=' ',icon_url='https://cdn.discordapp.com/attachments/691224840392278016/694145453570260992/IMG_20200312_174727.jpg')
        self.embed.add_field(name="Option 1", value="0", inline=False)
        self.embed.add_field(name="Option 2", value="0", inline=False)
        self.embed.add_field(name="Option 3", value="0", inline=False)
        self.embed.set_footer(text=f"𝕿𝖍𝖊 B𝖆𝖉𝖘𝖍𝖆𝖍 🇮🇳 #5776", \
            icon_url="https://cdn.discordapp.com/avatars/487951701827911681/b49466d35068ecb9fae2b53754d33b6e.png?size=256")
        self.embed.set_thumbnail(url ='https://www.gstatic.com/allo/stickers/pack-8/v5/xxhdpi/7.gif')
        # await message.add_reaction(emoji=' :white_check_mark: ')
        # await self.bot.add_reaction(embed,' :white_check_mark: ', ':x:')



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
 
        self.embed.set_field_at(0, name="**Option 1**", value="``{0}``{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="**Option 2**", value="``{0}``{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="**Option 3**", value="``{0}``{1}".format(lst_scores[2], three_check))
        if self.embed_msg is not None:
           await self.embed_msg.edit(embed=self.embed)
           await msg.add_reaction(emoji=' :white_check_mark: ')

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

        if message.content.lower() == ".":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**make ``fetch`` role and taken self** ")
            return

        if message.content.startswith('.help'):
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
    loop.create_task(bot.start('NTk5NTU3NTMyNTgyNjc0NDUz.XoTtug.jHgfvn1gt1cFbiLnhoNQ2AvlnTs'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NDg3OTUxNzAxODI3OTExNjgx.Xf4IXA.4Lg60LIjHSNyVC1iNYvJNUW9NbA',
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
