import os
import requests
from bs4 import BeautifulSoup
import json


urls_list = [
    'http://localhost:61220/',
]

file_name = os.path.normpath('C:/logs/hdd_state.json')
logs_path = os.path.normpath('C:/logs')
lsi_log = 'bbu.log'
mega_cli = os.path.normpath('C:/scripts/Hpacucli/Bin/hpacucli.exe') + ' ctrl slot=0 show status > C:/logs/bbu.log'

hdd_state = []


def get_hdd_state(url):
    item = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    item['server_name'] = soup.body.div.div.div.contents[4].contents[1].contents[3].text.strip()
    item['bbu_state'] = ''
    item['disk_drive'] = []
    if True:
        os.chdir(logs_path)
        command = 'del ' + os.path.join(logs_path, lsi_log)
        os.system(command)
        command = mega_cli
        os.system(command)
        with open(os.path.join(logs_path, lsi_log), 'r') as f:
            for ff in f.readlines():
                if 'Battery' in ff:
                    item['bbu_state'] = ff.split()[2].strip()
                    break
        for item2 in soup.findAll('td', string='Health'):
            disk_drive = {}
            if 'Unknown' in item2.parent.contents[3].text:
                continue
            health = int(item2.parent.contents[5].text.split()[0])
            disk_drive['health'] = health
            drive_id = item2.parent.parent.parent.contents[2].find_next('td',
                                                                        string='Hard Disk Serial Number').nextSibling.nextSibling.text.strip()
            disk_drive['drive_id'] = drive_id
            item['disk_drive'].append(disk_drive)
        hdd_state.append(item)


def main():
    for item in urls_list:
        get_hdd_state(item)
    with open(file_name, 'w') as fp:
        json.dump(hdd_state, fp, indent=2)
    print(json.dumps(hdd_state, indent=2))


if __name__ == '__main__':
    main()
