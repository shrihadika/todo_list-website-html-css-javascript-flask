# app.py

# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    SrNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SrNo} - {self.title}"
    
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
        
      # Get the value of the search query parameter

    allTodo = Todo.query.all()
    
    
    # for search result
    
    query = request.args.get('search')

    # Check if a search query is present
    if query:
        # Use SQLAlchemy's `ilike` for case-insensitive search
        allTodo = Todo.query.filter(or_(Todo.title.ilike(f"%{query}%"), Todo.desc.ilike(f"%{query}%"))).all()
    else:
        # If no search query, get all todos
        allTodo = Todo.query.all()

    return render_template('index.html', allTodo=allTodo, query=query)

    #end of search result 




@app.route('/update/<int:SrNo>', methods=['GET', 'POST'])
def update(SrNo):
    print(f"Entered update route for SrNo: {SrNo}")
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo.query.filter_by(SrNo=SrNo).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()  # Commit the changes directly
        return redirect("/")

    todo = Todo.query.filter_by(SrNo=SrNo).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:SrNo>')
def delete(SrNo):
    print(f"Entered delete route for SrNo: {SrNo}")
    todo = Todo.query.filter_by(SrNo=SrNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# searching start 
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    if not query:
        return redirect('/')

    # Use SQLAlchemy's `ilike` for case-insensitive search
    search_results = Todo.query.filter(or_(Todo.title.ilike(f"%{query}%"), Todo.desc.ilike(f"%{query}%"))).all()
    
    return render_template('index.html', allTodo=search_results, query=query)

# end of searching

if __name__ == "__main__":
    app.run(debug=True)
