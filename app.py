from flask import Flask, render_template, request, redirect, url_for, session
import dataset
import time
db=dataset.connect("postgres://typqlxxugqjyof:9d54ce31d149842942fc9ad81e1ffe1008c330e8b13c04a775867c3b5b3eee64@ec2-54-221-254-72.compute-1.amazonaws.com:5432/d1i3hr803iem45")
app = Flask(__name__)
app.secret_key="'jaskdgjklsaldkgsfljjehkfdlekjldsjlsds'"

@app.route('/')
@app.route('/home')
def homepage():
	return render_template('home.html')
		

@app.route('/list', methods= ["GET","POST"])
def list2():
		Table=db["up"]
		alluser=list(Table.all())
		print alluser
		return render_template("list.html", alluser=alluser)

@app.route('/newfeed', methods= ["GET","POST"])
def newfeed():
	if request.method=='GET':
		newfeedTable=db['newfeeds']
		feedb=list(newfeedTable.all())[::-1]
		return render_template("feed.html", feedb=feedb)
	else:
		form = request.form
        posts = form["post"] 
        username=form["username"]   
        newfeed=db["newfeeds"]
        time_string = time.strftime('%l:%M %p on %b %d, %Y')
        entry = { "post":posts,"username":username,"time_string":time_string}
        newfeed.insert(entry)  
        feedb=list(newfeed.all())[::-1]
        return render_template("feed.html", feedb=feedb,username=username,posts=posts,time=time)

@app.route("/login", methods=['GET', 'POST'])
def login():
        if request.method == "get":
            return render_template("login.html")
        else:
            form = request.form
            username = form["username"]
            password=form["password"]
            signupTable = db["signup"]
            if len(list(signupTable.find(username=username,password=password))) > 0 :
                session['username'] = request.form['username']
                return redirect("suc")

            else:
                session['error'] =  True
                error = session['error']
                return render_template("home.html",error = error)

@app.route('/register',  methods= ['GET','POST'])
def signup():
	if request.method =="GET":
		return render_template("register.html")
	else:
		form = request.form
		firstname = form["firstname"]
		lastname = form["lastname"]
		username = form["username"]
		email = form["email"]
		password = form["password"]
		hometown = form["hometown"]
		website = form["personalwebsitelink"]
		print form
		signupTable = db["up"]
		genderr = list(signupTable.all())
		entry = {"username": username, "lastname":lastname, "email": email, "firstname": firstname, "password":password,"hometown":hometown,"website":website}
		if len(list(signupTable.find(username=username)))==0:
			session['username'] = request.form['username']
			signupTable.insert(entry)
			return render_template("login.html", email=email, firstname=firstname,lastname=lastname, username=username, password=password, hometown=hometown,website=website,genderr=genderr)
		else:
			session['error'] = True
			error = session['error']
			return render_template("register.html",error=error)

@app.route('/error')
def error():
	return render_template('error.html')


if __name__ == "__main__":
    app.run(port=3000)











