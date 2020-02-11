import sqlite3

database = 'database.sqlite'

def init_db():
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("""
    CREATE table posts (
        id integer primary key,
        message text,
        time text,
        date text,
        dialog text
    );
    """)
    cursor.execute("""
    CREATE table attachment (
        id integer primary key,
        url text,
        post_id integer,
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );
    """)
    connect.close()

def add_post(text,attachments,dialog,time):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM posts")
    try:
        post_id = str(cursor.fetchall()[-1][0] + 1)
    except:
        post_id = 1
    cursor.execute("insert into posts values ("+str(post_id)+",'"+text+"','"+dialog+"','"+time+"')")
    connect.commit()
    for attachment in attachments:
        cursor.execute("SELECT id FROM attachment")
        try:
            img_id = str(cursor.fetchall()[-1][0] + 1)
        except:
            img_id = 1
        cursor.execute("insert into attachment values ("+str(img_id)+",'"+attachment+"',"+str(post_id)+")")
        connect.commit()
    connect.close()

def get_post():
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM posts")
    # test_id = cursor.fetchall()[-1][0]
    cursor.execute("SELECT * FROM posts")
    res = cursor.fetchall()
    connect.close()
    posts = []
    for i in range(0,len(res)):
        res[i] = list(res[i])
        text = res[i][1]
        attachments = get_attachment(res[i][0])
        post = {
            "text":text,
            "attachments":attachments
        }
        posts.append(post)
    return posts

def get_attachment(post_id):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM attachment where post_id="+str(post_id))
    res = cursor.fetchall()
    connect.close()
    attachments = []
    for attachment in res:
        attachments.append(attachment[1])
    return attachments

def update_group(group):
    if group == "group2":
        dialog = 2
    elif group == "group3":
        dialog = 3
    elif group == "group4":
        dialog = 4
    elif group == "group5":
        dialog = 5
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM posts")
    last_id = cursor.fetchall()[-1][0]
    cursor.execute("UPDATE posts SET dialog="+str(dialog)+" where id="+str(last_id))
    connect.commit()
    connect.close()

def update_date(day,mounth,year):
    new_date = datetime.date(year, mounth, day)
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM posts")
    last_id = cursor.fetchall()[-1][0]
    cursor.execute("UPDATE posts SET date="+str(new_date)+" where id="+str(last_id))
    connect.commit()
    connect.close()

def update_time(time):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM posts")
    last_id = cursor.fetchall()[-1][0]
    cursor.execute("UPDATE posts SET time="+time+" where id="+str(last_id))
    connect.commit()
    connect.close()

def get_db(table):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM "+table)
    result = cursor.fetchall()
    connect.close()
    return result
