from opcua import ua
import digitalIO as io
import time

class PALinkerException:
    def __init__(self, server, Folder, idx, codename, index):
        self.server = server
        PAType_nodeid = self.server.get_node(ua.ObjectIds.BaseObjectType).get_child\
            (["%d:PneumaticActuatorType" % idx]).nodeid
        objects = Folder.add_object(idx, codename, objecttype=PAType_nodeid)

        self.Configuration = objects.get_child("0:Configuration")
        self.Information = objects.get_child("0:Information")
        self.Initiation = objects.get_child("0:Initiation")
        self.Initiation_Initiate = self.Initiation.get_child("0:Initiate")
        self.server.link_method(self.Initiation_Initiate, self.Initiation_Initiate_Method)

        self.Operation = objects.get_child("0:Operation")
        self.Operation_Target = self.Operation.get_child("0:Target")
        self.Operation_Move = self.Operation.get_child("0:Move")
        self.server.link_method(self.Operation_Move, self.Operation_Move_Method)

        self.Status = objects.get_child("0:Status")
        self.Status_Position = self.Status.get_child("0:Position")
        self.Status_isRunning = self.Status.get_child("0:isRunning")

        self._isRunning = False
        self._Position = False

        self.index = index

    def Initiation_Initiate_Method(self, parent):
        print("PA{} : Initiation".format(self.index))
        io.digitalWrite(self.index, 0)

    def Operation_Move_Method(self, parent):
        print("Operation")
        target = self.Operation_Target.get_value()
        print(target)
        print(self.index)
        print("---")
        io.digitalWrite(self.index, int(target))


if __name__ == '__main__':
    print("PA")