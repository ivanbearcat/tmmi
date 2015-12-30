# coding:utf8


class Machine:
    def __init__(self):
        self.IP = ''
        self.hostName = ''
        self.comment = ''

    @staticmethod
    def getString(self):
        return self.hostName+'&'+self.IP+'&'+self.comment


class MachineGroup:

    def __init__(self):
        self.group = []

    def getMachine(self, hostName):
        for x in self.group:
            if x.hostName == hostName:
                return x
        return None

    def deleteMachine(self, hostName):
        for x in self.group:
            if x.hostName == hostName:
                self.group.remove(x)
                return True
        return False

    def updateMachine(self, aMachine):
        """更新设备信息
        如果已经存在这台设备，就更新信息，否则就添加新的信息
        Args:
            aMachine: a Machine instance needed inserting

        Returns:
            1: update machine's information successfully
            2: add machine successfully

        """
        for x in self.group:
            if x.hostName == aMachine.hostName:
                x.IP == aMachine.IP
                if aMachine.comment != None:
                    x.comment = aMachine.comment
                return 1
        self.group.append(aMachine)
        return 2



