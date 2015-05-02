#!/usr/bin/env python

import sys
import json
import subprocess
import logging

def help():
    print "runner app_name command_path dir_path size"
    return 1

def build_commands(app_name, dir_path, size, commands):
    commands = commands[size]
    commands = [command for command in commands if command['name'] == app_name]
    if len(commands) != 1:
        raise ValueError('Application %s not found' % (app_name))
    commands = ['cd %s && %s' % (dir_path, command) for command in commands[0]['cmds']]
    logging.info('App: %s, Commands: %s', app_name, str(commands))
    return commands


def run_commands(commands):
    for command in commands:
        subprocess.check_output(command, shell=True)

def main():
    if len(sys.argv) != 5:
        return help()
    with open(sys.argv[2], 'r') as f:
        config = json.load(f)
        commands = build_commands(sys.argv[1], sys.argv[3], sys.argv[4], config)
        run_commands(commands)
    return 0

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
