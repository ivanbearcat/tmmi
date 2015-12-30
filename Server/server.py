#!/usr/bin/env python3
# coding : utf8

from http.server import BaseHTTPRequestHandler, HTTPServer
# attention:this 'Server.' caused by project structure.It should be deleted when you deploy it on production
import Server.machine as machine
import Server.LIB as LIB

# it will be input from commandline
password = 'thisIsTest'


def readIPHosts():
    """read host-ip map
    todo:
        encrypt data
    data format:
        hostname ip comment
    """
    machines = machine.MachineGroup()

    with open('database', 'r')as f:
        while 1:
            line = f.readline()
            if not line:
                break
            temp = line.split(' ')
            amachine = machine.Machine()
            amachine.hostName = temp[0]
            amachine.IP = temp[1]
            amachine.comment = temp[2]
            machines.updateMachine(amachine)
    return machines


class TmmiTCPHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print('connected by ', self.client_address[0])
        request = self.request.recv(1024)
        form = request.decode('utf8').split('\r\n')
        idx = form.index('') + 1
        postString = self.filterPostData(form[idx:])
        if postString is not None:
            amachine = machine.Machine()
            resultCode = self.analysisPostDataAndAct(postString, amachine)
            self.response(resultCode, amachine)
        else:
            # todo :raise exception
            print('error')

    def filterPostData(self, postForm):
        for x in postForm:
            if x == '':
                postForm.remove(x)
        if postForm:
            return postForm[0]
        return None

    def analysisPostDataAndAct(self, postString, amachine):
        """To find out the action which user wants to take
        dataStructure:
            hostname=aname&ip=ip&comment=ct&password=passwd
        Returns:
            1: update machine's information successfully
            2: add machine successfully
            3: wrong password
            4: not find this hostname
        """
        temp = postString.split('&')
        tLen = len(temp)
        if tLen == 4:
            # todo: verify that the data is legitimate
            if self.verifyPassword(temp[3]):
                bmachine = machine.Machine()
                bmachine.hostName = temp[0]
                bmachine.IP = temp[1]
                bmachine.comment = temp[2]
                result = machines.updateMachine(bmachine)
            else:
                result = 3
        # tell me my ip
        elif tLen == 2:
            if (self.verifyPassword(temp[1])):
                hostname = temp[0]
                amachine = machines.getMachine(hostname)
                if amachine is None:
                    result = 3
                else:
                    result = 5
            else:
                result = 3
        return result

    def verifyPassword(self, str):
        return True

    def response(self, resultCode, amachine):
        # illegal operation code
        if 0 < resultCode < LIB.LEGALOPERATIONCODEUPPERLIMIT:
            self.send_header('Content-type', 'text')
            self.end_headers()
            self.send_response(200)
            writeBackInfor = LIB.RESPONSEMESSAGE[resultCode]
            if resultCode == 5:
                writeBackInfor = amachine.getString()
            self.wfile.write(writeBackInfor)
            self.wfile.close()
        else:
            self.send_error(204)

        return True


if __name__ == '__main__':
    global machines
    machines = readIPHosts()
    try:
        server = HTTPServer((LIB.HOST, LIB.PORT), TmmiTCPHandler)
        print('server started on port ', LIB.PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.server_close()