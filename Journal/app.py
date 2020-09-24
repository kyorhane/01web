import os
import datetime
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, check

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# now = datetime.datetime.now()
# time = now.strftime("%a -" + "%b -" + "%Y -" + "%Hh -" + "%Mm -" + "%Ss")

@app.route("/")
@login_required
def index():
    with sqlite3.connect('story.db') as story:
        db = story.cursor()
        db.execute("SELECT * FROM gallery JOIN users ON gallery.user_id = users.id WHERE user_id=:user_id", {'user_id': session['user_id']})
        # imgcounter = db.fetchall()
        # print(f'index {imgcounter}')
        div1 = renderIndex("img1", "one") + "XXX</a></div>"
        div2 = renderIndex("img2", "two") + "XXX</a></div>"
        div3 = renderIndex("img3", "three") + "YYY</a></div>"
        div4 = renderIndex("img4", "four") + "YYY</a></div>"
        div5 = renderIndex("img5", "five") + "ZZZ</a></div>"
        div6 = renderIndex("img6", "six") + "ZZZ</a></div>"
        # print("printed div6 here for the sake of testing: " + div6)
        return render_template("index.html", div1 = div1, div2 = div2, div3 = div3, div4 = div4, div5 = div5, div6 = div6)

@app.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "POST":
            with sqlite3.connect("story.db") as storydb:
                db = storydb.cursor()
                username = check("username")
                password = check("password")
                if len(password) < 8:
                    return apology("Short password.")
                hashed = generate_password_hash(password)
                confirmation = check("confirmation")
                if confirmation != password:
                    return apology("Passwords do not match.")
                
                db.execute("SELECT * FROM users WHERE username = :username", {'username': username})
                checkexist = db.fetchall()
                print("name appears here if the it exists " + str(checkexist))
                if not checkexist:
                    db.execute("INSERT INTO users (username, password, hash) VALUES (:username, :password, :hash)",
                    {'username': username, 'password': password, 'hash': hashed})
                    db.execute("SELECT id FROM users WHERE username = :username", {"username": username})
                    registrantID = db.fetchone()
                    registrantID = registrantID[0]
                    print(registrantID)
                    
                    # urls for default image gallery
                    defxjumbo = "https://images.unsplash.com/photo-1600187831862-40bde7c4bfdf?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60"
                    defyzjumbo = "https://images.unsplash.com/photo-1600340145666-bc8292e2266c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60"
                    
                    db.execute("""INSERT INTO gallery (user_id)
                                VALUES (:user_id)""",
                                {"user_id": registrantID})
                    db.execute("""INSERT INTO xjumbo (user_id, xjumboBG, xjumboIMG1, xjumboIMG2, xjumboIMG3)
                                VALUES (:user_id, :imgdef, :imgdef, :imgdef, :imgdef)""",
                                {"user_id": registrantID, "imgdef": defxjumbo})
                    db.execute("""INSERT INTO yzjumbo (user_id, yjumboBG, zjumboBG)
                                VALUES (:user_id, :imgdef, :imgdef)""",
                                {"user_id": registrantID, "imgdef": defyzjumbo})
                    db.execute("""INSERT INTO txtjumbo (user_id)
                                VALUES (:user_id)""",
                                {"user_id": registrantID})
                    return redirect("/")
                else:
                    return apology("Username already exists.")
        else:    
            return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    with sqlite3.connect("story.db") as storydb:
        db = storydb.cursor()

        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":

            # Ensure username was submitted
            username = check("username")

            # Ensure password was submitted
            password = check("password")

            # Query database for username
            db.execute("SELECT * FROM users WHERE username = :username",
                            {'username': username})
            
            rows = db.fetchall()
            print(f'login {rows}')

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0][3], password):
                return apology("invalid username and/or password", 403)

            # Remember which user has logged in
            session["user_id"] = rows[0][0]

            # Redirect user to home page
            return redirect("/")
        else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/x", methods=["GET", "POST"])
