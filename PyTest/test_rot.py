import getpass
import sys

import stem
import stem.connection

from stem.control import Controller

def shutdown(controller):
    controller.signal('HALT')
    print("Tor is halt" )

def dump(controller):
    print("Tor is running version %s" % controller.get_version())
    print("Tor is running pid %s" % controller.get_pid())
    
    circuits = controller.get_circuits()
    print('circuits=')
    #print(circuits)
    cidList = []
    for c in circuits:
        print ('c: id={0}, status={1}, path={2}, purpose={3}'.format(c.id, c.status, c.path, c.purpose))
        cidList.append(c.id)

    streams = controller.get_streams()
    print('streams=')
    print(streams)
    for s in streams:
        print ('s: id={0}, circ_id={1}, source_address={2}, target_address={3}'.format(s.id, s.circ_id, s.source_address, s.target_address))

def closeCircuit(controller, cid):
    controller.close_circuit(cid)
    print ('close circuit {0}'.format(cid))

def closeAllCircuit(controller):
    circuits = controller.get_circuits()
    print('circuits=')
    print(circuits)
    cidList = []
    for c in circuits:
        cidList.append(c.id)

    for cid in cidList:
        controller.close_circuit(cid)
    print ('close all circuit')

def get_conf(controller, key):
    value = controller.get_conf(key)
    print ('get_config: key={0}, value={1}', key, value)

def set_conf(controller, key, value):
    controller.set_conf(key, value)
    print ('set_config: key={0}, value={1}', key, value)
    get_conf(controller, key)

def main():
    try:
        controller = Controller.from_port(address='127.0.0.1', port=9351)
    except stem.SocketError as exc:
        print("Unable to connect to tor on port 9351: %s" % exc)
        sys.exit(1)

    try:
        controller.authenticate()
    except stem.connection.MissingPassword:
        sys.exit(1)

    if len(sys.argv) == 1:
        print ('usage: py dump')
        print ('usage: py shutdown')
        print ('usage: py close_circuit cid')
        print ('usage: py close_all_circuit')
        print ('usage: py get_conf key')
        print ('usage: py set_conf key value')
        return

    if sys.argv[1] == 'dump':
        dump(controller)
    elif sys.argv[1] == 'shutdown':
        shutdown(controller)
    elif sys.argv[1] == 'close_circuit':
        closeCircuit(controller, sys.argv[2])
    elif sys.argv[1] == 'close_all_circuit':
        closeAllCircuit(controller)
    elif sys.argv[1] == 'get_conf':
        get_conf(controller, sys.argv[2])
    elif sys.argv[1] == 'set_conf':
        set_conf(controller, sys.argv[2], sys.argv[3])
    controller.close()

if __name__ == '__main__':
    main()
