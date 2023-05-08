import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import time
import csv
import random

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

CHANNEL_NAME = os.environ['CHANNEL_NAME']
CHANNEL_ID = None
SCORE_FILE = "score.csv"
DATA_FILE = "data.csv"
TIME_COLLECT = 0
TIME_ANNOUNCE = 10
NEGATIVE_REACTION = "-1"
SHORT_CYCLE = False

NEXT_WINNER = "n"
NEXT_ANNOUNCE = 1
NEXT_FETCH = 1
PREV_ANNOUNCE = time.time()-3600*24*5

GIFS = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODVmMGNlNjA0ZjIxNjJhNzg4NzY4MGM4ZGI0MDQzZWJiYTdiM2IyYiZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/OojQx4M3zYUOk/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmUyMDM1MjAyNTA0MjNmOWI0ZGJkZGY3NTNjNzVkMDY4M2Q0NWViZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/o7GBrAimljPyJHXM4z/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYThiZDkyZTQyMGNmMzYxZTVhN2I0Mjk5YTliODJlMjc2Y2QzYTQ5NCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/xHEf4bTL53m0g/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzNkNzllMzAxZTJlOGRhZjllNDVlOWZlNDdiZDViNDlmNDIzMWM0ZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/weR19smQUjVhm/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzNkNzllMzAxZTJlOGRhZjllNDVlOWZlNDdiZDViNDlmNDIzMWM0ZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/weR19smQUjVhm/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmJkYTRiMzYzMzMxMWZkZWE1OTVjY2IzNDZhMGI2ZDEwYzNhYWMwYSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/2UtitmPJZVDBTQPDX0/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmJkYTRiMzYzMzMxMWZkZWE1OTVjY2IzNDZhMGI2ZDEwYzNhYWMwYSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/2UtitmPJZVDBTQPDX0/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTIxMGFiOGJhNzlhN2FjZGRjOGZjMDI2ZTVjYzZkMTVhNjI2ZmFhYSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/oKcjVnEYh7DY4/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTEyMzY1ZmU1YWZmOTFjNDBjZTFlNDljZjMyZTEwZGIxOTkwNzZmOSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/fUwxLWCHe26xxAcATE/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzg2ZTgwYzU1OGJiNjAxZDZjYTM5YjNlYWJmMDI0YjBjNzhkZWNiNyZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/FnMOzdvh8M9CkSbOFi/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmVkNmQ2OTg3M2JjZTZmMzQ0NTlhOGNiYzcxOWI2OTZkNWRhMTM3NSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/hcXmpeCUuoIBMRBHyI/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWNlMzczMDczYjRlNDkyMmM1ZDY3MTQyN2U4NGE1NDU3YjAzMjQzYiZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/UTSxCoPWRbhD3Xn4rt/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmI1MGJmYzZmZGY1Nzc1ZjMzZjMzMTc5OTUzMjMwNGUyN2I0NzU4OSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/9PAHicJQZs9hYEdCfS/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjY1NDYzYmUxZDQ0YmU0OTY1YmE2ZTI0MTdlNzdkMTYwZGI4Y2FmZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/cNNZdRNDuLfH4Q3K7g/giphy.gif"]

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']


def getChannelId(CHANNEL_NAME):
    print(CHANNEL_NAME+" ...getting id")
    try:
        for result in client.conversations_list():
            for channel in result["channels"]:
                if channel["name"] == CHANNEL_NAME:
                    CHANNEL_ID = channel["id"]
                    #Print result
                    print(f"Found conversation ID: {CHANNEL_ID}")
                    return CHANNEL_ID
                    break

    except:
        print("failed to get channel id")

CHANNEL_ID = getChannelId(CHANNEL_NAME)


def setData():
    global NEXT_FETCH
    global NEXT_ANNOUNCE
    global NEXT_WINNER
    global PREV_ANNOUNCE

    with open(DATA_FILE, 'w', encoding='UTF8') as f:
        f.truncate()
        writer = csv.writer(f)
        writer.writerow( [NEXT_FETCH, NEXT_ANNOUNCE, NEXT_WINNER, PREV_ANNOUNCE] )
#    print("data set")


