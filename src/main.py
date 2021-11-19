import argparse
from Monitoring import monitoring

def main():
    monitoring(get_args())

def get_args():
    parser = argparse.ArgumentParser(description='Website monitor', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--url',type=str, required=True, help='Website which will be monitored')
    parser.add_argument('--output_json',type=int, required=False, default=0, help='Results to json')
    parser.add_argument('--json_pref',type=str, required=False, default='', help='File prefix')
    parser.add_argument('--output_folder',type=str, required=False, default='data/', help='File folder')
    parser.add_argument('--proxy',type=int, required=False, default=0, help='Use proxy')
    parser.add_argument('--sleep',type=int,required=False,default=25,help='Time (secs) between requests')
    return parser.parse_args()

if __name__ == '__main__':
    main()