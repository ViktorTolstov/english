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
    CREATE table images (
        id integer primary key,
        img_url text,
        post_id integer,
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );
    """)
    cursor.execute("""
    CREATE table docs (
        id integer primary key,
        doc_url text,
        post_id integer,
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );
    """)
    cursor.execute("""
    CREATE table video (
        id integer primary key,
        vid_url text,
        post_id integer,
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );
    """)
    connect.close()

def add_post(text,images,docs,videos,dialog,time):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM posts")
    try:
        post_id = str(cursor.fetchall()[-1][0] + 1)
    except:
        post_id = 1
    cursor.execute("insert into posts values ("+str(post_id)+",'"+text+"','"+dialog+"','"+time+"')")
    connect.commit()
    for image in images:
        cursor.execute("SELECT id FROM images")
        try:
            img_id = str(cursor.fetchall()[-1][0] + 1)
        except:
            img_id = 1
        cursor.execute("insert into images values ("+str(img_id)+",'"+text+"',"+str(post_id)+")")
        connect.commit()
    for video in videos:
        cursor.execute("SELECT id FROM video")
        try:
            vid_id = str(cursor.fetchall()[-1][0] + 1)
        except:
            vid_id = 1
        cursor.execute("insert into video values ("+str(vid_id)+",'"+text+"',"+str(post_id)+")")
        connect.commit()
    for doc in docs:
        cursor.execute("SELECT id FROM docs")
        try:
            doc_id = str(cursor.fetchall()[-1][0] + 1)
        except:
            doc_id = 1
        cursor.execute("insert into docs values ("+str(doc_id)+",'"+text+"',"+str(post_id)+")")
        connect.commit()
    connect.close()
    print(get_db("users"))

def get_db(table):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM "+table)
    result = cursor.fetchall()
    connect.close()
    return result