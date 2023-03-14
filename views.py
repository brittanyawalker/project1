"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app
from flask import render_template, request, redirect, url_for


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create', methods=['GET', 'POST'])
def createproperty():
    # Loads up the form
    form = PropertyForm()

    # Checks for method type and validatation
    if request.method == 'POST':
        if form.validate_on_submit():

            # Collect the data from the form
            proptitle = request.form['proptitle']
            description = request.form['description']
            room = request.form['room']
            bathroom = request.form['bathroom']
            propprice = request.form['propprice']
            proptype = request.form['proptype']
            location = request.form['location']
            file = request.files['picup']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            myprop = Property(proptitle, description, room, bathroom, propprice, proptype, location, filename)
            db.session.add(myprop)
            db.session.commit()

            flash('New property has been successfully created and added!', 'success')
            return redirect(url_for('properties'))
        else:
            flash("Error!")
            return render_template('property.html', form=form)
    elif request.method == 'GET':
        return render_template('property.html', form=form)  

@app.route('/properties')
def properties():

    properties=Property.query.all()
    return render_template("properties.html", properties=properties)

@app.route('/property/<propertyid>')
def propertyindivid(propertyid):
    propertyid = int(propertyid)
    myprop = Property.query.filter_by(id=propertyid).first()

    return render_template('individproperty.html', property=myprop)

@app.route('/uploads/<filename>')
def uploadimg(filename):
    upimg = send_from_directory(os.path.join(os.getcwd(),
    app.config['UPLOAD_FOLDER']), filename)
    return upimg


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
