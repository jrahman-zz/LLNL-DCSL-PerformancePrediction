#!/usr/bin/env python

import json
import sys

def main():
    json_path = sys.argv[1]
    app_name = sys.argv[2]
    with open(json_path, 'r') as f:
        data = json.load(f)
        print data['binaries'][app_name]

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Incorrect argument count')
    main()
