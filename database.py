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
        dialog text,
        status text 
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
    cursor.execute("insert into posts values ("+str(post_id)+",'"+text+"','"+dialog+"','"+time+"','status')")
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
    test_id = cursor.fetchall()[-1][0]
    cursor.execute("SELECT * FROM posts where id="+str(test_id))
    res = cursor.fetchall()
    connect.close()
    text = res[0][1]
    attachments = get_attachment(res[0][0])
    post = {
        "text":text,
        "attachments":attachments
    }
    return post

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

def get_db(table):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM "+table)
    result = cursor.fetchall()
    connect.close()
    return result