# digdug
Quickie hack to dig multiple domains or IP-addresses listed in a file.


         _____  _       _____              
        |  __ \(_)     |  __ \             
        | |  | |_  __ _| |  | |_   _  __ _ 
        | |  | | |/ _` | |  | | | | |/ _` |
        | |__| | | (_| | |__| | |_| | (_| |
        |_____/|_|\__, |_____/ \__,_|\__, |
                   __/ |              __/ |
                  |____/             |____/ 
        ____________________________________                      
        ++++++++++++++++++++++++++++++++++++    
        ©2023 masterofbrainstorming
                    
    Quickie hack to dig with my own preferences
                Version: 1.0

## Installation

The script will require pandas and argparse in addition to python standard libraries. Script is written using python3.9 and works on Linux.

```bash
pip install -r requirements.txt
```

## Commandline arguments

```bash
positional arguments:
  {res,rdns}            Resolve either domain or reverse dns

optional arguments:
  -h, --help            show this help message and exit
  -f [FILE], --file [FILE]
                        file containing ip-addresses or domains
  -t [THREADS], --thread [THREADS]
                        Threads launched
  -o [OUTPUT], --output [OUTPUT]
                        Threads launched
```
python3.9 dig-py.py res -f domains -o example
## Usage:

The script will require certain parameters in order to work. 
You must specify: 
- positional argument
  -   res = resolve (file contents example: example.org)
  -   rdns = reverse dns (file contents example : 8.8.8.8)
- file (go to examples/)
- output (any name you come up with)

### Optional arguments
```
  -t [THREADS], --threads [THREADS]
                        Thread pool count for queries, default is 4
```

### res

Using to resolve domains and subdomains
```bash
digdug.py res -f domains -o example
2023-09-13 23:27:32,916 [INFO] - res: dsadadsa.casdas.com
2023-09-13 23:27:32,916 [INFO] - res: example.org
2023-09-13 23:27:32,916 [INFO] - res: gewtgrwgs.fdsod9s.com
2023-09-13 23:27:32,916 [INFO] - res: google.com
2023-09-13 23:27:33,079 [INFO] - resolved items: 2
2023-09-13 23:27:33,079 [INFO] - unresolved items: 2
2023-09-13 23:27:33,080 [INFO] - output written to: example-resolved
2023-09-13 23:27:33,080 [INFO] - output written to: example-unresolved
2023-09-13 23:27:33,173 [INFO] - output written to: example.xlsx
2023-09-13 23:27:33,173 [INFO] - done
```

### rdns
```bash
digdug.py rdns -f ips -o example
2023-09-13 23:30:13,597 [INFO] - rdns: 8.8.8.8
2023-09-13 23:30:13,597 [INFO] - rdns: 6.6.6.6
2023-09-13 23:30:14,015 [INFO] - resolved items: 1
2023-09-13 23:30:14,015 [INFO] - unresolved items: 1
2023-09-13 23:30:14,015 [INFO] - output written to: example-resolved
2023-09-13 23:30:14,015 [INFO] - output written to: example-unresolved
2023-09-13 23:30:14,107 [INFO] - output written to: example.xlsx
2023-09-13 23:30:14,107 [INFO] - done
```
