from telethon import TelegramClient, events
from telethon.tl.custom import Button
from pymongo import MongoClient
import random
api_id = 8086441
api_hash = '2a305482a93b5a762d2acd4be90dd00f'
client = TelegramClient('doz', api_id, api_hash)
client.start(bot_token='7846955302:AAH29W8_DElo7ZwlhH-F2X7o96nvwY_Ec5k')
mongo_client=MongoClient()


def create_board_buttons(board):
    return [
        [
            Button.inline(board[0] if board[0] != '_' else "", "0"),
            Button.inline(board[1] if board[1] != '_' else "", "1"),
            Button.inline(board[2] if board[2] != '_' else "", "2"),
        ],
        [
            Button.inline(board[3] if board[3] != '_' else "", "3"),
            Button.inline(board[4] if board[4] != '_' else "", "4"),
            Button.inline(board[5] if board[5] != '_' else "", "5"),
        ],
        [
            Button.inline(board[6] if board[6] != '_' else "", "6"),
            Button.inline(board[7] if board[7] != '_' else "", "7"),
            Button.inline(board[8] if board[8] != '_' else "", "8"),
        ],
    ]

def check_winner(board, symbol):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],   
        [0, 4, 8], [2, 4, 6]             
    ]
    return any(all(board[i] == symbol for i in condition) for condition in win_conditions)


@client.on(events.NewMessage())
async def handler(event):
    dokme = [[Button.inline("بازی گل", "flower"),Button.inline("سنگ","rock") ,Button.inline("بازی دوز", "dooz")]]
    sender = await event.get_sender()
    sender_id = event.sender.username

    if event.message.message == '/start':
        sender = await event.get_sender()
        user_name = event.sender.first_name
# id bande khoda sender id 
        sender_id=event.sender.username
        player_exist = mongo_client.doooz.players.find_one({'id': event.message.peer_id.user_id, 'score': 0,'name':sender_id})
        players_lederbord = mongo_client.doooz.players.find({}).sort("score", -1).limit(5)
        top_players = ''
        for i in players_lederbord:
            top_players = top_players+str(i.get('name')) + '\n'
        if not player_exist:
            mongo_client.doooz.players.insert_one({'id': event.message.peer_id.user_id, 'score': 0,'name':sender_id,'turn':'player'})
        players = mongo_client.doooz.players.find({'name':sender_id})
#bayad matn reply shode taghir kone
        await event.reply('سلام'+str(sender_id)+'خوش اومدی، یکی از بازی هارو انتخاب کن و سعی کن بیشترین امیازو بدست بیاری 🔥 نفرات برتر:\n'+str(top_players)+'انتخاب کن :',
                                  buttons=dokme)



@client.on(events.CallbackQuery(pattern="rock"))
async def handlerdss(event):
    dokme = [[Button.inline("دوست","halk"),Button.inline("بات","Gili")]]
    await event.reply('با دوستت میخوای بازی کنی یا بات؟',buttons=dokme)




