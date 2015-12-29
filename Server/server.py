#!/usr/bin/env python3
#coding : utf8

import socketserver
#attention:this 'Server.' caused by project structure.It should be deleted when you deploy it on production
import Server.machine as machine
HOST = ''
PORT = 12345

#it will be input from commandline
password = 'thisIsTest'

machines = None

def readIPHosts():
    """read host-ip map
    todo:
        encrypt data
    data format:
        hostname ip comment
    """
    machines = machine.machineGroup()

    with open('database', 'r')as f:
        while 1:
            line = f.readline()
            if not line:
                break
            temp = line.split(' ')
            amachine = machine.machine()
            amachine.hostName = temp[0]
            amachine.IP = temp[1]
            amachine.comment = temp[2]
            machines.updateMachine(amachine)
    return machines




class tmmiTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request = self.request.recv(1024)
        print('connected by ', self.client_address[0])
        print('request is ',request)

        method = request.decode('utf8').split(' ')[0]
        if method == 'POST':
            form = request.decode('utf8').split('\r\n')
            idx = form.index('')+1
            postString = self.filterPostData(form[idx:])
            if postString!=None:
                result = self.analysisPostDataAndAct(postString)


            else:
                #todo :raise exception
                print('error')
        else:
            print('Unsupport method')

    def filterPostData(self, postForm):
        for x in postForm:
            if x == '':
                postForm.remove(x)
        if postForm:
            return postForm[0]
        return None

    def analysisPostDataAndAct(self, postString):
        """To find out the action which user wants to take
        dataStructure:
            hostname=aname&ip=ip&comment=ct&password=passwd
        """
        temp = postString.split('&')
        if len(temp) == 4:
            #todo: verify that the data is legitimate
            if self.verifyPassword(temp[3]):
                amachine = machine.machine()
                amachine.hostName = temp[0]
                amachine.IP = temp[1]
                amachine.comment = temp[2]
                result = machines.updateMachine(amachine)
            else:
                #todo:raise exception
                print('wrong password')
        else:
            #todo: raise exception
            print('error')
        return result

    def verifyPassword(self, str):
        return True

    def response(self, resultCode):
        return True

if __name__ == '__main__':
    global machines
    machines = readIPHosts()

    server = socketserver.TCPServer((HOST, PORT), tmmiTCPHandler)
    server.serve_forever()