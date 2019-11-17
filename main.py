#!/usr/bin/python3
from app.mongo import Mongo
import sys

class Main:

    def __init__(self):
        if sys.argv[1] == "master": 
            if sys.argv[2] == "init": 
                Mongo('master').init()
            else:
                if sys.argv[2] == "create":
                    Mongo('master').create()
                else:
                    if sys.argv[2] == "add":
                        Mongo('master').add()
                    else:
                        print("init, create or add?")
        else:
            if sys.argv[1] == "slave":
                index = int(sys.argv[2])
                if sys.argv[3] == "start":
                    Mongo('slave', index).start()
                else:
                    print("only option 'start'!")

Main()