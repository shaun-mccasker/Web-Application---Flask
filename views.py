from flask import Blueprint, render_template, session
from flask_login import login_required
from .models import Item, Purchased_item, Bid
from . import db
from .forms import searchForm
from sqlalchemy import desc

bp = Blueprint('main', __name__)

# -------------------
# landing page
# -------------------
@bp.route('/', methods=['GET', 'POST'])
def index():
    # load the search form
    formSearch = searchForm()

    # if the form has been submitted
    if formSearch.validate_on_submit():
        print('Search')
        # Pull the category data from the form
        cate = formSearch.category.data
        # query the database for an Item that is not purchased for the category selected
        # then sort by descending ID number
        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        # display the items for that category
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    # Query the database for Items that are not purchased and order by ID
    items = Item.query.filter_by(
        purchased=None).order_by(desc(Item.id)).all()

    return render_template('index.html', type="view", items=items, formSearch=formSearch, heading='Items For Sale')

# -------------------
# selling items page
# -------------------
@bp.route('/selling', methods=['GET', 'POST'])
@login_required
def selling():
   # load the search form
    formSearch = searchForm()

    # if the form has been submitted
    if formSearch.validate_on_submit():
        print('Search')
        # Pull the category data from the form
        cate = formSearch.category.data
        # query the database for an Item that is not purchased for the category selected
        # then sort by descending ID number
        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        # display the items for that category
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    # Query the DB for an Item that has the users id and is not sold
    items = Item.query.filter_by(
        user_id=session['user_id'], purchased=None).order_by(desc(Item.id)).all()

    # render the template, providing the correct titles
    return render_template('items.html', type="selling", items=items, formSearch=formSearch, heading="Items You Have For Sale")

# -------------------
# sold items page
# -------------------
@bp.route('/sold', methods=['GET', 'POST'])
@login_required
def sold():
    # load the search form
    formSearch = searchForm()

    # if the form has been submitted
    if formSearch.validate_on_submit():
        print('Search')
        # Pull the category data from the form
        cate = formSearch.category.data
        # query the database for an Item that is not purchased for the category selected
        # then sort by descending ID number
        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        # display the items for that category
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    # query the DB for items that have the users foriegn key and has a foreign key in the puchased_item Table
    items = Item.query.filter(
        Item.user_id == session['user_id'], Item.purchased != None).order_by(desc(Item.id)).all()

    # render the template with the correct headings
    return render_template('items.html', type="sold", items=items, formSearch=formSearch, heading="Items You Have Sold")

# -------------------
# Bidded Items page
# -------------------
@bp.route('/bid', methods=['GET', 'POST'])
@login_required
def bid():
    # load the search form
    formSearch = searchForm()

    # if the form has been submitted
    if formSearch.validate_on_submit():
        print('Search')
        # Pull the category data from the form
        cate = formSearch.category.data
        # query the database for an Item that is not purchased for the category selected
        # then sort by descending ID number
        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        # display the items for that category
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)
    # query the DB for Items that have bids and are not sold
    items = Item.query.filter(Item.bids != None, Item.purchased == None).order_by(
        desc(Item.id)).all()
    # pull every bid from the DB, to be compared to against the Items
    bids = Bid.query.all()

    # render the template with the correct headings
    return render_template('bid.html', items=items, formSearch=formSearch, bids=bids, heading="Items You Have Bidded On")

# --------------------
# purchased items page
# --------------------
@bp.route('/purchases', methods=['GET', 'POST'])
@login_required
def purchases():
    # load the search form
    formSearch = searchForm()

    # if the form has been submitted
    if formSearch.validate_on_submit():
        print('Search')
        # Pull the category data from the form
        cate = formSearch.category.data
        # query the database for an Item that is not purchased for the category selected
        # then sort by descending ID number
        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        # display the items for that category
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    # pull every purchased Item for the DB
    items = Item.query.filter(Item.purchased != None).order_by(
        desc(Item.id)).all()
    # pull every record of a sale from the db
    purchases = Purchased_item.query.all()

    # render the template with the correct headings
    return render_template('purchases.html', items=items, formSearch=formSearch, purchases=purchases, heading="Items You Have Purchased")
