from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "🔑1"

app.permanent_session_lifetime = timedelta(minutes = 4.20) # (weeks = intValue, days = 30 [DEFAULT], hours, minutes, seconds, milliseconds, microseconds)

NO_VALUE = "-⛔-"

@app.route("/")
def home():
	user = None
	if "userinfo" in session:
		user = session["userinfo"]
	return render_template("index.html", user = user)
	# return render_template("index.html", content="Testing the homepage template", title="Test.")
	# TODO: figure out the ** syntax, likely like {...spread} return render_template("index.html", {content: "Testing the homepage template", title: "Test."})
	# return render_template("./index.html")

# @app.route("/<name>")
# def user(name):
# 	return f"Hello, {name}..."

# @app.route("/admin/") # ending "/" means BOTH will work, a good idea in general for routes
# def admin():
# 	return redirect(url_for("user", name="*AdMiN*"))

# @app.route("/login") # default is to ONLY allow GET method!
@app.route("/login", methods=["pOsT", "GET"]) # unlisted method => 405 METHOD NOT ALLOWED
def login():
	if request.method == "POST":
		session.permanent = True
		user = request.form["nm"]
		print(">>> login: POSTed user=[" + user + "]<<<")
		session["userinfo"] = user
		flash(f"Login successful, {user}.", "info")
		return redirect(url_for("user"))
	else:
		print(">>>not posted - should be GET:" + request.method)
		if "userinfo" in session:
			print(">>> login: redirect to /user <<<")
			# flash("You are already logged in, " + session["userinfo"] + "!", "warn")
			flash(f"""You are already logged in, {session["userinfo"]}!""", "warn")
			return redirect(url_for("user"))
		return render_template("login.html")

# @app.route("/<usr>/")
# def user(usr):
@app.route("/user")
def user():
	if "userinfo" in session:
		user = session["userinfo"]
		return render_template("user.html", user = user)
	else:
		flash(f"You must first log in!", "error")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():

	# who_was_it = NO_VALUE
	# if "userinfo" in session:
	# 	who_was_it = session.pop("userinfo", None)
	who_was_it = session.pop("userinfo", NO_VALUE)

	print(">>> logout: who_was_it=[" + who_was_it + "]<<<") # "A" + None + "B" will FAIL: TypeError: can only concatenate str (not "NoneType") to str
	if who_was_it != NO_VALUE:
		flash(f"See you later, {who_was_it}; you have been logged out.", "info")

	return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug = True)
