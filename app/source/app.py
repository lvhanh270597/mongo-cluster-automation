from config.config import *
# from lib.ssupport import SaltSupport
import salt.client


class App:

    def __init__(self):
        self.initSalt()    # Init salt
        self.mongoConfig() # Create and Share folder

    def initSalt(self):
        self.saltLocal = salt.client.LocalClient()
        info = self.saltLocal.cmd('*', 'test.ping')
        return info

    def getHosts(self):
        self.hosts = list(config["hosts"].keys())
        print 'master: ', config["master"]
        print 'slaves: ', config["slaves"]
        for i, host in enumerate(self.hosts):
            self.hosts[i] = host.encode('ascii', 'ignore')

    def mongoConfig(self):
         # Get all host, master, slave...
        self.getHosts() 
        
        # Create folder and mount share folder there
        self.createAndMount() 
        self.createCluster()
    
    def createAndMount(self):
        for host in self.hosts:
            sharepath = config["hosts"][host]["data"]["sharedir"]
            info = self.saltLocal.cmd(host, 'file.directory_exists', [sharepath])
            exist = info.values()[0]
            if not exist:
                print "Making dir '%s'" % sharepath
                self.saltLocal.cmd(host, 'file.makedirs', [sharepath])
            else:
                print "'%s' existed!" % sharepath
        
        self.installNFS()
        for host in self.hosts:
            sharepath = config["hosts"][host]["data"]["sharedir"]
            print "Umounting on dir '%s'" % sharepath
            print(self.saltLocal.cmd(host, 'cmd.run', ['umount %s' % sharepath]))
            print "Mounting on dir '%s'" % sharepath
            print(self.saltLocal.cmd(host, 'cmd.run', ['mount -t nfs %s:%s %s' % (SIPMASTER, SHAPATH, sharepath)]))
    
    def installNFS(self):
        for host in self.hosts:
            print(self.saltLocal.cmd(host, "cmd.run", ['yum -y install nfs-utils python3']))
            print(self.saltLocal.cmd(host, 'cmd.run', ["systemctl restart nfs-utils"]))

    def createCluster(self):
        sharepath = config["hosts"][config["master"]]["data"]["sharedir"]
        info = self.saltLocal.cmd(config["master"], "cmd.run", ['cd %s && ./main.py master init' % sharepath])
        print(info.keys()[0])
        print(info.values()[0])
        info = self.saltLocal.cmd(config["master"], "cmd.run", ['cd %s && ./main.py master create' % sharepath])
        print(info.keys()[0])
        print(info.values()[0])
        for i, server in enumerate(config["slaves"]):
            sharepath = config["hosts"][server]["data"]["sharedir"]
            info = self.saltLocal.cmd(server, "cmd.run", ['cd %s && ./main.py slave %d start' % (sharepath, i)])
            print(info.keys()[0])
            print(info.values()[0])
        sharepath = config["hosts"][config["master"]]["data"]["sharedir"]
        info = self.saltLocal.cmd(config["master"], "cmd.run", ['cd %s && ./main.py master add' % sharepath])
        print(info.keys()[0])
        print(info.values()[0])