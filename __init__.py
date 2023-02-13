from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateDishForm, CreateCustomerForm, LoginForm
import shelve, Dishes, Customers
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "abc123"

@app.route('/')
def home():
    return render_template('home.html')

#Nicholas
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        if email == "secretadmin@myHawker.com" and password == "AdminAccess":
            return redirect(url_for('home_admin'))
        else:
            db = shelve.open('user_credentials.db', 'c')
            try:
                user_credentials = db['user_credentials']
            except:
                print("Error in retrieving user_credentials from user_credentials.db.")

            if email in user_credentials and user_credentials[email] == password:
                session['email'] = email
                return redirect(url_for('home'))
            else:
                error = 'Invalid username or password. Please try again.'

        db.close()
    return render_template('login.html', form=login_form, error=error)

#Nicholas
@app.route('/updateCredentials', methods=['GET', 'POST'])
def update_credentials():
    update_form = UpdateCredentialsForm(request.form)
    error = None
    if request.method == 'POST' and update_form.validate():
        db = shelve.open('user_credentials.db', 'w')
        try:
            user_credentials = db['user_credentials']
        except:
            user_credentials = {}

        if session['email'] in user_credentials:
            if user_credentials[session['email']] == update_form.current_password.data:
                if update_form.current_password.data != update_form.new_password.data:
                    if update_form.new_password.data == update_form.confirm_password.data:
                        user_credentials[session['email']] = update_form.new_password.data
                        db['user_credentials'] = user_credentials
                        db.close()
                        return redirect(url_for('home'))
                    else:
                        error = 'New password and confirmation do not match. Please try again.'
                else:
                    error = 'New password is the same as the current password.'
            else:
                error = 'Current password is incorrect. Please try again.'
        else:
            error = 'Error in updating the credentials. Please try again.'
            db.close()
    return render_template('updateCredentials.html', form=update_form, error=error)

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/createDish', methods=['GET', 'POST'])
def create_dish():
    create_dish_form = CreateDishForm(request.form)
    if request.method == 'POST' and create_dish_form.validate():
        dishes_dict = {}
        db = shelve.open('dish.db', 'c')

        try:
            dishes_dict = db['Dishes']
        except:
            print("Error in retrieving Users from dish.db")

        

        dish = Dishes.Dish(create_dish_form.dish_name.data, create_dish_form.price.data, create_dish_form.description.data, create_dish_form.cuisine.data)

        images = request.files.getlist("image")
        basePath = "static/images/dishes/" + str(dish.get_dish_id())
        os.makedirs(basePath)

        imagePath = secure_filename(images[0].filename)
        path = os.path.join(basePath, imagePath)
        images[0].save(path)
        dish.set_image(path)


        dishes_dict[dish.get_dish_id()] = dish
        db['Dishes'] = dishes_dict

        db.close()

        return redirect(url_for('retrieve_dishes'))
    return render_template('createDish.html', form=create_dish_form)


@app.route('/retrieveDish')
def retrieve_dishes():
    dishes_dict = {}
    db = shelve.open('dish.db', 'r')
    dishes_dict = db['Dishes']
    db.close()

    dishes_list = []
    for key in dishes_dict:
        dish = dishes_dict.get(key)
        dishes_list.append(dish)

    return render_template('retrieveDish.html', count=len(dishes_list), dishes_list=dishes_list)


@app.route('/updateDish/<int:id>/', methods=['GET', 'POST'])
def update_dish(id):
    update_dish_form = CreateDishForm(request.form)
    if request.method == 'POST' and update_dish_form.validate():
        dishes_dict = {}
        db = shelve.open('dish.db', 'w')
        dishes_dict = db['Dishes']

        dish = dishes_dict.get(id)
        dish.set_dish_name(update_dish_form.dish_name.data)
        dish.set_price(update_dish_form.price.data)
        dish.set_description(update_dish_form.description.data)
        dish.set_cuisine(update_dish_form.cuisine.data)

        images = request.files.getlist("image")
        if images[0].filename != "":
            basePath = "static/images/dishes/" + str(dish.get_dish_id())

            imagePath = secure_filename(images[0].filename)
            path = os.path.join(basePath, imagePath)
            images[0].save(path)
            dish.set_image(path)

        db['Dishes'] = dishes_dict
        db.close()

        return redirect(url_for('retrieve_dishes'))
    else:
        dishes_dict = {}
        db = shelve.open('dish.db', 'r')
        dishes_dict = db['Dishes']
        db.close()

        dish = dishes_dict.get(id)
        update_dish_form.dish_name.data = dish.get_dish_name()
        update_dish_form.price.data = dish.get_price()
        update_dish_form.description.data = dish.get_description()
        update_dish_form.cuisine.data = dish.get_cuisine()
        update_dish_form.image.data = dish.get_image()

        return render_template('updateDish.html', form=update_dish_form)


