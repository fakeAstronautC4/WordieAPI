#importing tools needed
from flask import Flask, render_template, flash
from flask_wtf.csrf import CSRFProtect
from forms import WordForm
import requests
import secrets
from waitress import serve
import os


#Setting up the app
app = Flask(__name__)

#Flask's session manager key
session_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = session_key

#API key n
secret_key = os.environ.get('SECRET_KEY')
csrf = CSRFProtect(app)

#######################################  ROUTES  ########################################
 
@app.route("/", methods=['GET', 'POST'])
def homepage():
    form = WordForm()
    word = None
    if form.validate_on_submit():
        word = form.word.data
        print(word)
        headers = {
        'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com',
        'X-RapidAPI-Key': secret_key
        }
        response = requests.get(f'https://wordsapiv1.p.rapidapi.com/words/{word}',headers=headers)
        if response.ok:
            data = response.json()
            try:
                definition = data['results'][0]['definition']
            except:
                flash('The word does not exist. Please try again!')
                return render_template('base.html', form=form)
            return render_template("base.html", definition=definition, form=form)
        else:
            flash('Failed to fetch definition. Please try again!')
            
    elif form.is_submitted():
        if not form.word.data:
            flash("Please enter a word")
        elif ' ' in form.word.data:
            flash("Input cannot contain spaces")
        else:
            flash("Word not found")

    return render_template('base.html', form=form)



#######################################  TRIGGER  ########################################

if __name__ == '__main__':
    
    serve(app, host='0.0.0.0', port=8080, threads = 2)