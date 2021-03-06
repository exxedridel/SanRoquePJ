from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User, Worker
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    workers = Worker.query.all()
    return render_template('home.html', workers=workers)


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"!Felicidades! Compraste {p_item_object.name} por ${p_item_object.price} mxn", category='success')
            else:
                flash(f"No cuentas con los fondos suficientes para comprar {p_item_object}", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"¬°Felicidades! vendiste tu {s_item_object.name} al Bazar por ${s_item_object.price} mxn", category='success')
            else:
                flash(f"Algo salio mal al tratar vender tu {s_item_object.name}", category='danger')


        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/userprofile', methods=['GET', 'POST'])
@login_required
def userprofile_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"!Felicidades! Compraste {p_item_object.name} por ${p_item_object.price} mxn", category='success')
            else:
                flash(f"No cuentas con los fondos suficientes para comprar {p_item_object}", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Cancelaste el pedido de {s_item_object.name} exitosamente por {s_item_object.price} puntos", category='success')
            else:
                flash(f"Algo salio mal al tratar vender tu {s_item_object.name}", category='danger')


        return redirect(url_for('userprofile_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('userprofile.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/manage")
def manage():
    return render_template("manage.html")

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"¬°Cuenta creada satisfactoriamente! Has iniciado sesi√≥n como {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'Hubo un error al crear el usuario: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Has iniciado sesi√≥n exitosamente como: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('El usuario y la contrase√Īa no coinciden, intenta de nuevo', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Has salido de tu sesi√≥n", category='info')
    return redirect(url_for("home_page"))
