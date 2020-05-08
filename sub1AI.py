# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:14:47 2020

@author: Louis & Adrian
"""
import socket
import json
import sys
po=int(sys.argv[1])
s = socket.socket ()
s.connect(('localhost', 3001))
def sendJSON(socket, data):
	msg = json.dumps(data).encode('utf8')
	total = 0
	while total < len(msg):
		sent = socket.send(msg[total:])
		total += sent
info = {"matricules":["18190","18303"],"port": po,"name": "Personnage_Non_Joueur"}
sendJSON(s,info)