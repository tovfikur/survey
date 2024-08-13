import routes
from flask import Flask,request, redirect, url_for, flash, render_template, send_from_directory
import os 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
def create_the_database(db):
    db.create_all()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'A secret'

all_methods = ['GET', 'POST']

# Home page (where you will add a new user)
app.add_url_rule('/', view_func=routes.index)
# "Thank you for submitting your form" page
app.add_url_rule('/submitted', methods=['POST'], view_func=routes.submitted)
# Viewing all the content in the database page
app.add_url_rule('/database', view_func=routes.view_database)
app.add_url_rule('/modify<the_id>/<modified_category>', methods=all_methods, view_func=routes.modify_database)
app.add_url_rule('/delete<the_id>', methods=all_methods, view_func=routes.delete)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # no warning messages
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db' # for using the sqlite database
app.config['SQLALCHEMY_BINDS'] = {
    'auth': 'sqlite:///auth.db',  # Separate database for authentication
    'main': 'sqlite:///info.db'   # Main database
}

db = SQLAlchemy(app)

# Create User Table
class User(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    damage = db.Column(db.String(10))
    thana = db.Column(db.String(10))
    address = db.Column(db.String(10))
    zilla = db.Column(db.String(10))
    details = db.Column(db.Text)
    proof = db.Column(db.Text)
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class AuthUser(UserMixin, db.Model):
    __bind_key__ = 'auth'
    __tablename__ = 'auth_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return AuthUser.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AuthUser.query.filter_by(username=username).first()

        if user and user.password == password:  # Hashing is recommended for passwords
            login_user(user)
            return redirect(url_for('view_database'))

        flash('Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        user = AuthUser.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
        else:
            new_user = AuthUser(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/admins')
@login_required
def view_users():
    users = AuthUser.query.all()
    return render_template('users.html', users=users)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # Ensure only admin can access this route
    if not current_user.username == 'admin':
        return redirect(url_for('login'))

    user = AuthUser.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.')
    else:
        flash('User not found.')

    return redirect(url_for('view_users'))

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory('uploads/', filename)

@app.route('/success')
def success():
    return render_template('success.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



def insert_data(name, phone, damage,thana,address,zilla,details,proof):
    print(proof)
    new_user = User(name=name, phone=phone, damage=damage, thana=thana, address=address, zilla=zilla, details=details, proof=proof)
    db.session.add(new_user)
    db.session.commit()
    print(new_user.proof)

def modify_data(the_id, col_name, user_input):
    the_user = User.query.filter_by(id=the_id).first()
    if col_name == 'name':
        the_user.name = user_input
    elif col_name == 'phone':
        the_user.phone = user_input 
    elif col_name == 'damage':
        the_user.damage = user_input 
    elif col_name == 'thana':
        the_user.thana = user_input 
    elif col_name == 'address':
        the_user.address = user_input 
    elif col_name == 'zilla':
        the_user.zilla = user_input 
    elif col_name == 'details':
        the_user.details = user_input 
    elif col_name == 'proof':
        the_user.proof = user_input 
    
    
    db.session.commit() 


def delete_data(the_id):
    the_user = User.query.filter_by(id=the_id).first()
    db.session.delete(the_user)
    db.session.commit()
    

def get_all_rows_from_table():
    users = User.query.all()
    return users 
    

# if database does not exist in the current directory, create it!
db_is_new = not os.path.exists('info.db')
if db_is_new:
    create_the_database(db)




def create_default_user():
    # Check if the default user already exists
    default_user = AuthUser.query.filter_by(username='admin').first()
    if not default_user:
        # Create the default user
        default_user = AuthUser(username='admin', password='alsopasswordofadmin')
        db.session.add(default_user)
        db.session.commit()


# start the app
if __name__ == '__main__':
    create_default_user()
    app.run(debug=True)
