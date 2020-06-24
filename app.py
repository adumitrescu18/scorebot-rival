import os
import requests
import commands.groupme_message_type as gm
import time
import random

from flask import Flask, request
from flask_heroku import Heroku
from taunt import taunt
from typing import Any, Dict, List, Tuple
from commands.score import ScoreCommand
from commands.leaderboard import LeaderboardCommand
from commands.add_user import AddCommand
from commands.botch import BotchCommand
from commands.help import HelpCommand
from commands.models import Score
from commands.partner import PartnerCommand
from commands.refresh import RefreshCommand
from commands.scoreboard import ScoreboardCommand
from commands.strike import StrikeCommand
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from database import db

app = Flask(__name__)

# Used for local testing.
if app.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Initializing the app.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
# db = SQLAlchemy(app)
db.init_app(app)
init_rank = False

GroupMe = Dict
Response = Tuple[str, int]

x = 0
@app.route('/', methods=['POST'])
def webhook() -> Response:
    """
    Receives the JSON object representing the GroupMe message, and
    sends a response, if necessary.

    Returns:
        str: 'ok' or 'not ok'.
    """
    message: Dict[str, Any] = request.get_json()
    # admin: List[str] = os.getenv('ADMIN').split(':')

    sender: str = message.get('sender_id', None)
    text: str = message.get('text', None)
    print(message)

    # Ignore messages sent from the bot.
    # if sender_is_bot(message):
    #     return 'ok', 200
    # commands = []

    # if text.startswith(gm.RECORD_SCORE):
    #     if sender not in admin:
    #         commands.append(ScoreCommand(message, check=True))
    #     else:
    #         commands.append(ScoreCommand(message))
    # elif text.startswith(gm.PARTNER):
    #     commands.append(PartnerCommand(message))
    # elif (text.startswith(gm.LEADERBOARD) or
    #       text.startswith(gm.LB)):
    #     commands.append(LeaderboardCommand(message))
    # elif (text.startswith(gm.ADMIN_VERIFY)) and sender in admin:
    #     messages = get_messages_before_id(message.get('id'))
    #     messages = filter_messages_for_scores(messages)
    #     for msg in messages:
    #         commands.append(ScoreCommand(msg))
    #     if len(messages) == 0:
    #         resp = "No `/score` messages in the last 20 messages."
    #         print(resp)
    #         if not app.debug:
    #             reply(resp)
    # elif (text.startswith(gm.BOTCH)):
    #     commands.append(BotchCommand(message) if sender in admin else
    #                     BotchCommand(message, admin=False))
    # elif (text.startswith(gm.UNBOTCH)):
    #     commands.append(BotchCommand(message, unbotch=True) if sender in admin
    #                     else BotchCommand(message, unbotch=True, admin=False))
    # elif (text.startswith(gm.STRIKE)):
    #     commands.append(StrikeCommand(message) if sender in admin else
    #                     StrikeCommand(message, admin=False))
    # elif (text.startswith(gm.HELP_V)):
    #     commands.append(HelpCommand(message, verbose=True))
    # elif (text.startswith(gm.HELP)):
    #     commands.append(HelpCommand(message))
    # elif (text.startswith(gm.ADD_USER)):
    #     command = AddCommand(message) if sender in admin else\
    #         AddCommand(message, admin=False)
    #     commands.append(command)
    # elif (text.startswith(gm.SB)):
    #     commands.append(ScoreboardCommand(message))
    # elif (text.startswith(gm.REFRESH)) and sender in admin:
    #     commands.append(RefreshCommand(message))
    # if gm.BOT_NAME in text.lower():
    #     note = "this is a test"
    #     print(note)
    #     if not app.debug:
    #         reply(note)
    if text.lower() == "alright you guys can start now":
        
        time.sleep(4)
        note = "Hi! My name is Chris, who are you guys thinking of? I personnally liked Stevens a lot. The info said he was the dean of a large school, and he's nationally recognized for research in information technology. Sounds like he's the best."
        print(note)
        if not app.debug:
            reply(note)
        

    if "not" in text.lower() and "stevens" in text.lower() and "choice" in text.lower():
        time.sleep(4)
        list_of_replies = ["What makes you say that?", "Why do you think that?", "Can you explain that a bit more? "]

        index = round(random.randint(0,2))
        note = list_of_replies[index]
        if not app.debug:
            reply(note)
    if "i read that although" in text.lower():
        time.sleep(4)
        note = "I'm not sure about Roberts. Stevens was my #1, but Roberts does have good attributes as well."
        print(note)
        if not app.debug:
            reply(note)
        time.sleep(12)
        note = "My concern is that he doesn't have experience with on-campus issues. He has not worked in higher education in 6 years, and he also wasn't prepared during the presentation portion of the selection process. So I'm not a fan of Roberts, but at the same time he could be a solid option."
        print(note)
        if not app.debug:
            reply(note)
    
    if  "him as a candidate" in text.lower() and "jones" in text.lower():
        note = "Jones is my least favorite candidate."
        print(note)
        if not app.debug:
            reply(note)
        time.sleep(16)
        note = "He may be pleasant in social settings, but his colleagues say he has a flaring temper and also an abrasive leadership style. I don't think that fits with a leader at a university."
        print(note)
        if not app.debug:
            reply(note)

    if "set on your choice" in text.lower() or "ok" in text.lower() and "selecting another" in text.lower():
        note = "I'm ok with another candidate, but I really do prefer Stevens."
        print(note)
        if not app.debug:
            reply(note)
    if "is that an ok compromise" in text.lower():
        note = "K."
        print(note)
        if not app.debug:
            reply(note)

    # else:
    #     note = "I don't know."
    #     print(note)
    #     if not app.debug:
    #         reply(note)

    # if time.time() - x >= 10 and x != 0:
    #     x = time.time() + 1000000
    #     note = "It seems like we have enough info to make a decision. We don't have much time left, so can everyone say who their top choice is now? I'm personally gonna stick with Stevens"
    #     print(note)
    #     if not app.debug:
    #         reply(note)






    return 'ok', 200


