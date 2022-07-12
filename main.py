from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length
from datetime import datetime
import os

CURRENT_MONTH = datetime.now().month
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


class ExpenditureForm(FlaskForm):
    amount_expenditure = DecimalField(label='Amount', validators=[DataRequired()], default=100.00)
    category_expenditure = SelectField(label='Category', choices=expenditure_categories)
    comment_expenditure = StringField(label='Label (optional)')
    recurring_expenditure = BooleanField(label='Recurring')
    submit_expenditure = SubmitField(label="Add")


class SavingForm(FlaskForm):
    amount_saving = DecimalField(label='Amount', validators=[DataRequired()], default=100.00)
    comment_saving = StringField(label='Label (optional)')
    recurring_saving = BooleanField(label='Recurring')
    submit_saving = SubmitField(label="Add")


class PiggyBankForm(FlaskForm):
    amount_piggy_bank = DecimalField(label='Amount', validators=[DataRequired()], default=100.00)
    name_piggy_bank = StringField(label='Name of goal (e.g. New House)', validators=[DataRequired(), Length(max=50)])
    submit_piggy_bank = SubmitField(label="Add")


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_FINANCE_TRACKER_KEY")

# ---------------- SQLite CREATE --------------------- #

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-finance-tracker.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column('expenses', db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    variety = db.Column(db.String(250), nullable=False)
    comment = db.Column(db.String(250), nullable=True)
    category = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=True)
    recurring = db.Column(db.Boolean, nullable=False)
    month = db.Column(db.String(250), nullable=False)


db.create_all()

# -------INITIAL DB FILLER----------#

# groceries = [0.67, -20.00, 47.72, -23.00, 6.45, 8.42, 24.64, 10.69, 6.18, -53.00, 10.67, 40.46, 4.24, -20.00, 6.82, 6.90, 9.27, 42.86, 0.7]
# drinks = [9.00, 1.20, 10.50, 6.00]
# eating_out = [39.75, 4.15, 11.98, -12.00, 11.98, 7.95, 5.99]
#
# for x in groceries:
#     new_expense = Item(variety='expense', amount=x, category='Groceries', recurring=False, month=CURRENT_MONTH)
#     db.session.add(new_expense)
#     db.session.commit()
#
# for x in drinks:
#     new_expense = Item(variety='expense', amount=x, category='Drinks with friends', recurring=False, month=CURRENT_MONTH)
#     db.session.add(new_expense)
#     db.session.commit()
#
# for x in eating_out:
#     new_expense = Item(variety='expense', amount=x, category='Eating out/Takeout', recurring=False, month=CURRENT_MONTH)
#     db.session.add(new_expense)
#     db.session.commit()# ---------------FILLER END-----------#
#

# ----------------- SQLite READ ---------------------- #
all_items = Item.query.all()
total_amount = 0
for item in all_items:
    if item.variety == 'expense':
        total_amount += item.amount

expenditure_categories_dict = {
    'Groceries': 0,
    'Drinks with friends': 0,
    'To go': 0,
    'Gifts': 0,
    'Eating out/Takeout': 0,
    'Office supplies': 0,
    'Self care': 0,
    'Clothes': 0,
    'Transport': 0,
    'Other': 0
}


for item in all_items:
    for x in expenditure_categories:
        if item.category == x:
            expenditure_categories_dict[x] += item.amount



# ---------------- SQLite UPDATE --------------------- #


def add_expense(database, amount, category, comment, recurring):
    new_expense = Item(variety='expense', amount=amount, category=category, comment=comment, recurring=recurring, month=CURRENT_MONTH)
    database.session.add(new_expense)
    database.session.commit()


def add_saving(database, amount, comment, recurring):
    new_saving = Item(variety='saving', amount=amount, comment=comment, recurring=recurring, month=CURRENT_MONTH)
    database.session.add(new_saving)
    database.session.commit()


def add_piggy_bank(database, amount, name):
    new_piggy_bank = Item(variety='piggy_bank', amount=amount, name=name, month=CURRENT_MONTH)
    database.session.add(new_piggy_bank)
    database.session.commit()


# ---------------- SQLite DELETE --------------------- #


# ---------------- Flask render_template --------------------- #
@app.route("/", methods=["GET", "POST"])
def get_main_page():
    form1 = ExpenditureForm()
    form2 = SavingForm()
    form3 = PiggyBankForm()
    if request.method == 'POST':
        if form1.validate():
            add_expense(database=db,
                        amount=form1.amount_expenditure.data,
                        category=form1.category_expenditure.data,
                        comment=form1.comment_expenditure.data,
                        recurring=form1.recurring_expenditure.data)
            return redirect(url_for('get_main_page'))
        else:
            print(form1.errors)
        if form2.validate():
            add_saving(database=db,
                       amount=form2.amount_saving.data,
                       comment=form2.comment_saving.data,
                       recurring=form2.recurring_saving.data)
            return redirect(url_for('get_main_page'))
        else:
            print(form2.errors)
        if form3.validate():
            add_piggy_bank(database=db,
                           amount=form3.amount_piggy_bank.data,
                           name=form3.name_piggy_bank.data)
            return redirect(url_for('get_main_page'))
        else:
            print(form3.errors)
    return render_template("index.html",
                           form1=form1,
                           form2=form2,
                           form3=form3,
                           all_items=all_items,
                           total_amount=total_amount,
                           categories=expenditure_categories,
                           amount_list=list(expenditure_categories_dict.values()))

# --------------Running the app------------#
if __name__ == "__main__":
    app.run(debug=True)
