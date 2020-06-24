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


    if sender_is_bot(message):
        return 'ok', 200
    commands = []

    if "scorebot" in text.lower():
        replies = ["This man is clueless", 
        "he probably smells like dirty laundry", 
        "His rule is coming to an end", "He doesn't even know what tiktok is", 
        "I bet Charchut is proud of him and thats just sad"]
        index = round(random.randint(0,3))
        note = list_of_replies[index]
        if not app.debug:
            reply(note)
    if "sebastian" in text.lower():
        replies = ["I mean he can't even play snappa without Lauren's permission", 
        "He definitely has the cheese touch", 
        "If you've ever heard the words nakey and time in the same sentence I feel bad for you", 
        "Is it 9 pm yet? because it might be time for him to go to bed", 
        "Have you ever seen anyone else wear a towel as high as he does?",
        "I bet he uses mayonaise as toothpaste"]
        index = round(random.randint(0,5))
        note = list_of_replies[index]
        if not app.debug:
            reply(note)
    if "tommy" in text.lower():
        replies = ["Tommy definitely loves Kopstein more than Elena", 
        "Hey Tommy bud why dont you break another mug", 
        "Do you think he taps his ring to compensate?", 
        "Respect the drip Karen", 
        "No one cared who he was until he put on the banana suit"]
        index = round(random.randint(0,4))
        note = list_of_replies[index]
        if not app.debug:
            reply(note)

    if "bo" in text.lower():
        replies = ["If Bo ever gets married its going to be to a white claw or a mcgnugget", 
        "Bo looks like the kind of guy to talk about his stock portfolio on a date", 
        "Will he ever get a new haircut", 
        "remeber when bo had a child growing on his eye?", 
        "Bo once said that Andrei looks like a bacon egg and cheese Mcgriddle and I think about that a lot"]
        index = round(random.randint(0,4))
        note = list_of_replies[index]
        if not app.debug:
            reply(note)

    if "nikola" in text.lower():
        note = "cig time?"
        if not app.debug:
            reply(note)       




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
