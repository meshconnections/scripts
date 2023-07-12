#!/usr/bin/env python3
import json
import yaml
import re
import argparse
import sys

def createFile(folderName):
  folderName = folderName.replace("|", " ")
  folderName = folderName.replace("_", "-")
  folderName = (folderName[:50]).rstrip()
  folderName = folderName.strip().lower()
  folderName = re.sub(r"\s+", "-", folderName)
  folderName = re.sub(r'--+', '-', folderName)

  if re.search(r'^.*?[^A-Za-z]$', folderName):
    folderName = folderName[:-1]

  if args.directory:
    with open( args.directory + "/" + folderName + '.yml', 'w') as yaml_file:
      yaml.dump(dict, yaml_file, default_flow_style=False)
  else:
    with open(  folderName + '.yml', 'w') as yaml_file:
      yaml.dump(dict, yaml_file, default_flow_style=False)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", type=str, help="Directory where to dump converted yaml files")
parser.add_argument("-g", "--groupalerts", type=str, help="Name of the group/folder where you extracted the alerts")
parser.add_argument("-i", "--input", type=str, help="CASE SENSITIVE: Extracted json data of group alerts in API /api/ruler/grafana/api/v1/rules/<alert folder>")
args = parser.parse_args()

# Load the JSON file
if args.input is None:
  print("some expected arguments are missing, run --help")
  sys.exit(1)
else:
  with open(args.input, 'r') as f:
    data = json.load(f)


if args.groupalerts is None:
  print("some expected arguments are missing, run --help")
  sys.exit(1)
else:
  folderName = args.groupalerts
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
