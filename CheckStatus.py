from EcobeeAPI import getThermostatInfo

##
# Gets sensor data:  temperature and occupancy.
#
# author: mjhwa@yahoo.com
##
def getTemperatures():
  try:
    data = getThermostatInfo()

    temperature = 0.0
    occupancy = ''
    for x in data['thermostatList']:
      for y in x['remoteSensors']:
        for z in y['capability']:
          if z['type'] == 'temperature':
            temperature = round((float(z['value']) * 0.1), 1)
          if z['type'] == 'occupancy':
            occupancy = z['value']

        print(y['name'] + ': ' + str(temperature) + '°F (motion: ' + occupancy + ')')
  except Exception as e:
    print('getTemperatures(): ' + str(e))


def main():
  print('[1]  getTemperatures()')

  try:
    choice = int(input('selection: '))
  except ValueError:
    return

  if choice == 1:
    getTemperatures()


if __name__ == "__main__":
  main()