@client.on(events.CallbackQuery(pattern="halk"))
async def handler10(event):
    async with client.conversation(event.sender_id) as conv:
        dokme = [
            [
                Button.inline("🪨سنگ", "iron"),
                Button.inline("📃کاغذ", "xman"),
                Button.inline("✂️قیچی","gold"),
            ],
        ]
        await conv.send_message('آیدی دوستت رو بدون @ بده:')
        id_doos = await conv.get_response()
        sender_id = event.sender.username
        mongo_client.doooz.online_game.insert_one({'id':sender_id})
        online_game = mongo_client.doooz.online_game.find_one({'id':id_doos.message})
        id2 = online_game.get('id')
        try:
            if id_doos.message ==id2:
                await conv.send_message("دوست شما وصل شد!",buttons=dokme)
        except Exception as e:
            await conv.send_message('دوست شما وصل نیست، صبر کنید...')
            return




    @client.on(events.CallbackQuery(pattern="iron"))
    async def handler110(event):
        dokme = [
            [
                Button.inline("🪨سنگ", "iron"),
                Button.inline("📃کاغذ", "xman"),
                Button.inline("✂️قیچی","gold"),
            ],
        ]        
        await event.reply('انتخاب کن',
                        buttons=dokme)
        game = 'sang'
        mongo_client.doooz.online_game.update_one({'id':sender_id},{'$set':{'entekhab':game}})
        bff = mongo_client.doooz.online_game.find_one({'id':id_doos.message})
        entekhab = bff.get('entekhab')
        if entekhab not in bff:
            await event.reply('dobare emtehan kon doostet entekhab nakarde...')
        if entekhab == game:
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score
            await event.reply(' مساوی شد 🦍 \n امتیازت: ' + str(player_new_score),buttons=dokme)
        elif entekhab =='kaghaz':
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score-3
            mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
        elif entekhab == 'gheychi':
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score+5
            mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)



    



    @client.on(events.CallbackQuery(pattern="xman"))
    async def handler120(event):
        dokme = [
            [
                Button.inline("🪨سنگ", "iron"),
                Button.inline("📃کاغذ", "xman"),
                Button.inline("✂️قیچی","gold"),
            ],
        ]        
        await event.reply('انتخاب کن',
                        buttons=dokme)
        game = 'kaghaz'

        bff = mongo_client.doooz.online_game.find_one({'id':id_doos.message})
        mongo_client.doooz.online_game.update_one({'id':sender_id},{'$set':{'entekhab':game}})
        entekhab = bff.get('entekhab')
        if entekhab not in bff:
            await event.reply('dobare emtehan kon doostet entekhab nakarde...')
        if entekhab == game:
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score
            await event.reply(' مساوی شد 🦍 \n امتیازت: ' + str(player_new_score),buttons=dokme)
        elif entekhab == 'sang':
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score+5
            mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)
        elif entekhab == 'gheychi':
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score-3
            mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    
    



    @client.on(events.CallbackQuery(pattern="gold"))
    async def handler130(event):
        dokme = [
            [
                Button.inline("🪨سنگ", "iron"),
                Button.inline("📃کاغذ", "xman"),
                Button.inline("✂️قیچی","gold"),
            ],
        ]        
        await event.reply('انتخاب کن',
                        buttons=dokme)
        game = 'gheychi'
        bff = mongo_client.doooz.online_game.find_one({'id':id_doos.message})
        mongo_client.doooz.online_game.update_one({'id':sender_id},{'$set':{'entekhab':game}})
        entekhab = bff.get('entekhab')
        if entekhab not in bff:
            await event.reply('dobare emtehan kon doostet entekhab nakarde...')
        if entekhab == game:
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score
            await event.reply(' مساوی شد 🦍 \n امتیازت: ' + str(player_new_score),buttons=dokme)
        elif entekhab == 'sang':
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score-3
            mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
        elif entekhab== 'kaghaz':
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score+5
            mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)

    





@client.on(events.CallbackQuery(pattern="Gili"))
async def call_handler12(event):
    dokme = [
        [
            Button.inline("🪨سنگ", "sigar"),
            Button.inline("📃کاغذ", "k"),
            Button.inline("✂️قیچی","gholi"),
        ],
    ]
    await event.reply('انتخاب کن',buttons=dokme)


@client.on(events.CallbackQuery(pattern="sigar"))
async def call_handler12(event):
    dokme = [
        [
            Button.inline("🪨سنگ", "sigar"),
            Button.inline("📃کاغذ", "k"),
            Button.inline("✂️قیچی","gholi"),
        ],
    ]
    bot_bazi=random.randint(1,3)
    if bot_bazi==1:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score
        await event.reply(' مساوی شد 🦍 \n  امتیازت: ' + str(player_new_score), buttons=dokme)
    elif bot_bazi==2:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score+5
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    elif bot_bazi==3:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score-3
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)



@client.on(events.CallbackQuery(pattern="k"))
async def call_handler6(event):
    dokme = [
        [
            Button.inline("🪨سنگ", "sigar"),
            Button.inline("📃کاغذ", "k"),
            Button.inline("✂️قیچی","gholi"),
        ],
    ]
    bot_bazi=random.randint(1,3)
    if bot_bazi==1:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score-3
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    elif bot_bazi==2:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score
        await event.reply(' مساوی شد 🦍 \n امتیازت: ' + str(player_new_score),buttons=dokme)
    elif bot_bazi==3:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score+5
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)


