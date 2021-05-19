#Import Libraries
import maes
from array import array
import textwrap
import json

#Set your key and initialization vector as variable.
#Optionally as a more secure option these files can be read from pem file.
key = b'\xf8\xfe]\xad\xa5I\xcd\x83\xdf\xfd\xc9\x14\nI\xba\x01'
iv = b'\xde\xce\xa4@B\xeaC\xd4\x03\xe1?\xb8\x0b{>I'
decryptor = maes.new(key, maes.MODE_CBC, IV=iv) #Initialize the AES-128-CBC class from library

def array_tostring(array_data):
  _string = ""
  for _array in array_data:
    _string = _string + chr(_array)
  return _string

def getnumbers(decryptedstr):
    divided = textwrap.wrap(decryptedstr,11) #Divide string into pieces of at least 11 characters
    el = [] #Create an empty list
    for n in divided:
        el.append(n[n.find("+") + 1: n.find("$")]) #Append the values between + and $ to the list
    el+="iot/temperature","iot/humidity",'iot/pressure' #Append the measurement topics to the list
    return el

def decrypt(secret):
    ret = json.loads(secret) #Get the integers inside of the list
    decrypted = array_tostring(decryptor.decrypt(ret)) #Decode and strip using the array_tostring function
    return  getnumbers(decrypted)
