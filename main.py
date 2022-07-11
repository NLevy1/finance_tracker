from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# ---------------- SQLite CREATE --------------------- #

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-finance-tracker.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()

# ----------------- SQLite READ ---------------------- #


# ---------------- SQLite UPDATE --------------------- #
class Expense(db.Model):
    id = db.Column('expenses', db.Integer, primary_key=True)
    variety = db.Column(db.String(250), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tag = db.Column(db.String(250), nullable=True)
    category = db.Column(db.String(250), nullable=False)


def add_expense(variety, amount, tag, category):
    new_expense = Expense(variety=variety, amount=amount, tag=tag, category=category)
    db.session.add(new_expense)
    db.session.commit()


# ---------------- SQLite DELETE --------------------- #


# ---------------- Flask render_template --------------------- #
@app.route("/")
def get_main_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)