def getData():
    global NEXT_FETCH
    global NEXT_ANNOUNCE
    global NEXT_WINNER
    global PREV_ANNOUNCE

    if os.path.exists(DATA_FILE) != True:
        setData()
       
    with open(DATA_FILE, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        for line in reader:
            NEXT_FETCH = float(line[0])
            NEXT_ANNOUNCE = float(line[1])
            NEXT_WINNER = str(line[2])
            PREV_ANNOUNCE = float(line[3])
#    print("data read")




def getNextTime(type = 0):
    h = TIME_COLLECT
    if type>0: h = TIME_ANNOUNCE
    t = time.time() + 3600*24
    tm = time.localtime(t)
    while tm.tm_wday>4:
        t += 3600*24
        tm = time.localtime(t)

    tt = time.mktime( (tm.tm_year, tm.tm_mon, tm.tm_mday, h, 0, 0, tm.tm_wday, tm.tm_yday, tm.tm_isdst) )
#    print(time.localtime(tt))

    if SHORT_CYCLE: tt = (int(time.time()/300)+1)*300 + 60*type
    return tt



def getScores():
    scores = {}
    if os.path.exists(SCORE_FILE) != True:
        with open(SCORE_FILE, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
       
    with open(SCORE_FILE, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        for line in reader:
            scores[line[0]] = float(line[1])
#    print("scores read")

    return scores


def updateScores(scores, update, winner=True):
    for k, v in scores.items():
        if winner==False:
            scores[k] = float(scores[k])*0.9
        else:
            if k==winner: scores[k] = float(scores[k])*0.05
    for k, v in update.items():
        try: scores[k] += 0
        except: scores[k] = 0
        scores[k] += v
        if k==winner: scores[k] = float(scores[k])*0.05
        print(k+"> "+str(scores[k])+"  /+"+str(v))

    with open(SCORE_FILE, 'w', encoding='UTF8') as f:
        f.truncate()
        writer = csv.writer(f)
        for k, v in scores.items():
            v = int(v*1000)/1000
            scores[k] = v
            writer.writerow([k, v])

#    print("scores updated")
    return scores


def lottery(scores):
    sum = 0
    pick = ""
    for k, v in scores.items():
        sum += float(scores[k])
    if sum==0: return "n"
    rnd = random.triangular(0,sum)
    sum = 0
    for k, v in scores.items():
        sum += float(scores[k])
        if rnd<=sum:
            pick = k
            break
    global NEXT_WINNER
    NEXT_WINNER = pick
    return pick


def announce():
    global NEXT_WINNER
    if len(NEXT_WINNER)<2: return
    n = random.randint(0, len(GIFS)-1)
    message = [{"type": "section","text": {"type": "mrkdwn","text": ":cupcake: *Šodien foršas dienas vēlējumu loterijas uzvarētājs ir... <@"+NEXT_WINNER+">* :cupcake:\n---- sūti <@"+NEXT_WINNER+"> apsveikumu, pieminot viņu un <@"+BOT_ID+">\n---- <https://google.com|Uzzini vairāk, kā piedalīties loterijā>"}},{"type": "image","block_id": "image4","image_url": GIFS[n],"alt_text": "a gif"}]
    client.chat_postMessage(channel='#'+CHANNEL_NAME, text='', blocks=message )
    print("----- the winner is "+NEXT_WINNER+" -----")



getMessagesAgain = False

def getMessages():
    updates = {}
    others = {}

    try:
        result = client.conversations_history(
            channel=CHANNEL_ID,
            inclusive=True,
            oldest=PREV_ANNOUNCE,
            limit = 0
        )

        for m in result["messages"]:
            usr = m.get('user')
            if usr!=BOT_ID:
                mm = m.get('blocks')[0].get('elements')[0].get('elements')
                m1 = False
                m2 = False
                for mmm in mm:
                    if mmm.get('type')=="user" and mmm.get('user_id')==BOT_ID: m1 = True
                    if mmm.get('type')=="user" and mmm.get('user_id')==NEXT_WINNER: m2 = True
                
                if m1 and m2:
                    updates[usr] = 1
                    if m.get('reactions') is not None:
                        for r in m.get('reactions')[0]:
                            if(r.get('name')==NEGATIVE_REACTION): updates[usr] -= 0.2 * r.get('count')
                            else: updates[usr] += 0.1 * r.get('count')
                    if updates[usr]<0: updates[usr] = 0
                else: others[usr] = 1

        # UPDATE SCORE UPDATES HERE

        print("messages loaded")
        getMessagesAgain = False

 
    except:
        print("failed to load messages")
        getMessagesAgain = True

    if len(updates)>0:
        scores = getScores()
        scores = updateScores(scores, updates)
        winner = lottery(scores)
        scores[winner] *= 0.05
        updateScores(scores, {})
    else:
        if len(others)>0:
            scores = getScores()
            winner = lottery(others)
            scores[winner] = 0.05
            updateScores(scores, {})
            print("no greetings found. picked the winner among regular users")
        else:
            print("no activity in channel to start the lottery")

            
            
def checkTime():
    getData()

    global NEXT_FETCH
    global NEXT_ANNOUNCE
    global PREV_ANNOUNCE


    if time.time()>=NEXT_FETCH:
        getMessages()
        NEXT_FETCH = getNextTime(0)
    if time.time()>=NEXT_ANNOUNCE:
        announce()
        PREV_ANNOUNCE = NEXT_ANNOUNCE
        NEXT_ANNOUNCE = getNextTime(1)

    setData()


    
def tick():

    tt = round(max(1, min( NEXT_FETCH-time.time(), NEXT_ANNOUNCE-time.time() )))
    ttx = "winner selection"
    if NEXT_FETCH>NEXT_ANNOUNCE: ttx = "announcement"
    print(str(tt)+" sec until next "+ttx)
    time.sleep( max(2,tt/4) )

    checkTime()
    global getMessagesAgain
    if getMessagesAgain==True: getMessages()

    tick()

tick()

if __name__ == "__main__":
    app.run(debug=True)
