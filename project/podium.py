from flask import render_template
from project import app, mail, client, bcrypt
from flask_mail import Message
from bson.objectid import ObjectId
from datetime import datetime
from decorators import async
import gmail_config
from bson import BSON
from bson import json_util
import random
import pprint

#define user database
db = client.steppodium
users = db.users2

def mongo_sum_leaderboard():
    pipeline = [ 
        {"$unwind" : "$entry" },
        {"$group": {"_id": "$display_name", "totalsteps":{"$sum":"$entry.steps"}}},
        {"$sort": {"totalsteps":-1}},
        {"$limit":10}
    ]
    pprint.pprint(db.command('aggregate', 'users2', pipeline=pipeline))

def sum_leaderboard(category):
    leaderboard = []
    mongo_object = users.find({"entry":{"$exists": True}})
    for each in mongo_object:
        _id = each["_id"]
        step_total = sum_steps(_id)
        display = each[category]
        leaderboard.append((step_total,display))
    
    print sorted(leaderboard, reverse = True)[0:10]        

def team_email_list(team_number):
    team_list = []
    team = users.find({"team.team_number":team_number})
    for each in team:
        email = each["email"]
        team_list.append(email)
     
    print team_list
    return team_list

def make_teams():
    team_max = 5
    team_number = 1
    player_number = 1

    #find count of all players without team
    count = users.find({"password":{"$exists": True},"team":{"$exists": False}}).count()

    for each in range(count):
        random_user = users.find({"password":{"$exists": True},"team":{"$exists": False}})[random.randrange(count)]
        _id = random_user["_id"]
        #add random_user to team     
        users.update({"_id":ObjectId(_id)},{"$set":{"team.team_number":team_number,
                     "team.player_number":player_number}})
        print "team number:" + str(team_number)
        print "team player:" + str(player_number)

        #reset count of unassigned teams
        count = db.users.find({"password":{"$exists": True},"team":{"$exists": False}}).count()

        #increment team and player numbers
        if player_number == team_max:
            player_number = 1
            team_number += 1
        else:
            player_number += 1

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def sendemail(esubject, esender, erecipients, ehtml):
    msg = Message(esubject, sender = esender, recipients = erecipients)
    msg.html = ehtml
    send_async_email(app,msg)

def sendconfirm(email, user_id):
    erecipients = [email]
    esender = gmail_config.MAIL_USERNAME
    esubject = 'You are almost registered!'
    ehtml = render_template('email-premailer.html',user_id=user_id)
    sendemail(esubject, esender, erecipients, ehtml)

def send_password_link(email,user_id):
    erecipients = [email]
    esender = gmail_config.MAIL_USERNAME
    esubject = 'Password reset link.'
    ehtml = render_template('password_link.html',user_id=user_id)
    sendemail(esubject, esender, erecipients, ehtml)

def send_team_email():
    for i in range(1,8):
        team_list = team_email_list(i)
        erecipients = ["zac.demi@gmail.com","dan.k.lee.0@gmail.com"] #team_list
        esender = gmail_config.MAIL_USERNAME
        esubject = "Welcome to your team!"
        ehtml = render_template('email-new_team.html',team_number=i,team_list=team_list)
        sendemail(esubject, esender, erecipients, ehtml)

def email_exists(email):
    in_database = users.find({"email":email}).count()
    return in_database > 0

def email_registered(email):
    in_database = db.users.find({"email":email, "password":{"$exists": True}}).count()
    return in_database > 0

def unique_display(_id,field,value):
    user_display = users.find({"_id":{"$ne":ObjectId(_id)},field:value}).count()
    return user_display == 0 

def valid_password(email,password):
    user_object = users.find_one({"email":email})
    pw_hash = user_object["password"]
    return bcrypt.check_password_hash(pw_hash, password)

def insert_user(email, *args):
    users.insert({"email":email,"podium_client":"ajg"})
    user_id = return_id(email)
    sendconfirm(email,user_id)

def update_user(_id,dname,password,position,office):
    #encrypt password
    password = bcrypt.generate_password_hash(password)
    users.update({"_id":ObjectId(_id)},{"$set":{"display_name":dname,
        "password":password,"position":position,"office":office}})

def update_password(_id,password):
    password = bcrypt.generate_password_hash(password)
    users.update({"_id":ObjectId(_id)},{"$set":{"password":password}})

def add_steps(_id,steps):
    date = datetime.now()
    date = datetime.strftime(date,"%Y%m%d%H%M%S")
    users.update({"_id":ObjectId(_id)},{"$push":{"entry":{"date":date, "steps":steps}}})

def sum_steps(_id):
    stepcount = 0
    # query a list of entries from mongo
    search_object  = users.find_one({"_id":ObjectId(_id)})
    try:
        entry = search_object["entry"]
        for each in entry:
            stepcount  += each['steps']
        return stepcount
    except:
        return 0

def get_recent_steps(_id):
    # query a list of entries from mongo
    search_object  = users.find_one({"_id":ObjectId(_id)})
    entry = search_object["entry"]
    entry.reverse()
    entry = entry[0:10]
    return entry

def return_id(email):
    try:
        user_object = users.find_one({"email":email})
        user_id = user_object["_id"]
        return user_id
    except:
        return False

def return_user_object(user_id):
    user = users.find_one({"_id":ObjectId(user_id)})
    return user

