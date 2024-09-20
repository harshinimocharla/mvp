from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apparel.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize the database
db = SQLAlchemy(app)

# Model for Apparel
class Apparel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)  # e.g., "T-shirt", "Shoes"
    condition = db.Column(db.String(100), nullable=False)  # e.g., "Worn-out", "Like-new"
    action = db.Column(db.String(100), nullable=False)  # e.g., "Recycle", "Donate", "Dispose"

    def repr(self):
        return f"<Apparel {self.type} - {self.condition}>"

# Home route - Form to submit apparel information
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data from user input
        apparel_type = request.form.get('type')
        condition = request.form.get('condition')
        action = request.form.get('action')

        # Validate form data
        if not apparel_type or not condition or not action:
            flash('All fields are required!')
            return redirect(url_for('index'))

        # Create a new Apparel entry
        new_apparel = Apparel(type=apparel_type, condition=condition, action=action)
        try:
            db.session.add(new_apparel)
            db.session.commit()  # Commit to the database
            flash('Apparel information submitted successfully!')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}")
            return redirect(url_for('index'))

        return redirect(url_for('dashboard'))

    return render_template('index.html')

# Dashboard route to view submissions
@app.route('/dashboard')
def dashboard():
    apparels = Apparel.query.all()  # Retrieve all apparel submissions
    return render_template('dashboard.html', apparels=apparels)

# Error handling for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Initialize the database tables manually
with app.app_context():
    db.create_all()  # Create tables before the app starts

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
