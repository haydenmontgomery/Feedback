from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserRegisterForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.app_context().push()
connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def goto_register():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    form = UserRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username or Email Taken. Please Pick Another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome to the site!', 'success')
        return redirect(f'/users/{session["username"]}')
    
    return render_template('register.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back!, {user.username}!', 'primary')
            session['username'] = user.username
            return redirect(f'/users/{session["username"]}')
        else:
            form.username.errors = ['Invalid username or password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    if "username" in session:
        session.pop('username')
        flash("Goodbye!", "info")
        return redirect('/')
    return redirect('/')

@app.route('/users/<string:username>')
def user_page(username):
    if session['username'] == username:
        user = User.query.get_or_404(username)
        feedbacks = Feedback.query.filter_by(username=username)
        return render_template('user.html', user=user, feedbacks=feedbacks)

    flash("You do not have access to that user", "danger")
    return redirect('/login')    

@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("User deleted!", "danger")
        return redirect('/register')
    return redirect('/')

@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def feedback(username):
    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    form = FeedbackForm()
    if form.validate_on_submit():
        if session['username'] == username:
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            flash("Feedback added!", "info")
            return redirect(f'/users/{session["username"]}')
        #return render_template('feedback.html', form=form)
    
    #flash("You do not have access to that user", "danger")
    return render_template('feedback.html', form=form)

@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def edit_feedback(id):
    try:
        feedback = Feedback.query.get_or_404(id)
    except:
        flash("Feedback does not exist!", "info")
        return redirect('/login')   
    else: 
        if not feedback:
            return redirect('/login')
        if feedback.username != session['username']:
            flash("You did not write this feedback!", "info")
            return redirect('/login')

        form = FeedbackForm(title=feedback.title, content=feedback.content)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.add(feedback)
            db.session.commit()
            flash("Feedback updated!", "info")
            return redirect(f'/users/{session["username"]}')
    
    return render_template('edit_feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", "danger")
        return redirect(f'/users/{session["username"]}')