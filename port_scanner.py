import socket, re
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose = False):
    target_is_hostname = re.search('[a-zA-Z]', target)
    ip_data = get_ip(target)
    if ip_data["url"] == None and ip_data["ip"] == None and target_is_hostname:
        return "Error: Invalid hostname"
    if ip_data["ip"] == None:
        return "Error: Invalid IP address"
    open_ports = scanPorts(ip_data, port_range)
    if verbose:
        msg = create_msg(ip_data, open_ports)
        return msg
    return(open_ports)

def scanPorts(ip_data, port_range):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    open_ports = []
    for key in ports_and_services:
        if(key >= port_range[0] and key <= port_range[1]):
            scanned_port = portScanner(s, ip_data["ip"], key)
            if(scanned_port):
                open_ports.append(scanned_port)
    return open_ports

def portScanner(s, target, port):
    if s.connect_ex((target, port)):
        print("The port is closed", port)
    else:
        print("Open Port", port)
        s.detach()
        return port

def get_ip(target):
    url =  None
    ip = None
    try:
        target_data = socket.gethostbyaddr(target)
        url = target_data[0]
    except:
        print("Can't get hostname")
    try:
        ip = socket.gethostbyname(target)
    except:
        print("Can't get ip")
    return {"url" : url, "ip": ip}

def create_msg(ip_data, ports):
    msg = ""
    if ip_data["url"]:
        msg += f"Open ports for {ip_data["url"]} ({ip_data["ip"]})"
    else: 
        msg += f"Open ports for {ip_data["ip"]}"
    msg += "\nPORT     SERVICE"
    for port in ports:
        msg += f"\n{port}      {ports_and_services[port]}"
    return msg
