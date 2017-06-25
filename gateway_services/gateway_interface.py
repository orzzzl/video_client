from inventory import CAMERA_LIST
from gateway_services.gateway import Gateway

gateways = []

def init_gateways():
    for idx in CAMERA_LIST:
        gateways.append(Gateway(2, idx))

def get_gateways():
    return gateways

def stop_gateways():
    for g in gateways:
        g.set_off()

def start_gateways(session_id):
    for g in gateways:
        g.set_session_id(session_id)
        g.set_on()


