from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import requests # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db= SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False) #ye value null nahi ho sakti
    desc = db.Column(db.String(200), nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)
    #code
    #done = db.Column(db.Boolean, default=False)
    #code
    def __repr__(self):
        return f"{self.sno} - {self.title}"
    
#import logging

# Configure logging
#logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method =="POST":
        title = request.form['title']
        desc= request.form['desc']
        task = Todo(title=title, desc=desc)
        db.session.add(task)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template('index.html',all_todo=all_todo)

@app.route('/show')
def show_todos():
    all_todo = Todo.query.all()
    print( all_todo)
    #logging.debug("Todos retrieved: %s", all_todo)
    return 'Todos retrieved!'

"""@app.route('/show')
def show_todos():
    all_todo = Todo.query.all()
    print("lets see it gets printed in terminal or not", all_todo)
    return 'Todos printed in terminal!"""

"""@app.route('/update')
def update():
    sno = request.args.get('sno')
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    all_todo = Todo.query.all()
    print( all_todo)
    #logging.debug("Todos retrieved: %s", all_todo)
    return 'Todos retrieved!'
#code for delete
@app.route('/delete/<int:sno>')"""

#HELLO
"""@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        sno = request.form['sno']
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo.query.get(sno)
        if todo:
            todo.title = title
            todo.desc = desc
            db.session.commit()
        
        return redirect('/')"""



"""@app.route('/delete', methods=['POST'])
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task.'
        """

@app.route('/delete/<int:id>')
def delete_task(id):
    try:
        task = Todo.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error=str(e))
#marking as done
@app.route('/mark_as_done/<int:sno>')
def mark_as_done(sno):
    todo = Todo.query.get_or_404(sno)
    todo.done = not todo.done  # Toggle the 'done' status
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue marking your task as done.'

with app.app_context():
    db.create_all()
    print("successfully")
   

if __name__ == '__main__':
    app.run(debug=True,port=8000)