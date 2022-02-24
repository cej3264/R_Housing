from opcua import ua
import Opti05Connector as o

class OptiLinker:

    def __init__(self, server, Folder, idx, codename):
        self.robot = o.OptiConnector()
        self.robot.start()
        print("Connected")

        self.server = server
        OptiType_nodeid = self.server.get_node(ua.ObjectIds.BaseObjectType).get_child\
            (["%d:Opti05Type" % idx]).nodeid
        objects = Folder.add_object(idx, codename, objecttype=OptiType_nodeid)

        self.Configuration = objects.get_child("0:Configuration")

        self.Information = objects.get_child("0:Information")

        self.Initiation = objects.get_child("0:Initiation")
        self.Initiation_Initiate = self.Initiation.get_child("0:Initiate")
        self.server.link_method(self.Initiation_Initiate, self.Initiation_Initiate_Method)

        self.Operation = objects.get_child("0:Operation")
        self.Operation_Move = self.Operation.get_child("0:Move")
        self.server.link_method(self.Operation_Move, self.Operation_Move_Method)
        self.Operation_M_Index = self.Operation.get_child("0:M_Index")
        self.Operation_Stay = self.Operation.get_child("0:Stay")
        self.server.link_method(self.Operation_Stay, self.Operation_Stay_Method)
        self.Operation_Stop = self.Operation.get_child("0:Stop")
        self.server.link_method(self.Operation_Stop, self.Operation_Stop_Method)
        self.Operation_Grip = self.Operation.get_child("0:Grip")
        self.server.link_method(self.Operation_Grip, self.Operation_Grip_Method)
        self.Operation_G_Index = self.Operation.get_child("0:G_Index")

        self.Action = objects.get_child("0:Action")
        self.Action_Start = self.Action.get_child("0:Start")
        self.server.link_method(self.Action_Start, self.Action_Start_Method)

        self.Status = objects.get_child("0:Status")
        self.Status_isRunning = self.Status.get_child("0:isRunning")
        self.Status_Cur_Angles = self.Status.get_child("0:Cur_Angles")
        self.Status_Cur_Location = self.Status.get_child("0:Cur_Location")
        self.Status_Speed = self.Status.get_child("0:Speed")
        self.Status_Acceleration = self.Status.get_child("0:Acceleration")
        self.Status_Apply = self.Status.get_child("0:Apply")
        self.server.link_method(self.Status_Apply, self.Status_Apply_Method)

    def Initiation_Initiate_Method(self, parent):
        print("Initiation_Initiate")
        self.robot.home()
        self.updateAngles()
        self.updateLocation()
        self.updateGripper()

    def Operation_Move_Method(self, parent):
        print("Operation_Move")
        M_Index = self.Operation_M_Index.get_value().split(" ")

        if M_Index[0] == "J":

            if M_Index[1] == "A":
                self.robot.movej(M_Index[2], M_Index[3], M_Index[4], M_Index[5], M_Index[6], M_Index[7])
            elif M_Index[1] == "R":
                now = self.robot.currAngles()
                self.robot.movej(str(float(now[0]) + float(M_Index[2])), str(float(now[1]) + float(M_Index[3])),
                                 str(float(now[2]) + float(M_Index[4])), str(float(now[3]) + float(M_Index[5])),
                                 str(float(now[4]) + float(M_Index[6])), str(float(now[5]) + float(M_Index[7])))
        elif M_Index[0] == "L":

            if M_Index[1] == "A":
                self.robot.movel(M_Index[2], M_Index[3], M_Index[4], M_Index[5], M_Index[6], M_Index[7])
            elif M_Index[1] == "R":
                now = self.robot.currLocation()
                self.robot.movel(str(float(now[0]) + float(M_Index[2])), str(float(now[1]) + float(M_Index[3])),
                                 str(float(now[2]) + float(M_Index[4])), str(float(now[3]) + float(M_Index[5])),
                                 str(float(now[4]) + float(M_Index[6])), str(float(now[5]) + float(M_Index[7])))

        self.updateAngles()
        self.updateLocation()
        self.updateGripper()

    def Operation_Stay_Method(self, parent):
        print("Operation_Stay")
        self.robot.stay()
        self.updateAngles()
        self.updateLocation()
        self.updateGripper()

    def Operation_Stop_Method(self, parent):
        print("Operation_Stop")
        self.robot.stop()
        self.updateAngles()
        self.updateLocation()
        self.updateGripper()

    def Operation_Grip_Method(self, parent):
        print("Operation_Grip")
        G_Index = self.Operation_G_Index.get_value()

        if G_Index == True:
            self.robot.gOpen()
        elif G_Index == False:
            self.robot.gClose()

        self.updateAngles()
        self.updateLocation()
        self.updateGripper()

    def Action_Start_Method(self, parent):
        print("Action_Start")
        path = open("opti_path_cej.txt", mode="rt")

        for txt in path:
            item = txt.split(" ")

            if item[0] == "J":
                if item[1] == "R":
                    now = self.robot.currAngles()
                    self.robot.movej(str(float(now[0]) + float(item[2])), str(float(now[1]) + float(item[3])),
                                     str(float(now[2]) + float(item[4])), str(float(now[3]) + float(item[5])),
                                     str(float(now[4]) + float(item[6])), str(float(now[5]) + float(item[7])))

                elif item[1] == "A":
                    self.robot.movej(item[2], item[3], item[4], item[5], item[6], item[7])

            elif item[0] == "L":
                if item[1] == "R":
                    now = self.robot.currLocation()
                    self.robot.movel(str(float(now[0]) + float(item[2])), str(float(now[1]) + float(item[3])),
                                     str(float(now[2]) + float(item[4])), str(float(now[3]) + float(item[5])),
                                     str(float(now[4]) + float(item[6])), str(float(now[5]) + float(item[7])))

                elif item[1] == "A":
                    self.robot.movel(item[2], item[3], item[4], item[5], item[6], item[7])

            elif item[0] == "T":
                self.robot.gOpen()

            elif item[0] == "F":
                self.robot.gClose()

            self.updateAngles()
            self.updateLocation()
            self.updateGripper()


    def Status_Apply_Method(self, parent):
        print("Status_Apply")
        self.robot.set_prof(self.Status_Speed.get_value(), self.Status_Acceleration.get_value())
        self.updateAngles()
        self.updateLocation()
        self.updateGripper()

    def updateAngles(self):
        self.currAngles = self.robot.currAngles()

        self.Status_Cur_Angles.set_value(self.currAngles[0] + " " + self.currAngles[1] + " " + self.currAngles[2] + " "
                                         + self.currAngles[3] + " " + self.currAngles[4] + " " + self.currAngles[5])

    def updateLocation(self):
        self.currLocation = self.robot.currLocation()

        self.Status_Cur_Location.set_value(self.currLocation[0] + " " + self.currLocation[1] + " " + self.currLocation[2] + " "
                                         + self.currLocation[3] + " " + self.currLocation[4] + " " + self.currLocation[5])

    def updateGripper(self):
        if self.robot.currGripper() == "-1":
            self.Operation_G_Index.set_value(True)
        elif self.robot.currGripper() == "0":
            self.Operation_G_Index.set_value(False)