import requests
import json
import os

from Utilities import getToken, printJson
from Crypto import encrypt

AUTH_URL = 'https://api.ecobee.com/token'
BASE_URL = 'https://api.ecobee.com/1/thermostat'

config = getToken()
REFRESH_TOKEN = config['ecobee']['refresh_token']
API_KEY = config['ecobee']['api_key']


##
# Retrieves Ecobee thermostat data using their API and access token.
#
# author: mjhwa@yahoo.com
##
def getThermostatInfo():
  try:
    body = {'selection': 
             {'selectionType': 'registered', 
              'selectionMatch': '', 
              'includeRuntime': 'true',
              'includeSensors': 'true'
             }
           }

    url = (BASE_URL
           + '?format=json'
           + '&body=' + str(body))

    response = json.loads(
      requests.get(
        url,
        headers={'authorization': 'Bearer ' + getToken()['ecobee']['access_token']}
      ).text
    )

    # Detect expired token and re-auth
    if (response['status']['message'].strip() == 'Authentication token has expired. Refresh your tokens.'):
      refreshToken()
      return getThermostatInfo()

    return response
  except Exception as e:
    print('getThermostatInfo(): ' + str(e))


##
# Gets a new access token using the documented method on Ecobee's developer
# portal.  This will also write the new token into a local encrypted file
# for reuse. 
#
# author: mjhwa@yahoo.com
##
def refreshToken():
  try:
    url = (AUTH_URL
           + '?grant_type=refresh_token'
           + '&code='
           + REFRESH_TOKEN
           + '&client_id='
           + API_KEY)

    response = json.loads(
      requests.post(
        url
      ).text
    )

    message =  '[ecobee]\n'
    message += 'access_token=' + response['access_token'] + '\n'
    message += 'token_type=' + response['token_type'] + '\n'
    message += 'refresh_token=' + response['refresh_token'] + '\n'
    message += 'expires_in=' + str(response['expires_in']) + '\n'
    message += 'scope=' + response['scope'] + '\n'
    message += 'api_key=' + API_KEY + '\n'

    # Encrypt config file
    encrypt(
      message,
      os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'token.xor'
      ),
      os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'token_key'
      )
    )
  except Exception as e:
    print('refreshToken(): ' + str(e))


def main():
  print('[1]  getThermostatInfo()')

  try:
    choice = int(input('selection: '))
  except ValueError:
    return

  if choice == 1:
    data = getThermostatInfo()

  printJson(data, 0)


if __name__ == "__main__":
  main()
