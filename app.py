#!/usr/bin/env python
"""
Flask Super Geocoder App.

Script creates a simple Flask app which allows a user to upload a CSV file,
then presents that dataset back to the user with additional values for latitude
and longitude. The user has the option to download an updated CSV file.
"""
from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename

app = Flask(__name__)

# TODO: Define Geocoder function for uploaded CSV file.


@app.route('/')
def index():
    """Return app home page."""
    return render_template('index.html')


@app.route('/success-table', methods=['POST'])
def success():
    """Collect data entered on form and commit to database."""
    global file
    if request.method == 'POST':
        file = request.files['file']
        file.save(secure_filename('uploaded' + file.filename))
        # Create a dataframe object (pandas)
        with open('uploaded' + file.filename, 'a') as f:
            f.write('\nThis was added later!')
        # insert call to Geocoder function
        print(file)
        print(type(file))
        return render_template('index.html', btn='download.html')
    return render_template(
        'index.html',
        text='Please make sure you have an address column in your CSV file!'
    )


@app.route('/download')
def download():
    """Download selected file as attachment to user."""
    return send_file(
        'uploaded' + file.filename,
        attachment_filename='yourfile.txt',
        as_attachment=True)


if __name__ == '__main__':
    app.debug = True
    app.run()
