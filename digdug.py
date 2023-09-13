from multiprocessing.pool import ThreadPool
import pandas as pd
import subprocess
import logging
import argparse
import sys
import re
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')


def argumentParser():
    logging.debug('parsing cmd arguments')
    VERSION  = '1.0'
    parser = argparse.ArgumentParser(
          description=f'''

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
                Version: {(VERSION)}
        ''', 
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('query', choices=['res', 'rdns'], help='Resolve either domain or reverse dns')
    parser.add_argument('-f', '--file', nargs='?',dest='file', help='file containing ip-addresses or domains', type=str)
    parser.add_argument('-t', '--thread', nargs='?', dest='threads', help='Threads launched', type=int, default=4)
    parser.add_argument('-o', '--output', nargs='?', dest='output', help='Threads launched', type=str, default='digdug-output')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args


def xlsxWriter(output, data):
    output = output + '.xlsx'
    for key, items in data.items():
        if key == 'resolved':
            df_resolved = pd.DataFrame(columns=['Host', 'Result'])
            for values in items:
                host, result = values.split(':')
                result, _ = re.subn('[\[\]\t]', '', result)
                row = {'Host': host, 'Result':result}
                df_row = pd.DataFrame([row])
                df_resolved = pd.concat([df_resolved, df_row], ignore_index=True)
                
        else:
            df_unresolved = pd.DataFrame(columns=['Host', 'Result'])
            for values in items:
                host, result = values.split(':')
                row = {'Host': host, 'Result':result}
                df_row = pd.DataFrame([row])
                df_unresolved = pd.concat([df_unresolved, df_row], ignore_index=True)
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_resolved.to_excel(writer, sheet_name='Resolved', index=False)
            df_unresolved.to_excel(writer, sheet_name='Unresolved', index=False)
    except Exception as e:
        logging.error(f'{e}')
    logging.info(f'output written to: {output}')


def outputWriter(output, data):
    for key, result in data.items():
        with open(f'{output}-{key}', 'a') as file:
            for record in result:
                file.write(str(record)+'\n')
        logging.info(f'output written to: {output}-{key}')


def stdoutParse(header, result):
    if result:
        stdout = f'{header}:[\n{result}\n]' 
    else:
        stdout = f'{header}:""' 
    return stdout


def resultsParser(results, output):
    resolved = []
    unresolved = []
    resolver = {
        'resolved':[],
        'unresolved':[]
    }
    for result in results:
        result = result.replace('\n','\n\t')
        result = result.replace('.\n','\n')
        if result.endswith('.'):
            result = result.rstrip('.')
        if ':""' in result or ":''" in result:
            unresolved.append(result)
        else:
            resolved.append(result)
    logging.info(f'resolved items: {len(resolved)}')
    logging.info(f'unresolved items: {len(unresolved)}')
    resolver['resolved'].extend(resolved)
    resolver['unresolved'].extend(unresolved)
    outputWriter(output, resolver)
    xlsxWriter(output, resolver)
    logging.info('done')


def subPopen(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()


def resolver(command):
    retry = 0
    if '-x' == command[2]:
        title = 'rdns'
    else:
        title = 'res'
    logging.info(f'{title}: {command[-1]}')
    while retry < 3:
        result = subPopen(command)
        if ';;' not in result:
            break
        retry += 1
    return stdoutParse(command[-1], result)
    

def fileReader(file):
    hosts = []
    with open(file) as items:
        for host in items:
            if host != '':
                hosts.append(host.strip())
    return hosts


def main(args):
    results = []
    if args.file and args.query in ['res','rdns']:
        if os.path.isfile(args.file):
            hosts = fileReader(args.file)
            with ThreadPool(args.threads) as pool:
                if args.query == 'res':
                    results = pool.map(resolver, [(['dig', '+short', subdomain]) for subdomain in hosts])            
                if args.query == 'rdns':
                    results = pool.map(resolver, [(['dig', '+short', '-x', ip]) for ip in hosts])
            resultsParser(results, args.output)
        else:
            logging.critical(f'provided "{args.file}" does not exist')
    else:
        logging.critical('missing file containing ip or hostnames')
    sys.exit(0)


if __name__ == '__main__':
    args = argumentParser()
    main(args)
