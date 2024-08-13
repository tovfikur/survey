from flask import render_template, request, redirect, url_for, jsonify
import forms
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
""" 
Generate the login form (using flask) for the index.html page, where you will 
enter a new user. The form itself is created in forms.py. 
The index() route method is called from app.py
"""
def index():
    form = forms.LoginForm()
    return render_template('index.html', form=form)

""" 
Retrieve all the rows from the database and return them.
All the data will be displayed on entire_database.html file.
The view_database() route method is called from app.py
"""
@login_required
def view_database():
    from app import get_all_rows_from_table
    rows = get_all_rows_from_table()
    
    return render_template('entire_database.html', rows=rows)

@login_required
def modify_database(the_id ,modified_category):
    if request.method == 'POST':
        from app import modify_data
        # Get data from the form on database page
        user_input = request.form[modified_category]
        # modify the row from the database
        modify_data(the_id, modified_category, user_input)
        # redirect back to the database page
        return redirect(url_for('view_database'))
    return redirect(url_for('index'))

@login_required
def delete(the_id):
    if request.method == 'POST':
        from app import delete_data
        # if the checkbox was selected (for deleting entire row)
        if 'remove' in request.form:
            delete_data(the_id)
    return redirect(url_for('view_database'))




UPLOAD_FOLDER = 'uploads/'  # Directory to save uploaded files
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'doc', 'docx', 'txt', 'zip'}  # Allowed file extensions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def submitted():
    from app import insert_data

    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.form['name']
            phone = request.form['phone']
            damage = request.form['damage']
            thana = request.form['thana']
            address = request.form['address']
            zilla = request.form['zilla']
            details = request.form['details']
            # Handle file uploads
            proof_files = request.files.getlist('proof')  # Multiple files
            proof_filenames = []

            for file in proof_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    proof_filenames.append(filename)

            # Store filenames in proof field
            proof = ','.join(proof_filenames)  # Store as comma-separated list

            # Insert data into database
            insert_data(name, phone, damage, thana, address, zilla, details, proof)

            # Return JSON response indicating success
            return jsonify({"status": "success", "message": "Data submitted successfully."})
        
        except Exception as e:
            # Return JSON response indicating failure
            return jsonify({"status": "failed", "message": str(e)}), 500