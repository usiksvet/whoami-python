import ipaddress
import requests

from app import app, db
from app.models import Visitor
from flask import request


@app.route('/')
def index():
    ip_address = request.remote_addr

    if not store_ip_address(ip_address):
        return "Error retrieving location data", 500

    visitors = Visitor.query.all()
    # map = folium.Map(location=[0, 0], zoom_start=2)
    # for visitor in visitors:
    #     folium.Marker(location=[visitor.latitude, visitor.longitude]).add_to(map)
    # map_html = map._repr_html_()

    # return render_template('index.html', map_html=map_html)

    return [v.ip_address for v in visitors]


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
    if ipaddress.ip_address(addr).is_private:
        visitor = Visitor(
            ip_address=addr,
        )
    else:
        data = requests.get(f'http://ip-api.com/json/{ip_address}').json()

        if data['status'] == 'success':
            return False

        visitor = Visitor(
            ip_address=addr,
            longitude=data['lon'],
            latitude=data['lat']
        )

    db.session.add(visitor)
    db.session.commit()
    return True