@client.on(events.CallbackQuery(pattern="gholi"))
async def call_handler(event):
    dokme = [
        [
            Button.inline("🪨سنگ", "sigar"),
            Button.inline("📃کاغذ", "k"),
            Button.inline("✂️قیچی","gholi"),
        ],
    ]
    bot_bazi=random.randint(1,3)
    if bot_bazi==1:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score+5
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    elif bot_bazi==2:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score-3
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    elif bot_bazi==3:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score
        await event.reply(' مساوی شد 🦍 \n امتیازت: ' + str(player_new_score),buttons=dokme)


@client.on(events.CallbackQuery(pattern="flower"))
async def call_handler2(event):
    dokme = [[Button.inline("بازی با بات", "friend"), Button.inline("بازی با دوست", "doost")]]
    await event.reply('انتخاب کن ربات یا دوست',buttons=dokme)

@client.on(events.CallbackQuery(pattern="doost"))
async def doost(event):
    async with client.conversation(event.sender_id) as conv:
        dokme =[[Button.inline("راست", "batman"), Button.inline("چپ", "spiderman"),]]
        await conv.send_message('آی‌دی کسی که می‌خواهید با او بازی کنید را بدون @ وارد کنید!')
        id_doos = await conv.get_response()
        sender_id = event.sender.username
        mongo_client.doooz.online_game.insert_one({'id':sender_id})
        online_game = mongo_client.doooz.online_game.find_one({'id':id_doos.message})
        id2 = online_game.get('id')
        try:

            if id_doos.message!=id2:
                await conv.send_message('دوست شما وصل شد!\nانتخاب کنید',buttons=dokme)
                return
        except Exception as e:

            await conv.send_message('دوست شما وصل نیست، صبر کنید...')
            return




    @client.on(events.CallbackQuery(pattern="batman"))
    async def call_handler_gol_r_d(event):
        dokme =  [[Button.inline("راست", "batman"), Button.inline("چپ", "spiderman")]]
        game = 'rast'
        sender_id = event.sender.username
        mongo_client.doooz.online_game.update_one({'id':sender_id},{'$set':{'entekhab':game}})
        bff = mongo_client.doooz.online_game.find_one({'id':id_doos.message})
        entekhab = bff.get('entekhab')
        if entekhab not in bff:
            await event.reply('دوست شما انتخاب نکرده....')
        if entekhab==game:
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score+5
            players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)
            mongo_client.doooz.online_game.delete_one({'entekhab':game})
        elif entekhab!=game:
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score-3
            players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
    #be reply ezafeh she hala nobat bote
            await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
            mongo_client.doooz.online_game.delete_one({'entekhab':game})
        

                


    @client.on(events.CallbackQuery(pattern="spiderman"))
    async def call_handler_gol_r(event):
        dokme =  [[Button.inline("راست", "batman"), Button.inline("چپ", "spiderman")]]
        game = 'chap'
        sender_id = event.sender.username
        mongo_client.doooz.online_game.update_one({'id':sender_id},{'$set':{'entekhab':game}})
        bff = mongo_client.doooz.online_game.find_one({'id':id_doos.message})
        entekhab = bff.get('entekhab')
        if entekhab not in bff:
            await event.reply('dobare emtehan kon doostet entekhab nakarde...')
        if entekhab==game:
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score+5
            players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
            await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)
            mongo_client.doooz.online_game.delete_one({'entekhab':game})
        elif entekhab!=game:
            player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
            player_score = player_score.get('score')
            player_new_score=player_score-3
            mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
    #be reply ezafeh she hala nobat bote
            await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
            mongo_client.doooz.online_game.delete_one({'entekhab':game})
        
            
    
@client.on(events.CallbackQuery(pattern="friend"))
async def call_handler_gol(event):
    dokme =[[Button.inline("راست", "rast"), Button.inline("چپ", "c")]]
    await event.reply('تو دست راست یا چپ؟ ',
                              buttons=dokme)


@client.on(events.CallbackQuery(pattern="rast"))
async def call_handler_gol_r(event):
    dokme =  [[Button.inline("راست", "rast"), Button.inline("چپ", "c")]]
    bot=random.randint(1,2)
    if bot==1:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score-3
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
    #be reply ezafeh she hala nobat bote
        await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    elif bot==2:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score+5
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    

