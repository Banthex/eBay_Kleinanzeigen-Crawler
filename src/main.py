import argparse
from montoring import start_monitoring

def main():
    args = get_args()
    start_monitoring(args.url)

def get_args():
    parser = argparse.ArgumentParser(description='Website monitor', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--url',type=str, required=True, help='Website which will be monitored')
    return parser.parse_args()

if __name__ == '__main__':
    main()