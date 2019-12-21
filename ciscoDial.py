#!/usr/bin/python

import sys
import os
import requests
import argparse

from xml.etree import ElementTree

from StringIO import StringIO

CUCUM="https://10.10.50.10/webdialer/services/WebdialerSoapService70"

def scriptPath():
   return  os.path.dirname(
       os.path.realpath(__file__))

def getXmlRequest(xml, data):

    file = open(xml, mode='r')
    content = file.read()
    file.close()
    return content % data

def getProfileSoap(userId, password, profileUserId):

    xml_file = os.path.join(scriptPath(), "getProfileSoap.xml")
    return getXmlRequest(xml_file, {
        "userId" : userId, "password" : password, "profileUserId" : profileUserId })

def getMakeCallSoap(userId, password, callerUserId, deviceName, lineNumber, destination):

    xml_file = os.path.join(scriptPath(), 'makeCallSoap.xml')

    return getXmlRequest(xml_file, {
        "userId" : userId,
        "password" : password,
        "callerUserId" : callerUserId,
        "deviceName" : deviceName,
        "lineNumber" : lineNumber,
        "destination" : destination
    })

def sendSoapEnvelope(envelope):

   headers = {'content-type': 'text/xml', 'SOAPAction': 'CUCM:DB ver=10.0'}
   r = requests.post(CUCUM, headers=headers, data=envelope, verify=False)

   return (r.status_code, r.content)


def getSoapNamespaces(response):

    my_namespaces = dict([
        node for _, node in ElementTree.iterparse(
            StringIO(response), events=['start-ns']
        )
    ])
    from pprint import pprint
    pprint(my_namespaces)



def getSoapResponseData(response,namespaces, data):

    dom = ElementTree.fromstring(response)
    names = dom.findall(
       data,
       namespaces
    )
    return names[0].text


parser = argparse.ArgumentParser(description='Effettua una chiamata con Cisco WebDialer in Python')
parser.add_argument("--username", help="Nome utente per l'autenticazione (o dell'utente proxy)", required=True)
parser.add_argument("--password", help="Password dell'utente per l'anticazione (o dell'utente proxy)", required=True)
parser.add_argument("--profile", help="Profilo (telefono) da cui eseguire la chiamata (predefinito username)", default=None)
parser.add_argument("--callto", help="Telefono da chiamare", required=True)

args = parser.parse_args()

#username=8140
#password=8140
#profile=8140
#callTo=8139

username=args.username
password=args.password
profile=args.profile
callTo=args.callto

if not profile:
    profile=username

responseDescription=None

try:

    res = sendSoapEnvelope( getProfileSoap(username, password, profile) )
    namespaces = { "ns": "urn:WD70" }

    deviceName = getSoapResponseData( res[1], namespaces, './/deviceName' )
    lineNumber = getSoapResponseData( res[1], namespaces, './/lines/item' )

    res = sendSoapEnvelope(
       getMakeCallSoap(username, password, profile, deviceName, lineNumber, callTo)
    )

    namespaces = { "ns": "WebdialerSoap" } 
    responseDescription = getSoapResponseData( res[1], namespaces, './/responseDescription' )

except Exception as e:
    pass

print responseDescription
sys.exit(int(responseDescription != "Success"))

