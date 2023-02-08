from flask import Flask, render_template

app = Flask(__name__)

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
