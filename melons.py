from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    cart_list = session.get("cart", [])
    melon_dict = {}
    # get melon quantities
    if not cart_list:
        flash("Your cart is empty")
    for melon_id in cart_list:  #  {'price':0, 'formatted_total_price':'$2.50'}
        melon_dict[melon_id] = melon_dict.get(melon_id, [0]) 
        melon_dict[melon_id][0] += 1
    # print "************************melon_dict:", melon_dict
    melon_list = [model.get_melon_by_id(melon_id) for melon_id in melon_dict.keys()]
    # print "*********************melon_list: ", melon_list
    cart_total = 0
    for melon in melon_list:
        cart_total += melon_dict[melon.id][0] * melon.price
        total = melon_dict[melon.id][0] * melon.price
        melon_dict[melon.id].append("$%.2f" % total)
    total_string = "Total: $%.2f" % cart_total
    return render_template("cart.html", melon_list = melon_list, quantities = melon_dict, 
        cart_total = total_string)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    id = int(request.form.get("id"))
    cart = session.get('cart', None) or []
    session['cart'] = cart + [id]
    #session.setdefault("cart", []).append(id)
    print "**********************session:", session, cart
    flash("Melon successfully added to cart")
    return redirect("/cart")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    user_email = request.form.get("email")
    user_password = request.form.get("password")
    user_info = model.get_customer_by_email(user_email)
    if user_info:
        session["user"] = user_info
        flash("Login Successful")
    print "*******************email, password", session["user"]
    return redirect("/melons")

@app.route("/logout")
def process_logout():
    session["user"] = []
    flash("Logout successful")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