@login_required
def x():
    if request.method == 'GET':
        xbgcall = renderIndex('xjumboBG')
        # print(str(xbgcall) + " is xbg0")
        txtcall = f"""<div class="container">
            <h1 class="display-4">{rendertxt('xtxtH')}</h1>
            <p class="lead">{rendertxt('xtxtP1')}</p>
            <hr class="my-4">
            <p>{rendertxt('xtxtP2')}</p>
            <button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#modaltxt">Edit</button></div></div>"""
        xbg = xbgcall + txtcall 
        # print(xbg + " is the final result of xbg")
        ximg1 = renderIndex('xjumboIMG1')
        ximg2 = renderIndex('xjumboIMG2')
        ximg3 = renderIndex('xjumboIMG3')
        return render_template("x.html", xbg = xbg, ximg1 = ximg1, ximg2 = ximg2, ximg3 = ximg3)
    else:
        this_col = check('txtColumn')
        this_val = check('modaltxt')
        # print(this_val + this_col + " is this request's value and column")
        updateText(this_col, this_val)
        return redirect("/x")

@app.route("/y", methods=["GET", "POST"])
@login_required
def y():
    if request.method == "GET":
        ybgcall =  renderIndex('yjumboBG')
        ybg = ybgcall + f"""<div class='container'>
        <h1 class='display-4'>{rendertxt('ytxtH')}</h1>
        <p class='lead'>{rendertxt('ytxtP1')}</p>
        <hr class='my-4'><p>{rendertxt('ytxtP2')}</p><button class='btn btn-primary btn-sm' data-toggle="modal" data-target="#modaltxt">Edit</button></div></div>"""
        ybox1 = simpleRender('img3')
        ybox2 = simpleRender('img4')
        return render_template("y.html", ybg=ybg, ybox1=ybox1, ybox2=ybox2)
    else:
        this_col = check('txtColumn')
        this_val = check('modaltxt')
        updateText(this_col, this_val)
        return redirect("/y")

@app.route("/z", methods=["GET", "POST"])
@login_required
def z():
    if request.method == "GET":
        zbgcall =  renderIndex('zjumboBG')
        zbg = zbgcall + f"""<div class='container'>
        <h1 class='display-4'>{rendertxt('ztxtH')}</h1>
        <p class='lead'>{rendertxt('ztxtP1')}</p>
        <hr class='my-4'><p>{rendertxt('ztxtP2')}</p><button class='btn btn-primary btn-sm' data-toggle="modal" data-target="#modaltxt">Edit</button></div></div>"""
        zbox1 = simpleRender('img5')
        zbox2 = simpleRender('img6')
        return render_template("z.html", zbg=zbg, zbox1=zbox1, zbox2=zbox2)
    else:
        thisCol = check('txtColumn')
        thisVal = check('modaltxt')
        updateText(thisCol, thisVal)
        return redirect("/z")

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        galleryIndex = check("gallery")
        # print(f'gallery index is {galleryIndex}')
        url = check("imgurl")
        # print(f'url is {url}')
        updateCol(galleryIndex, url)
        return redirect("/upload")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

def updateCol(this, url):
    """Update img column in gallery table"""
    if this in ['Gallery 1', 'Gallery 2', 'Gallery 3', 'Gallery 4', 'Gallery 5', 'Gallery 6']:
        for x in this:
            if x.isdigit():
                col_id = "img" + str(x)
        with sqlite3.connect("story.db") as storydb:
            db = storydb.cursor()
            try:
                sql = f"""UPDATE gallery SET ({col_id}) = (:url) WHERE user_id = :user_id"""
                # print(sql)
                db.execute(sql, {"url": url, "user_id": session['user_id']})
                return True
            except:
                return apology("There has been a gallery error!")
    elif this in ['xjumboBG', 'xjumboIMG1', 'xjumboIMG2', 'xjumboIMG3']:
        with sqlite3.connect("story.db") as storydb:
            db = storydb.cursor()
            try:
                sql = f"""UPDATE xjumbo SET ({this}) = (:url) WHERE user_id = :user_id"""
                # print(sql)
                db.execute(sql, {"url": url, "user_id": session['user_id']})
                return True
            except:
                return apology("There has been an xjumbo error!")
    elif this in ['yjumboBG', 'zjumboBG']:
        with sqlite3.connect("story.db") as storydb:
            db = storydb.cursor()
            try:
                sql = f"""UPDATE yzjumbo SET ({this}) = (:url) WHERE user_id = :user_id"""
                # print(sql)
                db.execute(sql, {"url": url, "user_id": session['user_id']})
                return True
            except:
                return apology("There has been a yzjumbo error!")

