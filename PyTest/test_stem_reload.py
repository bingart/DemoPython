import getpass
import sys

import stem
import stem.connection

from stem.control import Controller

if __name__ == '__main__':
    
    try:
        controller = Controller.from_port(address='127.0.0.1', port=9351)
    except stem.SocketError as exc:
        print("Unable to connect to tor on port 9351: %s" % exc)
        sys.exit(1)

    try:
        controller.authenticate()
    except stem.connection.MissingPassword:
        pw = ''

    controller.signal('RELOAD')
    print("Tor is reload" )
    controller.close()
