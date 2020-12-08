from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#function to create a random alphanumberic string for the domain
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    vanity = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class Email(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    vanity = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Email %r>' % self.email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generateWithoutEmail')
def generateQuickList():
    db.create_all()
    redirectString = get_random_alphanumeric_string(8)
    return redirect(redirectString)

@app.route('/generateWithEmail', methods=['POST'])
def generateWillyList():
    email_content = request.form['emailtest']
    vanity = get_random_alphanumeric_string(8)
    new_email = Email(email=email_content, vanity=vanity)
    try:
        db.session.add(new_email)
        db.session.commit()
        redirectString = '/' + vanity
        return redirect(redirectString)
    except:
        return 'There was an issue with your email address'

@app.route('/<string:vanity>', methods=['POST', 'GET'])
def display(vanity):
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, vanity=vanity)
        try:
            db.session.add(new_task)
            db.session.commit()
            redirectString = '/' + vanity
            return redirect(redirectString)
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.filter_by(vanity=vanity).all()
        return render_template('showlist.html', vanity=vanity, tasks=tasks)

@app.route('/delete/<int:id>/<string:vanity>')
def delete(id, vanity):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        redirectString = '/' + vanity
        return redirect(redirectString)
    except:
        return 'There was a problem deleting that task'

if __name__ == "__main__":
    app.run(debug=True)
