from database import get_db
from flask import request

def get_links():
    db = get_db()
    links = db.execute("""
        SELECT urls.id, urls.original_url, urls.short_url, urls.user_id, COUNT(link_visits.id) as visits_count 
        FROM urls
        LEFT JOIN link_visits ON urls.short_url = link_visits.short_url
        GROUP BY urls.id
    """).fetchall()
    print(links)
    host_url = request.host_url
    return links, host_url

def get_visits(short_url):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM link_visits WHERE short_url = ?", (short_url,))
    visits = cursor.fetchall()

    cursor.execute("SELECT DATE(timestamp) as day, COUNT(*) FROM link_visits WHERE short_url = ? GROUP BY day", (short_url,))
    clicks_by_day = cursor.fetchall()
    
    cursor.execute("SELECT device, COUNT(*) FROM link_visits WHERE short_url = ? GROUP BY device", (short_url,))
    clicks_by_device = cursor.fetchall()

    cursor.execute("SELECT browser, COUNT(*) FROM link_visits WHERE short_url = ? GROUP BY browser", (short_url,))
    clicks_by_browser = cursor.fetchall()

    return visits, clicks_by_day, clicks_by_device, clicks_by_browser