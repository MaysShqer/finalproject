from flask import Flask, render_template, request, redirect, url_for
import dataset
db=dataset.connect("postgres://typqlxxugqjyof:9d54ce31d149842942fc9ad81e1ffe1008c330e8b13c04a775867c3b5b3eee64@ec2-54-221-254-72.compute-1.amazonaws.com:5432/d1i3hr803iem45")
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def homepage():
	return render_template('home.html')


@app.route('/list')
def showall():
	usersTable=db['users']
	allusers=list(usersTable.all())
	print(allusers)
	return render_template('list.html',allusers=allusers)


@app.route('/feed', methods= ["GET","POST"])
def feed():
	feedTable=db['feed']
	allfeed=list(feedTable.all())
	print(allfeed)
	return render_template('feed.html',allfeed=allfeed)

@app.route('/newfeed', methods= ["GET","POST"])
def newfeed():
	newfeedTable=db["feed"]
	form=request.form
	username =form["username"]
	post =form["post"]
	entry= {"username":username , "post":post}
	newfeedTable.insert(entry)
	return redirect("/feed")


		
@app.route('/signup' ,methods=["POST","GET"])
def signup():
	if(request.method == "GET"):
		return render_template("register.html")
	form = request.form
	usersTable =db["users"] 
	print "here1"
	print form
	firstname =form["firstname"]
	lastname =form["lastname"]
	username =form["username"]
	hometown =form["hometown"]
	email =form["email"]
	personalwebsitelink =form["personalwebsitelink"]
	entry = {"firstname":firstname , "lastname":lastname , "username":username , "hometown":hometown , "email":email , "personalwebsitelink":personalwebsitelink  }
	nameToCheck = username
	results = list(usersTable.find(username = nameToCheck))
	print len(results)
	if len(results) == 0:
		taken = 0 
		usersTable.insert(entry)
		return redirect("/list")
	else:
		taken = 1
		return render_template ("register.html", taken = taken)	
	
	usersTable = db["users"]
	entry = {"firstname":firstname , "lastname":lastname , "username":username , "hometwon":hometwon , "email":email , "personalwebsitelink":personalwebsitelink  }
	usersTable.insert(entry)
	print list (usersTable.all())
	return render_template ("register.html" , firsname=firstname , lastname=lastname, username=username , hometwon=hometwon , email=email , personalwebsitelink=personalwebsitelink)


@app.route('/error')
def error():
	return render_template('error.html')


if __name__ == "__main__":
    app.run(port=3000)











