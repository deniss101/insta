from instagrapi import Client
from progress.bar import IncrementalBar
import sqlite3
import time

cl = Client()
con = sqlite3.connect('insta.db')

print('Base Connected\n')


def logon():
    print('Logging in:')
    cl.login("login", "password")
    print('Done:\n')


def send():
    username = input('Username:')
    message = input('Message: ')
    user_id = cl.user_id_from_username(username)
    cl.direct_send(message, user_id)
    print('Done')


def media_hashtag():
    hashtag = input('Tag:')
    amount = int(input('Amount:'))
    cur = con.cursor()
    start = time. time()
    media = cl.hashtag_medias_recent_v1(hashtag, amount)
    bar = IncrementalBar('Получаю ID, выгружаю в базу:', max=amount, suffix='%(percent)d%%')
    cur.execute("CREATE TABLE if not exists {tab} (userid, username, userfull, current_pos, comment)".format(tab=hashtag))
    for i in range(amount):
        media_dict = media[i].dict()
        user_dict = media_dict.get('user')
        userid = (user_dict.get('pk'))
        username = (user_dict.get('username'))
        userfull = (user_dict.get('full_name'))
        cur.execute("INSERT INTO {} (userid, username, userfull) VALUES(?, ?, ?)".format(hashtag), (userid, username, userfull))
        bar.next()
    bar.finish()
    con.commit()
    cur.close()
    stop = time. time()
    print(f"\nDone in {stop - start: 0.1f} seconds")


def base():
    pass


def main():
    command = input("\nlogon(), send(user), media_hashtag() \nCommand: ")
    try:
        exec(command)
    except:
        main()
    main()


main()
