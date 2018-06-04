import datetime
import os

from flask import Flask, render_template, redirect, url_for, request
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, price=form.price.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    results = Items.query.order_by("name desc").all()
    return str(results)

@app.route("/shop", methods=("GET", "POST"))
def shop():
    if request.method == "POST":
        item_id = request.values.get("item-id")
        quantity = request.values.get("quantity")
        total = request.values.get("total")

        Items.query.filter_by(id=item_id).update(dict(quantity=( int(total) - int(quantity) )  ))
        db_session.commit()

        return redirect(url_for("success"))
    else:
        results = Items.query.order_by("name desc").all()
        return render_template("shop.html", itemList=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