def renderIndex(imgID, col_id_str=None):
    if imgID in ['img1', 'img2', 'img3', 'img4', 'img5', 'img6']:
        try:
            if col_id_str not in ['one', 'two', 'three', 'four', 'five', 'six']:
                return apology("There's only 6 columns, chief!")
            else:
                col_id_str = "\'" + col_id_str + "\'"
                url = openDbUrl(imgID, 'gallery')
                # columnRendered = f"<div class='gallery border border-dark' id={col_id_str} style='background-image: url({url});'><a href='{url}'>XXX</a></div>"
                columnRendered = f"<div class='gallery border border-dark' id={col_id_str} style='background-image: url({url});'><a href='{url}'>"
                return columnRendered
        except:
            return apology("Something went wrong while rendering za page, chief.")
    elif imgID in ['xjumboBG', 'xjumboIMG1', 'xjumboIMG2', 'xjumboIMG3']:
        try:
            url = openDbUrl(imgID, 'xjumbo')
            if imgID == 'xjumboBG':
                columnRendered = f"<div class='jumbotron jumbotron-fluid xjumbo' style='background-image: url({url}); color: DarkRed;'>"
            else:
                columnRendered = f"<img src={url} class='mb-2 img-fluid' alt='image can't be loaded right now'>"
            # print("Which columnRendered was that? This sir is - " + columnRendered)
            return columnRendered
        except:
            return apology("Something went wrong while rendering xjumbo!")
    elif imgID in ['yjumboBG', 'zjumboBG']:
        try:
            url = openDbUrl(imgID, 'yzjumbo')
            if imgID == 'yjumboBG':
                columnRendered = f"<div class='jumbotron jumbotron-fluid yjumbo' style='background-image: url({url}); color: Fuchsia;'>"
            else:
                columnRendered = f"<div class='jumbotron jumbotron-fluid zjumbo' style='background-image: url({url}); color: Gold;'>"
            # print("Which columnRendered was that? This sir - " + columnRendered)
            return columnRendered
        except:
            return apology("Something went wrong while rendering yzjumbo!")
    else:
        return apology("Not an accepted imgID.")

def rendertxt (txtID):
    try:
        with sqlite3.connect("story.db") as storydb:
            db = storydb.cursor()
            sql = f"SELECT ({txtID}) FROM txtjumbo WHERE user_id = :user_id"
            db.execute(sql, {"user_id": session['user_id']})
            txtresult = db.fetchone()
            # print(txtresult[0] + " is the result of rendertxt")
            return txtresult[0]
    except:
        return apology("Something went wrong while rendering jumbo text!")

def updateText (this_col, this_val):
    # print(this_col, this_val)
    try:
        with sqlite3.connect("story.db") as storydb:
            db = storydb.cursor()
            sql = f"UPDATE txtjumbo SET ({this_col}) = (:this_val) WHERE user_id = :user_id"
            db.execute(sql, {"this_val": this_val, "user_id": session['user_id']})
            return True
    except:
        return apology("Oh no, we weren't able to change the text. Try again!")

def simpleRender (col):
        try:
            url = openDbUrl(col, 'gallery')
            columnRendered = f"<img src={url} class='m-1 img-fluid' style='max-width: 480px; height: auto;' alt='image can't be loaded right now'>"
            return columnRendered
        except:
            return apology("Something went wrong while rendering yzboxes!")

def openDbUrl (col, table):
    with sqlite3.connect("story.db") as storydb:
                db = storydb.cursor()
                sql = f"SELECT ({col}) FROM {table} WHERE user_id = :user_id"
                db.execute(sql, {"user_id": session['user_id']})
                url_results = db.fetchone()
                # print("These are url_results for imgID in yzjumbo: " + url_results[0])
                url = url_results[0]
                return url