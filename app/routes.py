import datetime
import folium
import ipaddress
import requests

from app import app, db
from app.models import Visitor
from flask import request, render_template
from sqlalchemy import func, desc


@app.route('/')
def index():
    remote_addr = request.remote_addr

    if not store_ip_address(remote_addr):
        return "Error retrieving location data", 500

    visitors = (
        db.session.query(
            Visitor.ip_address,
            func.max(Visitor.timestamp).label('last_seen'),
            func.count(Visitor.id).label('count'),
            Visitor.longitude,
            Visitor.latitude,
        )
        .group_by(Visitor.ip_address)
        .order_by(desc('last_seen'))
        .all()
    )

    map = folium.Map(location=[0, 0], zoom_start=2)
    for visitor in visitors:
        if visitor.latitude and visitor.longitude:
            folium.Marker(location=[visitor.latitude, visitor.longitude]).add_to(map)
    map_html = map._repr_html_()

    return render_template('index.html', map_html=map_html, visitors=visitors)


@app.route('/ip')
def ip():
    remote_addr = request.remote_addr

    if not store_ip_address(remote_addr):
        return "Error retrieving location data", 500

    return remote_addr


@app.route('/healthcheck')
def healthcheck():
    return "OK"


def store_ip_address(addr):
    now = datetime.datetime.utcnow()

    if ipaddress.ip_address(addr).is_private:
        visitor = Visitor(
            timestamp=now,
            ip_address=addr,
        )
    else:
        data = requests.get(f'http://ip-api.com/json/{addr}').json()

        if data['status'] != 'success':
            return False

        visitor = Visitor(
            timestamp=now,
            ip_address=addr,
            longitude=data['lon'],
            latitude=data['lat']
        )

    db.session.add(visitor)
    db.session.commit()
    return True
