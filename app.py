from flask import Flask, render_template, request, redirect
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Simple Todos")


@app.route('/enternew')
def new_todo():
   return render_template('todo_form.html')

@app.route('/createtodo',methods = ['POST', 'GET'])
def createtodo():
   if request.method == 'POST':
      try:
         description = request.form['description']
         due_date = request.form['due_date']
         status = request.form['status']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO todos(description,due_date,status) VALUES (?,?,?)",(description,due_date,status))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "Error in insert operation"
      
      finally:
         return redirect("list")
         con.close()

@app.route('/deletetodo',methods = ['POST', 'GET'])
def deletetodo():
   if request.method == 'POST':
      try:
         rowid = request.form['rowid']
                 
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("DELETE FROM todos WHERE rowid=?",(rowid))
            
            con.commit()
            msg = "Task succesfully delete"
      except:
         con.rollback()
         msg = "Error in deleting task"
      
      finally:
         return redirect("list")
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select rowid,description,due_date,status from todos")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
