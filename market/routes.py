import re
from flask_wtf import form
from market import app , db
from flask import render_template , redirect , url_for , flash, request
from market.models import Item, User
from market.forms import Purchace, RegesterForm , LoginForm , Sell
from flask_login import login_user , logout_user ,login_required , current_user


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/market" , methods = ['POST' , 'GET'])
@login_required
def market():

    #buying item ..

    selling_form = Sell()
    purchace_form= Purchace()
    if request.method == 'POST':
        purchaceed_item = request.form.get('purchaced_item')
        p_item_object = Item.query.filter_by(name = purchaceed_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congrats ! You purshed {p_item_object.name} for {p_item_object.price}$' , category='success')
            else:
                flash('You dont have enough money ..' , category='danger')

        #selling ..

        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f'Congrats ! You sold {sold_item_object.name} for {sold_item_object.price}$' , category='success')
            else:
                flash('something went wrong ..' , category='danger')
        return redirect(url_for('market'))


    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items =Item.query.filter_by(owner = current_user.id)
        return render_template('market.html' , items = items , purchace_form=purchace_form , owned_items=owned_items , selling_form=selling_form)


@app.route('/regester' , methods = ['POST' , 'GET'])
def regester():
    form = RegesterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                            email = form.email.data,
                            password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Success ! You are signed in as : ' + user_to_create.username , category='success')
        return redirect(url_for('market'))
    if form.errors != {}: #if there are errors ..
        for err in form.errors.values():
            flash(f"Something went wrong : {err}" , 'danger')

    return render_template('regester.html' , form = form)
    

@app.route('/login' , methods = ['POST' , 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash('Success ! You are logged in as : ' + attempted_user.username , category='success')
            return redirect(url_for('market'))
        else:
            flash('Username and Password dosent mach .. please try again.' , category='danger')


    return render_template('login.html' , form = form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been loged out !' , category='info')
    return redirect(url_for('home'))
