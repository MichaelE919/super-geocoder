#!/usr/bin/env python
"""
Flask Super Geocoder App.

Script creates a simple Flask app which allows a user to upload a CSV file,
then presents that dataset back to the user with additional values for latitude
and longitude. The user has the option to download an updated CSV file.
"""
import pandas
import datetime
from geopy.geocoders import Nominatim

from flask import Flask, render_template, request, send_file

app = Flask(__name__)


def geocoder(df):
    nom = Nominatim()
    if 'Address' in df.columns:
        df['Coordinates'] = df['Address'].apply(nom.geocode)
    elif 'address' in df.columns:
        df['Coordinates'] = df['address'].apply(nom.geocode)
    df['Latitude'] = df['Coordinates'].apply(
        lambda x: x.latitude if x is not None else None)
    df['Longitude'] = df['Coordinates'].apply(
        lambda x: x.longitude if x is not None else None)
    del (df['Coordinates'])
    return df


@app.route('/')
def index():
    """Return app home page."""
    return render_template('index.html')


@app.route('/success-table', methods=['POST'])
def success():
    """Collect data entered on form and commit to database."""
    global filename
    if request.method == 'POST':
        file = request.files['file']
        df = pandas.read_csv(file)
        try:
            geocoder(df)
            filename = datetime.datetime.now().strftime(
                'upload_files/%Y-%m-%d-%H-%M-%S-%f' + '.csv')
            df.to_csv(filename, index=None)
            return render_template(
                'index.html', text=df.to_html(), btn='download.html')
        except KeyError:
            return render_template(
                'index.html',
                text=
                'Please make sure you have an address column in your CSV file!'
            )


@app.route('/download')
def download():
    """Download selected file as attachment to user."""
    return send_file(
        filename, attachment_filename='yourfile.csv', as_attachment=True)


if __name__ == '__main__':
    app.debug = True
    app.run()
