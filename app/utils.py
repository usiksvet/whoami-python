import datetime
import ipaddress
import requests

from app import db
from app.models import Visitor


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
