#!/usr/bin/env python3
import json
import yaml
import re

def createFile(folderName):
  folderName = folderName.replace("|", " ")
  folderName = folderName.replace("_", "-")
  folderName = (folderName[:50]).rstrip()
  folderName = folderName.strip().lower()
  folderName = re.sub(r"\s+", "-", folderName)
  folderName = re.sub(r'--+', '-', folderName)

  if re.search(r'^.*?[^A-Za-z]$', folderName):
    folderName = folderName[:-1]

  with open( "us-prod-databases/" + folderName + '.yml', 'w') as yaml_file:
    yaml.dump(dict, yaml_file, default_flow_style=False)


# Load the JSON file
with open('us-prod-databases.json', 'r') as f:
# with open('general.json', 'r') as f:
  data = json.load(f)

folderName = 'us-prod-databases'
# folderName = 'Send_report'

# Dict = {1: 'Geeks', 2: 'For', 3: 'Geeks'}
for folder in data[folderName]:
  for rules in folder['rules']:
    dict = {
      "apiVersion": 1
    }

    groups = {
      "orgId": 1,
      "name": folderName,
      "folder": folderName,
      "interval": folder['interval']
    } 
    
    grafana_alert = rules['grafana_alert']
    group_rules = {
      "uid" : grafana_alert['uid'],
      "title": grafana_alert['title'],
      "condition": grafana_alert['condition'],
      "for": rules['for'],
      "isPaused": "false"
    }

    if 'no_data_state' in grafana_alert:
      group_rules['noDataState'] = grafana_alert['no_data_state']

    if 'exec_err_state' in grafana_alert:
      group_rules['execErrState'] = grafana_alert['exec_err_state']

    if 'labels' in rules:
      group_rules['labels'] = rules['labels']

    if 'annotations' in rules:
      group_rules['annotations'] = rules['annotations']

    if (grafana_alert['data']):
      group_rules['data'] = grafana_alert['data']


    groups['rules'] = [
      group_rules
    ]

    dict['groups'] = [
      groups
    ]

    createFile(grafana_alert['title'])




