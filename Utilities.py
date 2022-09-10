import configparser
import os

from Crypto import decrypt
from io import StringIO


##
# Retrieves dictionary of configuration values.
#
# author: mjhwa@yahoo.com
##
def getConfig():
  try:
    buffer = StringIO(
      decrypt(
        os.path.join(
          os.path.dirname(os.path.abspath(__file__)),
          'config.xor'
        ),
        os.path.join(
          os.path.dirname(os.path.abspath(__file__)),
          'config_key'
        )
      )
    )
    config = configparser.ConfigParser()
    config.sections()
    config.read_file(buffer)
    values = {s:dict(config.items(s)) for s in config.sections()}
    buffer.close()
    return values
  except Exception as e:
    print('getConfig(): ' + str(e))


##
# Retrievies dictionary of access token values.
#
# author: mjhwa@yahoo.com
##
def getToken():
  try:
    buffer = StringIO(
      decrypt(
        os.path.join(
          os.path.dirname(os.path.abspath(__file__)),
          'token.xor'
        ),
        os.path.join(
          os.path.dirname(os.path.abspath(__file__)),
          'token_key'
        )
      )
    )
    config = configparser.ConfigParser()
    config.sections()
    config.read_file(buffer)
    values = {s:dict(config.items(s)) for s in config.sections()}
    buffer.close()
    return values
  except Exception as e:
    print('getToken(): ' + str(e))


##
# Takes a JSON object and recursively prints out it's name/value pairs with
# indentation for each level.
#
# author: mjhwa@yahoo.com
##
def printJson(json_obj, level):
  offset = ''
  offset += '  ' * level

  if (isinstance(json_obj, dict) == True):
    for key in json_obj:

      value = json_obj[key]
      if ((isinstance(value, dict) == True) or (isinstance(value, list) == True)):
        print(offset + key)
        printJson(value, level + 1)
      else:
        print (offset + key + ' = ' + str(value))
  elif (isinstance(json_obj, list) == True):
    for x in json_obj:

      if (isinstance(x, list) == True):
        for key, value in x.items():
          print(offset + key)
          printJson(value, level + 1)
      else:
        printJson(x, level)
  else:
    print (offset + str(json_obj))
