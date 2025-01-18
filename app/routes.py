import folium

import app.utils as utils

from app import db
from app.models import Visitor
from flask import Blueprint, current_app, render_template
from sqlalchemy import func, desc

main = Blueprint("main", __name__)


@main.route("/")
def index():
    remote_addr = utils.get_ip()

    if not utils.store_ip_address(remote_addr):
        return "Error retrieving location data", 500

    visitors = (
        db.session.query(
            Visitor.ip_address,
            func.max(Visitor.timestamp).label("last_seen"),
            func.count(Visitor.id).label("count"),
            Visitor.longitude,
            Visitor.latitude,
        )
        .group_by(Visitor.ip_address, Visitor.longitude, Visitor.latitude)
        .order_by(desc("last_seen"))
        .all()
    )

    map = folium.Map(
        location=current_app.config.get("MAP_CENTER"),
        zoom_start=current_app.config.get("MAP_ZOOM"),
    )
    for visitor in visitors:
        if visitor.latitude and visitor.longitude:
            icon_color = "green" if visitor.ip_address == remote_addr else "blue"
            folium.Marker(
                location=[visitor.latitude, visitor.longitude],
                icon=folium.Icon(color=icon_color),
                popup=f"Visits: {visitor.count}",
            ).add_to(map)
    map_html = map._repr_html_()

    return render_template(
        "index.html", ip=remote_addr, map_html=map_html, visitors=visitors
    )


@main.route("/ip")
def ip():
    remote_addr = utils.get_ip()

    if not utils.store_ip_address(remote_addr):
        return "Error retrieving location data", 500

    return remote_addr


@main.route("/healthcheck")
def healthcheck():
    return "OK"
