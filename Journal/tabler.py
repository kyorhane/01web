import sqlite3

# SELECT sql FROM sqlite_master WHERE name = 'users'; 
# Use the above query to check the structure of a table from command palette
# Or use "open database" query to open tab in the explorer

with sqlite3.connect("story.db") as storydb:
    db = storydb.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        username VARCHAR(255) NOT NULL, 
        password VARCHAR(255) NOT NULL, 
        hash VARCHAR(255) NOT NULL
    )
    """)

with sqlite3.connect("story.db") as storydb:
    db = storydb.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS gallery (
        user_id INTERGER NOT NULL,
        img1 DEFAULT "https://images.unsplash.com/photo-1600282408787-b8025eef26b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60",
        img2 DEFAULT "https://images.unsplash.com/photo-1600282408787-b8025eef26b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60",
        img3 DEFAULT "https://images.unsplash.com/photo-1600282408787-b8025eef26b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60",
        img4 DEFAULT "https://images.unsplash.com/photo-1600282408787-b8025eef26b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60",
        img5 DEFAULT "https://images.unsplash.com/photo-1600282408787-b8025eef26b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60",
        img6 DEFAULT "https://images.unsplash.com/photo-1600282408787-b8025eef26b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60",
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)


with sqlite3.connect("story.db") as storydb:
    db = storydb.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS xjumbo (
        user_id INTEGER NOT NULL, xjumboBG VARCHAR(255) NOT NULL,
        xjumboIMG1 VARCHAR(255) NOT NULL, xjumboIMG2 VARCHAR(255) NOT NULL, xjumboIMG3 VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

with sqlite3.connect("story.db") as storydb:
    db = storydb.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS yzjumbo (
        user_id INTEGER NOT NULL,
        yjumboBG VARCHAR(255) NOT NULL, zjumboBG VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

with sqlite3.connect("story.db") as storydb:
    db = storydb.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS txtjumbo (
        user_id INTEGER NOT NULL, 
        xtxtH DEFAULT "Hello, X!",
        xtxtP1 DEFAULT "This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.",
        xtxtP2 DEFAULT "It uses utility classes for typography and spacing to space content out within the larger container.",
        ytxtH DEFAULT "Hello, Y!",
        ytxtP1 DEFAULT "This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.",
        ytxtP2 DEFAULT "It uses utility classes for typography and spacing to space content out within the larger container.",
        ztxtH DEFAULT "Hello, Z!",
        ztxtP1 DEFAULT "This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.",
        ztxtP2 DEFAULT "It uses utility classes for typography and spacing to space content out within the larger container.",
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)