@app.route('/deleteDish/<int:id>', methods=['POST'])
def delete_dish(id):
    dishes_dict = {}
    db = shelve.open('dish.db', 'w')
    dishes_dict = db['Dishes']
    dishes_dict.pop(id)
    db['Dishes'] = dishes_dict
    db.close()
    return redirect(url_for('retrieve_dishes'))

@app.route('/addtocart/<int:id>', methods=['POST'])
def add_to_cart(id):
    dishes_dict = {}
    db = shelve.open('dish.db', 'w')
    dishes_dict = db['Dishes']
    dishes_dict.pop(id)
    db['Dishes'] = dishes_dict
    db.close()
    return redirect(url_for('retrieve_dishes'))


@app.route('/adminindiancuisine')
def adminindian_cuisine():
    dishes_dict = {}
    db = shelve.open('dish.db', 'r')
    dishes_dict = db['Dishes']
    db.close()

    dishes_list = []
    for key in dishes_dict:
        dish = dishes_dict.get(key)
        dishes_list.append(dish)

    return render_template('adminindiancuisine.html', count=len(dishes_list), dishes_list=dishes_list)

@app.route('/customerindiancuisine')
def customerindian_cuisine():
    dishes_dict = {}
    db = shelve.open('dish.db', 'r')
    dishes_dict = db['Dishes']
    db.close()

    dishes_list = []
    for key in dishes_dict:
        dish = dishes_dict.get(key)
        dishes_list.append(dish)

    return render_template('customerindiancuisine.html', count=len(dishes_list), dishes_list=dishes_list)

@app.route('/adminwesterncuisine')
def adminwestern():
    dishes_dict = {}
    db = shelve.open('dish.db', 'r')
    dishes_dict = db['Dishes']
    db.close()

    dishes_list = []
    for key in dishes_dict:
        dish = dishes_dict.get(key)
        dishes_list.append(dish)

    return render_template('adminwesterncuisine.html', count=len(dishes_list), dishes_list=dishes_list)

@app.route('/customerwesterncuisine')
def customerwestern():
    dishes_dict = {}
    db = shelve.open('dish.db', 'r')
    dishes_dict = db['Dishes']
    db.close()

    dishes_list = []
    for key in dishes_dict:
        dish = dishes_dict.get(key)
        dishes_list.append(dish)

    return render_template('customerwesterncuisine.html', count=len(dishes_list), dishes_list=dishes_list)


@app.route('/adminmixedrice')
def adminmixedrice():
    dishes_dict = {}
    db = shelve.open('dish.db', 'r')
    dishes_dict = db['Dishes']
    db.close()

    dishes_list = []
    for key in dishes_dict:
        dish = dishes_dict.get(key)
        dishes_list.append(dish)

    return render_template('adminmixedrice.html', count=len(dishes_list), dishes_list=dishes_list)

@app.route('/customermixedrice')
def customermixedrice():
    dishes_dict = {}
    db = shelve.open('dish.db', 'r')
    dishes_dict = db['Dishes']
    db.close()

    dishes_list = []
    for key in dishes_dict:
        dish = dishes_dict.get(key)
        dishes_list.append(dish)

    return render_template('customermixedrice.html', count=len(dishes_list), dishes_list=dishes_list)
