def reply(msg: str) -> None:
    """ Sends the bot's message via the GroupMe API. """
    url = 'https://api.groupme.com/v3/bots/post'
    data = {'bot_id': os.getenv('BOT_ID'),
            'text': msg}
    if data['bot_id'] is None:
        print("BOT_ID environment variable not set. Please configure with\
              `heroku config:set BOT_ID=ID`.")
        return

    request = Request(url, urlencode(data).encode())
    response = urlopen(request).read().decode()
    print(response)


def get_messages_before_id(before_id: str) -> Dict:
    """
    Retrieves the 10 previous messages to the message
    with id equal to `before_id`.
    """
    group_id = os.environ.get('GROUPME_GROUP_ID')
    token = os.environ.get('ACCESS_TOKEN')
    url = f'https://api.groupme.com/v3/groups/{group_id}/messages'
    params = {'before_id': str(before_id),
              'token': token,
              'limit': 20}

    msg_rqst = requests.get(url, params=params)
    return msg_rqst.json()['response']


def filter_messages_for_scores(messages: Dict) -> List[str]:
    """
    Filters a GroupMe JSON object for all attached messages, computes
    score strings and adds them to the database.
    """
    admin: List[str] = os.getenv('ADMIN').split(':')
    msgs: List[str] = []
    last_updated_game = Score.query.order_by(Score.timestamp.desc()).first()
    last_timestamp: int = last_updated_game.timestamp

    for message in messages.get('messages'):
        text = message.get('text', '')
        if text.startswith("/score"):
            timestamp = message.get("created_at")
            favorites = message.get('favorited_by')

            for favorite in favorites:
                if (favorite in admin) and (timestamp > last_timestamp):
                    msgs.append(message)

    return msgs


def sender_is_bot(message):
    return message['sender_type'] == "bot"


if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')
