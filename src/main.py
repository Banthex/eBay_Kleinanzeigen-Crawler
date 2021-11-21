import argparse
from re import T
from Monitoring import monitoring

def main():
    monitoring(get_args())

def get_args():
    parser = argparse.ArgumentParser(description='Website monitor', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--url',type=str, required=False, default='https://www.ebay-kleinanzeigen.de/s-pc-zubehoer-software/grafikkarten/anzeige:angebote/rtx/k0c225+pc_zubehoer_software.art_s:grafikkarten', help='Website which will be monitored')
    parser.add_argument('--output_json',type=int, required=False, default=0, help='Cache to json')
    parser.add_argument('--file_name',type=str, required=False, default='out', help='File name')
    parser.add_argument('--output_folder',type=str, required=False, default='data/', help='Output folder')
    parser.add_argument('--proxy',type=int, required=False, default=0, help='Use proxy')
    parser.add_argument('--sleep',type=int,required=False,default=25,help='Time (secs) between requests')
    parser.add_argument('--cache',type=int,required=False,default=50,help='Cache size')
    parser.add_argument('--log_level',type=int,required=False,default=0,help='Log level')
    parser.add_argument('--log_date_format',type=str,required=False,default='%H:%M',help='Logger date format')
    return parser.parse_args()

if __name__ == '__main__':
    main()