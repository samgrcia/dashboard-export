#!/usr/bin/python3

import requests
import json
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

"""
Type : Class 
Name : GrafanaInstance
Description : Represents a Grafana instance. 
"""
class GrafanaInstance:
    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey
        self.headers = {"Authorization":f"Bearer {self.apikey}", 'Content-Type':'application/json'}
        self.dashboards = sorted(self.gatherDashboards())

    """
    method gatherDashboards()
    Collect all dashboards from the Grafana server.
    arguments: self
    return: list of tuple (int,int,string)
    """
    def gatherDashboards(self):
        endpoint = "api/search"
        
        r = requests.get(f'{self.url}/{endpoint}', headers=self.headers)
        if r.status_code != 200:
            print(f'ERROR: status code = {r.status_code}. Content : {r.content}')
            sys.exit(1)
        
        return [(dash['id'],dash['uid'],dash['title']) for dash in r.json() if dash['type'] == 'dash-db']
    
    """
    method downloadDashboards(l)
    Download multiple dashboards specified from a list. 
    arguments: self, list of int
    return: nothing
    """
    def downloadDashboards(self, l):
        endpoint = "api/dashboards/uid"
        charToRemove = ['(',')']

        wanted = [int(dashId) for dashId in l.split(',')]
        for uid in [dashTuple[1] for dashTuple in self.dashboards if dashTuple[0] in wanted]:
            print(f"Working on {uid}...")
            r = requests.get(f'{self.url}/{endpoint}/{uid}', headers=self.headers)
            if r.status_code != 200:
                print(f'ERROR: status code = {r.status_code}. Content : {r.content}')
                sys.exit(1)
            jsonDashboard = r.json()['dashboard'] 
            
            filename = f"{jsonDashboard['title'].lower().replace(' ','-')}"
             
            for c in charToRemove:
                filename = filename.replace(c,'')
    
            with open(f"{OUTPUTDIR}/{filename}.json", 'w') as outfile:
                outfile.write(json.dumps(jsonDashboard, indent=4))

    """
    method downloadAllDashboards()
    Download all available dashboards. 
    arguments: self
    return: nothing
    """    
    def downloadAllDashboards(self):
        endpoint = "api/dashboards/uid"
        charToRemove = ['(',')']

        for uid in [dashTuple[1] for dashTuple in self.dashboards]:
            print(f"Working on {uid}...")

            r = requests.get(f'{self.url}/{endpoint}/{uid}', headers=self.headers)
            if r.status_code != 200:
                print(f'ERROR: status code = {r.status_code}. Content : {r.content}')
                sys.exit(1)

            jsonDashboard = r.json()['dashboard'] 
            # Clean the dashboard name
            filename = f"{jsonDashboard['title'].lower().replace(' ','-')}"
            for c in charToRemove:
                filename = filename.replace(c,'')

            with open(f"{OUTPUTDIR}/{filename}.json", 'w') as outfile:
                outfile.write(json.dumps(jsonDashboard, indent=4))
    """
    method printDashboards()
    Pretty print available dashboards. 
    arguments: self
    return: nothing
    """    
    def printDashboards(self):
        print(f'+{"-"*9}+{"-"*52}+')
        print(f'| {"ID":^7} | {"Dashboard Name":<50} |')
        print(f'+{"-"*9}+{"-"*52}+')
    
        for dash in self.dashboards:
            print(f'| {dash[0]:^7} | {dash[2]:<50} |')
        
        print(f'+{"-"*9}+{"-"*52}+')
    
def main():
     
    # Parse arguments
    parser = ArgumentParser(description="Download and save Grafana dashboards into a file. "
                                    "Dashboards are saved in a JSON format.\nTo authenticate "
                                    "the server, you need a valid API key.",
                            epilog = "Exemple :\n\n"
                                "* List available dashboards :\n "
                                "   dashboard-export.py -l https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='\n\n"
                                "* Download all available dashboards :\n"
                                "   dashboard-export.py -D https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='\n\n"
                                "* Download all available dashboards in /tmp/backup :\n"
                                "   dashboard-export.py -D -o /tmp/backup https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='\n\n"
                                "* Download only dashboards with id 1, 22 and 23. Use -l argument to get the id list :\n"
                                "   dashboard-export.py -d 1,22,33 https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("url", help="The Grafana server url. Use the following format : 'http://server:port'.")
    parser.add_argument("apikey", help="The API key to authenticate the server.")
    parser.add_argument('-d', 
                        help="Download only the following id list. Use comma separated integers.",
                        metavar='1,2,3,...', 
                        dest='opt_download', 
                        action='store')
    parser.add_argument('-D', 
                        help="Download all available dashboards.",
                        dest='opt_download_all', 
                        action='store_true')
    parser.add_argument('-l', 
                        help="List all available dashboards.",
                        dest='opt_list', 
                        action='store_true')
    parser.add_argument('-o', 
                        help="Specify a custom output directory. Default : './output'.",
                        metavar='directory', 
                        dest='opt_output', 
                        action='store', 
                        default='./output')
    args = parser.parse_args()
    global OUTPUTDIR
    OUTPUTDIR = args.opt_output
    
    g = GrafanaInstance(args.url, args.apikey)
    
    """
    Case '-D' : Download all graphs.
    """
    if args.opt_download_all: 
        g.downloadAllDashboards()
        exit(0)    

    """
    Case '-d' : Download only specified graphs.
    """
    if args.opt_download is not None: 
        g.downloadDashboards(args.opt_download)
        exit(0)    

    """
    Case '-l' : List all graphs.
    """
    if args.opt_list:
        g.printDashboards()
        exit(0)
    
    # Default behavior 
    print('Please specify -D or -d or -l.')
    
if __name__ == "__main__":
    main()
