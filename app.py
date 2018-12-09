from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.github import make_github_blueprint, github
import feedparser

app = Flask(__name__)

app.config['SECRET_KEY'] = 'lablam.2017.lablam'

github_blueprint = make_github_blueprint(client_id ='f535b5151e041282efaf', client_secret ='8f7167dec44b205393243b7f830c49f6f57e1d2d')

app.register_blueprint(github_blueprint, url_prefix='/login')     


RSS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
       'cnn': 'http://rss.cnn.com/rss/edition.rss'}  

@app.route("/")
def github_login():

    if not github.authorized:
        return redirect(url_for("github.login"))

    account_info=github.get("/user")

    if account_info.ok:
	return redirect(url_for("news", publication="bbc"))

    return "request failed"    


@app.route("/<publication>")
def news(publication="bbc"):
          feed = feedparser.parse(RSS[publication])
          current_article = feed['entries'][0]
          return render_template("home.html", current_article=current_article)

 
if __name__ == '__main__':  
	app.run(port=5000, debug=True)