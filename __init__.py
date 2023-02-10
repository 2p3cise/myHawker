from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'abc123'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/indianCuisine')
def indianCuisine():
    return render_template('indianCuisine.html')

@app.route('/westernDelights')
def westernDelights():
    return render_template('westernDelights.html')

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

        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
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
@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)

#Nicholas (WORK IN PROGRESS)
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_date_joined(update_customer_form.date_joined.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_remarks(update_customer_form.remarks.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.date_joined.data = customer.get_date_joined()
        update_customer_form.address.data = customer.get_address()
        update_customer_form.membership.data = customer.get_membership()
        update_customer_form.remarks.data = customer.get_remarks()

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