#Nicholas
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        db = shelve.open('user_credentials.db', 'c')

        try:
            user_credentials = db['user_credentials']
        except:
            print("Error in retrieving user_credentials from user_credentials.db.")

        if email in user_credentials and user_credentials[email] == password:
            session['email'] = email
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password. Please try again.'

        db.close()
    return render_template('login.html', form=login_form, error=error)

#Nicholas
@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customers.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data, create_customer_form.membership.data,
                                     create_customer_form.remarks.data, create_customer_form.email.data,
                                     create_customer_form.date_joined.data, create_customer_form.address.data,
                                     create_customer_form.password.data)
        customers_dict[customer.get_user_id()] = customer
        db['Customers'] = customers_dict

        db.close()

        db = shelve.open('user_credentials.db', 'c')
        try:
            user_credentials = db['user_credentials']
        except:
            user_credentials = {}

        user_credentials[create_customer_form.email.data] = create_customer_form.password.data
        db['user_credentials'] = user_credentials
        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)

#Nicholas
@app.route('/adminretrieveCustomer')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('adminretrieveCustomer.html', count=len(customers_list), customers_list=customers_list)

#Nicholas 
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_date_joined(update_customer_form.date_joined.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_password(update_customer_form.password.data)
        customer.set_remarks(update_customer_form.remarks.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_dishes'))

    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.date_joined.data = Customers.get_date_joined()
        update_customer_form.address.data = Customers.get_address()
        update_customer_form.membership.data = Customers.get_membership()
        update_customer_form.password.data = Customers.get_password()
        update_customer_form.remarks.data = Customers.get_remarks()

        return render_template('updateCustomer.html', form=update_customer_form)


#Nicholas
@app.route('/deleteCustomer/<int:id>/<email>', methods=['POST'])
def delete_customer(id, email):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    user_credentials = {}
    db = shelve.open('user_credentials.db', 'w')
    user_credentials = db['user_credentials']
    user_credentials.pop(email)

    db['user_credentials'] = user_credentials
    db.close()

    return redirect(url_for('retrieve_customers'))


#Nicholas
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    feedback_form = FeedbackForm(request.form)
    if request.method == "POST" and feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')
        feedback = Feedback.Feedback(feedback_form.rating.data, feedback_form.remarks.data)

        try:
            feedback_dict = db["Feedback"]
        except:
            print("Error")

        feedback_dict[feedback.get_feedback_id()] = feedback
        db["Feedback"] = feedback_dict

        db.close()

        return redirect(url_for("view_feedback"))
    return render_template('feedback.html', form=feedback_form)

#Nicholas
@app.route('/viewFeedback')
def view_feedback():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db["Feedback"]
    db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedback_list.append(feedback)

    return render_template('viewFeedback.html', count=len(feedback_list), feedback_list=feedback_list)

#Nicholas
@app.route('/retrieveFeedback', methods=['GET', 'POST'])
def retrieve_feedback():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db["Feedback"]
    db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedback_list.append(feedback)

    return render_template('retrieveFeedback.html', count=len(feedback_list), feedback_list=feedback_list)

#Nicholas
@app.route('/updateFeedback/<int:id>/', methods=['GET', 'POST'])
def update_feedback(id):
    update_feedback_form = FeedbackForm(request.form)
    if request.method == 'POST' and update_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'w')
        feedback_dict = db['Feedback']
        feedback = feedback_dict.get(id)
        feedback.set_rating(update_feedback_form.rating.data)
        feedback.set_remarks(update_feedback_form.remarks.data)

        db['Feedback'] = feedback_dict
        db.close()

        return redirect(url_for('retrieve_feedback'))
    else:
        feedback_dict = {}
        db = shelve.open('feedback.db', 'r')
        feedback_dict = db['Feedback']
        db.close()

        feedback = feedback_dict.get(id)
        update_feedback_form.rating.data = feedback.get_rating()
        update_feedback_form.remarks.data = feedback.get_remarks()

        return render_template('updateFeedback.html', form=update_feedback_form)

#Nicholas
@app.route('/deleteFeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedback_dict = db['Feedback']

    feedback_dict.pop(id)

    db['Feedback'] = feedback_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))

if __name__ == '__main__':
    app.run(debug=True)
