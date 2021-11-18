import argparse
from Montoring import montioring

def main():
    montioring(get_args())

def get_args():
    parser = argparse.ArgumentParser(description='Website monitor', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--url',type=str, required=True, help='Website which will be monitored')
    parser.add_argument('--json_dump',type=int, required=False, default=0, help='Save results to file')
    parser.add_argument('--proxy',type=int, required=False, default=0, help='Use proxy')
    parser.add_argument('--sleep',type=int,required=False,default=15,help='Time (secs) between requests')
    return parser.parse_args()

if __name__ == '__main__':
    main()