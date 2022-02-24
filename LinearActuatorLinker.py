from opcua import ua, uamethod
import pyRSSeries.RSSeries as RS
import time

class LALinker:
    def __init__(self, server, Folder, idx, codename, index, port):
        self.c = RS.controller(port)
        self.server = server
        LAType_nodeid = self.server.get_node(ua.ObjectIds.BaseObjectType).get_child\
            (["%d:LinearActuatorType" % idx]).nodeid
        objects = Folder.add_object(idx, codename, objecttype=LAType_nodeid)

        self.Configuration = objects.get_child("0:Configuration")
        self.Information = objects.get_child("0:Information")

        self.Initiation = objects.get_child("0:Initiation")

        self.Operation = objects.get_child("0:Operation")
        self.Operation_toPoint = self.Operation.get_child("0:toPoint")
        self.Operation_Move = self.Operation.get_child("0:Move")
        self.server.link_method(self.Operation_Move, self.Operation_Move_Method)
        self.Operation_Stop = self.Operation.get_child("0:Stop")
        self.server.link_method(self.Operation_Stop, self.Operation_Stop_Method)

        self.Status = objects.get_child("0:Status")

        self.Status_Load = self.Status.get_child("0:Load")
        self.Status_OperationStatus = self.Status.get_child("0:OperationStatus")
        self.Status_Position = self.Status.get_child("0:Position")
        self.Status_Speed = self.Status.get_child("0:Speed")
        self.Status_Temperature = self.Status.get_child("0:Temperature")
        self.Status_Response = self.Status.get_child("0:Response")
        self.Status_Point = self.Status.get_child("0:Point")

    def Operation_Move_Method(self, parent):
        toPoint = self.Operation_toPoint.get_value()
        print("Move to", toPoint)
        self.c.move(str(toPoint))
        self.Status_Response.set_value(self.c.move_rsp)

    def Operation_Stop_Method(self, parent):
        print("Stop")
        self.c.stop()
        self.Status_Response.set_value(self.c.stop_rsp)

    def Status_Update(self):
        while True:
            if self.c.is_busy == 0:
                self.c.status()
                self.Status_Load.set_value(self.c.l_r)
                self.Status_OperationStatus.set_value(self.c.o_s)
                self.Status_Position.set_value(self.c.pos)
                self.Status_Speed.set_value(self.c.spd)
                self.Status_Temperature.set_value(self.c.tem)
                self.Status_Point.set_value(self.c.pt)
            time.sleep(1)

if __name__ == '__main__':
    print("LA")