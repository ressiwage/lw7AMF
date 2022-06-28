from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random, os
import pandas as p
import numpy as np


DS = p.read_csv("energy_dataset.csv")
cat_par = DS.columns.values.tolist()[1:21]
g1 = [str(DS[i].sum()) for i in DS.columns.values.tolist()[1:21] ]


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)



class note(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    summary = db.Column(db.Float())
    

    def __repr__(self):
        return '<note %r>' % self.id



def add_sh():
    global cat_par, g1, note, db

    os.remove("lab.db")
    db.create_all()
    for i in range(len(cat_par)):
        print(cat_par[i], g1[i])
        try:
            n = note(name=cat_par[i], summary=g1[i], id=random.randint(1000000000,10000000000))
            db.session.add(n)
            db.session.commit()
        except Exception as e:
            print(str(e)+"\n")
            db.session.rollback()
            try:
                n = note(name=cat_par[i], summary=g1[i], id=random.randint(1000000000,10000000000))
                db.session.add(n)
                db.session.commit()
                print("ok!")
            except Exception as e2:
                print(str(e2)+"\n\n")
                


@app.route('/', methods=['GET', 'POST'])
def index():
    vals = "|".join(g1)
    labs = "|".join(cat_par)
    if request.method == 'POST':
        data = request.form.keys()
        for i in data:
            if i=="submit":
                vals = "|".join(g1)
                labs="|".join(cat_par)
            else:
                vals = "|".join([j for j in g1 if float(j)!=0])
                labs = "|".join([cat_par[j] for j in range(len(cat_par)) if float(g1[j])>1])
    items = note.query.order_by(note.name.desc()).all()
    redirect('/')
    return render_template("index.html", items = items, labels=labs, values=vals)


@app.route('/<string:defined_page>')
def custom(defined_page):
    return defined_page


@app.route('/page2')
def pg2():
    return render_template("st.html")


if __name__ == '__main__':
    # add_sh()
    app.run(debug = True)
