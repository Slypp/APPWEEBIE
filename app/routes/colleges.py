from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from flask_login import login_required
import datetime as dt
from app.classes.data import College
from app.classes.forms import CollegeForm

@app.route('/college/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def collegeNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = CollegeForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new blog form. 
        # Blog() is a mongoengine method for creating a new blog. 'newBlog' is the variable 
        # that stores the object that is the result of the Blog() method.  
        newCollege = College(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            name = form.name.data,
            kind_of = form.kind_of.data,
            bef_cost = form.bef_cost.data,
            aft_cost = form.aft_cost.data,
            location = form.location.data,
            kd = form.kd.data,
            sum_weather = form.sum_weather.data,
            wint_weather = form.wint_weather.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
        )
        if form.imagefile.data:
            newCollege.imagefile.put(form.imagefile.data, content_type='image/jpeg')
            newCollege.save()
        # This is a method that saves the data to the mongoDB database.
        newCollege.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('college',collegeID=newCollege.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('collegeform.html',form=form)


@app.route('/college/<collegeID>')
@login_required

def college(collegeID):
    thisCollege = College.objects.get(id=collegeID)
    return render_template("college.html", college=thisCollege)

@app.route('/colleges')
@login_required

def colleges():
    colleges = College.objects()
    return render_template("colleges.html",colleges=colleges)


@app.route('/colleges/universities')
@login_required
def collegesuniversities():
    colleges = College.objects(kind_of="University")
    return render_template("colleges.html",colleges=colleges)

@app.route('/colleges/community')
@login_required
def collegescommunity():
    colleges = College.objects(kind_of="Community College")
    return render_template("colleges.html",colleges=colleges)

@app.route('/colleges/hbcu')
@login_required
def collegeshbcu():
    colleges = College.objects(kind_of="Historically Black Colleges and Universities(HBCU)")
    return render_template("colleges.html",colleges=colleges)

@app.route('/colleges/public')
@login_required
def collegespublic():
    colleges = College.objects(kind_of="Public 4 Year-College (UC/CSU)")
    return render_template("colleges.html",colleges=colleges)


@app.route('/college/edit/<collegeID>', methods=['GET', 'POST'])
@login_required

def collegeEdit(collegeID):
    form = CollegeForm()
    editCollege = College.objects.get(id=collegeID)

    if editCollege.author != current_user:
        flash("You can't edit a sleep you don't own.")
        return redirect(url_for('colleges'))
    
    if form.validate_on_submit():
        editCollege.update(
            name = form.name.data,
            kind_of = form.kind_of.data,
            bef_cost = form.bef_cost.data,
            aft_cost = form.aft_cost.data,
            location = form.location.data,
            kd = form.kd.data,
            sum_weather = form.sum_weather.data,
            wint_weather = form.wint_weather.data,
        )
        editCollege.save()
        if form.imagefile.data:
            if editCollege.imagefile:
               editCollege.imagefile.delete()
            editCollege.imagefile.put(form.imagefile.data, content_type='image/jpeg')
            editCollege.save()
        return redirect(url_for("college",collegeID=editCollege.id))

    form.name.process_data(editCollege.name)
    form.kind_of.process_data(editCollege.kind_of)
    form.bef_cost.process_data(editCollege.bef_cost)
    form.aft_cost.process_data(editCollege.aft_cost)
    form.location.process_data(editCollege.location)
    form.kd.process_data(editCollege.kd)
    form.sum_weather.process_data(editCollege.sum_weather)
    form.wint_weather.process_data(editCollege.wint_weather)
    return render_template("collegeform.html",form=form)


@app.route('/college/delete/<collegeID>')
@login_required

def collegeDelete(collegeID):
    delCollege = College.objects.get(id=collegeID)
    collegeDate = delCollege.create_date
    delCollege.delete()
    flash(f"The school with date {collegeDate} has been deleted.")
    return redirect(url_for('colleges'))