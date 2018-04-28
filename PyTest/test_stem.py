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

    print("Tor is running version %s" % controller.get_version())
    print("Tor is running pid %s" % controller.get_pid())
    
    circuits = controller.get_circuits()
    print('circuits=')
    print(circuits)
    cidList = []
    for c in circuits:
        print ('c: id={0}, status={1}'.format(c.id, c.status))
        cidList.append(c.id)

    for cid in cidList:
        controller.close_circuit(cid)
    print ('close all circuit')

    circuits = controller.get_circuits()
    print('circuits=')
    print(circuits)

    streams = controller.get_streams()
    print('streams=')
    print(streams)
    for s in streams:
        print ('s=' + str(s))

    #controller.signal('HALT')
    #print("Tor is halt" )
    controller.close()
