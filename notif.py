import json
import yaml


def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


def checkMatchers( matches ):
  if (len(matches) > 1):
    print('HEEY CHECK ME')

  # return (' '.join('"{0}"'.format(w) for w in words))
  # return (' '.join(['"%s"' % w for w in matches]))
  words = str((' '.join(matches[0])))
  return words


def createFile(dict):
  # yaml.add_representer(str, quoted_presenter)
  with open( 'test.yml', 'w') as yaml_file:
    yaml.dump(dict, yaml_file, default_flow_style=False)


# Load the JSON file
with open('routes.json', 'r') as f:
  data = json.load(f)

routes = data['route']

dict = {
  "apiVersion": 1,
  "policies" : []
}

mainData = {
  "orgId": 1,
  "receiver": routes['receiver'],
  "group_by": routes['group_by']
}

mainData['routes'] = []
forDictFirstRoutes = []
firstIndex = 0

for route in routes['routes']: # first routes

  firstMatchers = route['object_matchers']

  r = {
    'object_matchers': firstMatchers
  }

  if 'continue' in route:
    r['continue'] = route['continue']

  if 'receiver' in route:
    r['receiver'] = route['receiver']

  ## if object has mute intervals; please excite immediately
  if 'mute_time_intervals' in route:
    continue

  # mainData['routes'] = [r]

  forDictSecondRoutes = [];

  if ('routes' in route): # second routes
    secondIndex = 0
    for secondRoutes in route['routes']:
      
      rr = {
        'object_matchers': secondRoutes['object_matchers']
      }

      if 'continue' in secondRoutes:
        rr['continue'] = secondRoutes['continue']

      if 'receiver' in secondRoutes:
        rr['receiver'] = secondRoutes['receiver']
      else:
        print("no Receiver2")

      if 'mute_time_intervals' in secondRoutes:
        rr['mute_time_intervals'] = secondRoutes['mute_time_intervals']

      forDictSecondRoutes.append(rr)

      secondIndex +=1
  
  if 'receiver' not in r:
    print(firstMatchers)

  r['routes'] = forDictSecondRoutes

  firstIndex += 1
  mainData['routes'].append(r)

# print(mainData)

createFile(mainData)
