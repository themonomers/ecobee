import requests
import json

from Utilities import getToken, printJson

AUTH_URL = 'https://api.ecobee.com/token'
BASE_URL = 'https://api.ecobee.com/1/thermostat'

config = getToken()
REFRESH_TOKEN = config['ecobee']['refresh_token']
API_KEY = config['ecobee']['api_key']
ACCESS_TOKEN = config['ecobee']['access_token']


##
#
#
##
def getThermostatInfo():
  try:
    body = {'selection': {'selectionType': 'registered', 'selectionMatch': '', 'includeRuntime': 'true'}}

    url = (BASE_URL
           + '?format=json'
           + '&body=' + str(body))

    response = json.loads(
      requests.get(
        url,
        headers={'authorization': 'Bearer ' + ACCESS_TOKEN}
      ).text
    )

    return response
  except Exception as e:
    print('getThermostatInfo(): ' + str(e))


##
#
#
##
def getToken():
  try:
    url = (AUTH_URL
           + '?grant_type=refresh_token'
           + '&code='
           + REFRESH_TOKEN
           + '&client_id='
           + API_KEY)

    response = requests.post(
                 url
               ).text

    return json.loads(response)
  except Exception as e:
    print('getToken(): ' + str(e))


def main():
  print('[1]  getToken()')
  print('[2]  getThermostatInfo()')

  try:
    choice = int(input('selection: '))
  except ValueError:
    return

  if choice == 1:
    data = getToken()
  elif choice == 2:
    data = getThermostatInfo()

  printJson(data, 0)


if __name__ == "__main__":
  main()
