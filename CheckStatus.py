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
      print('Overall: ' + str(round(float(x['runtime']['actualTemperature']) * 0.1, 1)) + '°F')

      for y in x['remoteSensors']:
        for z in y['capability']:
          if z['type'] == 'occupancy':
            occupancy = z['value']
          elif z['type'] == 'temperature':
            try:
              temperature = round((float(z['value']) * 0.1), 1)
            except ValueError:
              temperature = z['value']

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