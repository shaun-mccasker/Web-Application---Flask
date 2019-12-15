from flask import (
    Blueprint, flash, render_template, request, url_for, redirect, session
)
from .models import Item, User, Bid, Purchased_item
from .forms import CreationForm, EditForm, bidForm
from . import db
from flask_login import current_user
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
import os
from flask_login import login_required

# shaun updated-30/9/2019 OPEN
bp = Blueprint('item', __name__)

# -------------------
# view item page
# -------------------
@bp.route('/viewItem/<id>', methods=['POST', 'GET'])
def show(id):
    # load the form for bidding
    bid = bidForm()
    # query for every user
    users = User.query.all()
    # query for the details of the item id provided
    item = Item.query.filter_by(id=id, purchased=None).first()

    # if the user is logged in
    if(current_user.is_authenticated):
        # query the db for any bids for this user in this item
        bids = Bid.query.filter_by(user_id=current_user.id, item_id=id).first()
    else:
        bids = None
    if item != None:
        if bid.validate_on_submit():
            # query the db for the details of the person bidding
            bidder = User.query.filter_by(id=current_user.id).first()

            # commit the bid to the db
            newBid = Bid(bidder_name=bidder.name, bidder_email=bidder.emailid,
                         bidder_phone=bidder.phone_no, user_id=bidder.id, item_id=id)
            db.session.add(newBid)
            db.session.commit()

            # give a succes message
            message = "Bid Placed Successfully!"

            # refresh the data pulled from the database so they can't spam the button
            bid = bidForm()
            users = User.query.all()
            item = Item.query.filter_by(id=id).first()
            bids = Bid.query.filter_by(
                user_id=current_user.id, item_id=id).first()

            return render_template('itemDetails.html', item=item, bid=bid, message=message, bids=bids, users=users)
    return render_template('itemDetails.html', item=item, bid=bid, bids=bids, users=users)

# -------------------
# selling item page
# -------------------
@bp.route('/sellItem/<id>', methods=['POST', 'GET'])
def sellItem(id):
    # pull the bid info from the db
    bid = Bid.query.filter_by(id=id).first()
    # pull the item info from the db
    item = Item.query.filter_by(id=bid.item_id).first()

    # commit the purchases to the db
    newPurchase = Purchased_item(buyer=bid.bidder_name, seller=item.seller,
                                 created_date=item.created_date, item_id=bid.item_id, seller_id=item.user_id, bid_id=bid.id)
    db.session.add(newPurchase)
    db.session.commit()
    # redirect the userto the sold page for that item
    return redirect('/soldItem/' + str(item.id))

# -------------------
# sold item page
# -------------------
@bp.route('/soldItem/<id>', methods=['GET', 'POST'])
@login_required
def soldItem(id):
    # pull the item info from the db
    item = Item.query.filter(Item.id == id, Item.purchased != None).first()
    # initilise as none
    users = None
    purchase = None
    bid = None

    if item != None:
        # pull the items purchase info from the db
        purchase = Purchased_item.query.filter_by(item_id=id).first()
        # pull the bid info from the db
        bid = Bid.query.filter_by(id=purchase.bid_id).first()
        # pull every user info
        users = User.query.all()

    return render_template('soldItemDetails.html', item=item, users=users, purchase=purchase, bid=bid)

# -------------------
# manage item page
# -------------------
@bp.route('/manageItem/<id>', methods=['POST', 'GET'])
@login_required
def manage(id):
    #query all info required for page
    users = User.query.all()
    item = Item.query.filter_by(id=id, purchased=None).first()
    bids = Bid.query.all()
    form = None

    #if looking at an item
    if item != None:
        #if viewing form autofill
        if request.method == 'GET':
            form = EditForm(formdata=MultiDict(
                {'name': item.name, 'price': item.price, 'category': item.category, 'model': item.model, 'description': item.description, 'quality': item.quality, 'image': item.image}))
        #else clear form
        else:
            form = EditForm()
        #Convert user input into data and submit to database
        if request.method == 'POST' and form.validate():
            item.name = form.name.data
            item.price = form.price.data
            item.category = form.category.data
            item.model = form.model.data
            item.description = form.description.data
            item.quality = form.quality.data
            #try image upload
            try:
                item.image = checkUploadFile(form)
            #except use previous image
            except:
                item.image = item.image
            db.session.commit()
            return render_template('itemManage.html', form=form, item=item, users=users, bids=bids)
    return render_template('itemManage.html', form=form, item=item, users=users, bids=bids)

# -------------------
# item upload page
# -------------------
@bp.route('/creation', methods=['POST', 'GET'])
@login_required
def create():
    #input form
    form = CreationForm()
    error = None
    #Convert user input into data and submit to database
    if form.validate_on_submit():
        print('Register form submitted')

        # where i represents item
        iuser_name = current_user.name
        iname = form.name.data
        iprice = form.price.data
        icategory = form.category.data
        imodel = form.model.data
        idescription = form.description.data
        iquality = form.quality.data
        iImage = checkUploadFile(form)
        iUser_id = session["user_id"]
        # create a new user model object
        new_item = Item(seller=iuser_name, name=iname, price=iprice, category=icategory,
                        model=imodel, description=idescription, quality=iquality, image=iImage, user_id=iUser_id)
        db.session.add(new_item)
        db.session.commit()
        # commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))

    return render_template('creation.html', form=form, heading='Item Creation')

# function for saving a file and making sure the filename is safe


def checkUploadFile(form):
    # get the form data
    fp = form.image.data
    # get the file name
    filename = fp.filename
    # get the site path on the system
    Base_Path = os.path.dirname(__file__)
    # get the os location the file will be stored
    upload_path = os.path.join(
        Base_Path, 'static/images', secure_filename(filename))
    # get the path the website will use to get images
    db_upload_path = 'static/images/'+secure_filename(filename)
    # save the file to the server
    fp.save(upload_path)
    # return the file path to be submitted to the db
    return db_upload_path
