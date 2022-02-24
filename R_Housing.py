from opcua import Server
from threading import *
from PneumaticActuatorLinker import PALinker
from PneumaticActuatorLinkerException import PALinkerException
from LinearActuatorLinker import LALinker
from Opti05Linker import OptiLinker
import time

server = Server()
server.set_endpoint("opc.tcp://192.168.50.14:4840")
server.import_xml('r_housing/PneumaticActuatorLinker.xml')
server.import_xml('r_housing/LinearActuatorLinker.xml')
server.import_xml('r_housing/Opti05Linker.xml')

idx = 0

objects = server.get_objects_node()
robot = objects.add_folder(idx, "robot")
devices = objects.add_folder(idx, "devices")

#PA3 = PALinker(server, devices, idx, "PA3", 3)
PA3 = PALinkerException(server, devices, idx, "PA3", 3)
PA4 = PALinker(server, devices, idx, "PA4", 4)
PA5 = PALinker(server, devices, idx, "PA5", 5)
PA6 = PALinker(server, devices, idx, "PA6", 6)

LA = LALinker(server, devices, idx, "LA", 10, "/dev/ttyUSB0")
#TLA = Thread(target=LA.Status_Update, args=())

Opti = OptiLinker(server, robot, idx, "Opti")

server.start()

while 1:
    print("open")
    time.sleep(5)