@client.on(events.CallbackQuery(pattern="c"))
async def call_handler_gol_c(event):
    dokme =  [[Button.inline("راست", "rast"), Button.inline("چپ", "c")]]
    bot=random.randint(1,2)
    if bot==1:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score-3
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
    #be reply ezafeh she hala nobat bote
        await event.reply(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    elif bot==2:
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score+5
        players=mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.reply(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=dokme)
    
# system emtiaz va if not game bayad dorost beshan
@client.on(events.CallbackQuery(pattern="dooz"))
async def call_handler2(event):
    dokme = [[Button.inline("بازی با بات", "b"), Button.inline("بازی با دوست", "d")]]

    await event.reply('انتخاب کن',buttons=dokme)



@client.on(events.CallbackQuery(pattern="b"))
async def call_handler3(event):
    sender_id = event.sender.username
    board = ['_'] * 9  


    mongo_client.doooz.games.update_one(
        {'sender_id': sender_id},
        {'$set': {'board': board, 'turn': 'player'}},
        upsert=True
    )


    dokme = create_board_buttons(board)
    await event.reply('نوبت توعه 🫵', buttons=dokme)


@client.on(events.CallbackQuery(pattern=r"^\d$"))
async def player_move(event):
    sender_id = event.sender.username
    

    move = int(event.data.decode())
    game = mongo_client.doooz.games.find_one({'sender_id':sender_id})
    if not game:
        await event.reply("بازی‌ای پیدا نشد. لطفاً دوباره با /start شروع کنید.")
        return
    
    turn = game['turn']
    board = game['board']
    if turn !='player':
        await event.answer('nobat robote!', alert = True)
        return
    elif board[move] != '_':
        await event.answer("این خانه پره! جای دیگه‌ای انتخاب کن.", alert=True)
        return
    board[move] = 'X'
    mongo_client.doooz.games.update_one(
        {'sender_id':sender_id },
        {'$set': {'board': board, 'turn': 'bot'}}
    )
    if check_winner(board, 'X'):
        buttons = create_board_buttons(board)
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score+5
        mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.edit(' بردی 🥶 5 تا امتیاز مثبت گرفتی \n امتیازت: ' + str(player_new_score),buttons=buttons)
        mongo_client.doooz.games.delete_one({'sender_id': sender_id})
        return

    if '_' not in board:
        buttons = create_board_buttons(board)
        await event.edit("😐 بازی مساوی شد!", buttons=buttons)
        mongo_client.doooz.games.delete_one({'seder_id': sender_id})
        return

    await bot_move(event, sender_id)
#
async def bot_move(event, sender_id):
    sender_id = event.sender.username
    game = mongo_client.doooz.games.find_one({'sender_id': sender_id})
    board = game['board']

    empty_cells = [i for i, cell in enumerate(board) if cell == '_']
    bot_move = random.choice(empty_cells)
    board[bot_move] = 'O'

    
    mongo_client.doooz.games.update_one(
        {'sender_id': sender_id},
        {'$set': {'board': board, 'turn': 'player'}}
    )

    
    if check_winner(board, 'O'):
        buttons = create_board_buttons(board)
        mongo_client.doooz.games.delete_one({'sender_id': sender_id})
        player_score=mongo_client.doooz.players.find_one({'id':event.query.user_id})
        player_score = player_score.get('score')
        player_new_score=player_score-3
        mongo_client.doooz.players.update_one({'id':event.query.user_id},{'$set':{'score':player_new_score}})
        await event.edit(' باختی بدبخت🤣 3 تا امتیاز از دست دادی \n امتیازت: ' + str(player_new_score),buttons=buttons)

        return

    if '_' not in board:
        buttons = create_board_buttons(board)
        await event.edit("😐 بازی مساوی شد!", buttons=buttons)
        mongo_client.doooz.games.delete_one({'sender_id':sender_id})
        return

    buttons = create_board_buttons(board)
    await event.edit("نوبت توئه! حرکت بعدی رو انتخاب کن:", buttons=buttons)



                

client.run_until_disconnected()


