from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length

expenditure_categories = ['Groceries',
                          'Drinks with friends',
                          'To go',
                          'Gifts',
                          'Eating out/Takeout',
                          'Office supplies',
                          'Self care',
                          'Clothes',
                          'Transport',
                          'Other']


class TransactionForm(FlaskForm):
    hidden = HiddenField()
    amount = DecimalField(label='Amount', validators=[DataRequired()], default=100.00)
    category = SelectField(label='Category', choices=expenditure_categories)
    comment = StringField(label='Label (optional)')
    recurring = BooleanField(label='Recurring')
    name = StringField(label='Name of goal (e.g. New House)', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField(label="Done")


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"

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
    form = TransactionForm()
    return render_template("index.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = TransactionForm()
    if form.validate_on_submit():
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            print("success")
        else:
            print("denied")
    return render_template("pages-login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)