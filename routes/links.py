from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required
from services.link_service import get_links, get_visits

bp = Blueprint('links', __name__)

@bp.route('/links')
def view_links():
    links, host_url = get_links()
    return render_template('links.html',links=links, host_url=host_url)

@bp.route('/link/<short_url>')
def view_link(short_url):
    visits, clicks_by_day, clicks_by_device, clicks_by_browser = get_visits(short_url)
    print(clicks_by_device)
    return render_template('link.html',
                           visits=visits,
                           title=request.host_url + short_url, 
                           clicks_by_day=clicks_by_day, 
                           clicks_by_device=clicks_by_device, 
                           clicks_by_browser=clicks_by_browser)