# dashboard-export
A python script to list and download dashboards from Grafana.

Tested with : 

* ✅ Grafana 8.2.4
* ✅ Python 3.6.8

## Usage 

```
dashboard-export.py [-h] [-d 1,2,3,...] [-D] [-l] [-o directory] url apikey

Download and save Grafana dashboards into a file. Dashboards are saved in a JSON format.
To authenticate the server, you need a valid API key.

positional arguments:
  url           The Grafana server url. Use the following format : 'http://server:port'.
  apikey        The API key to authenticate the server.

optional arguments:
  -h, --help    show this help message and exit
  -d 1,2,3,...  Download only the following id list. Use comma separated integers.
  -D            Download all available dashboards.
  -l            List all available dashboards.
  -o directory  Specify a custom output directory. Default : './output'.

Exemple :

* List available dashboards :
    dashboard-export.py -l https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='

* Download all available dashboards :
   dashboard-export.py -D https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='

* Download all available dashboards in /tmp/backup :
   dashboard-export.py -D -o /tmp/backup https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='

* Download only dashboards with id 1, 22 and 23. Use -l argument to get the id list :
   dashboard-export.py -d 1,22,33 https://grafana.server.local:3000  'eyJrIjoiaTxfQ=='
```