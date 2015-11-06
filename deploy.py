#!/usr/bin/python
# -*- coding:utf-8 -*-

import argparse
import os
from fabric.api import (
    execute,
    env,
    put,
    run,
    task
)
from consts import (
    USER,
    PASSWORD,
    CURRENT_PATH,
    REMOTE_PATH
)


def upload_agent():
    agent_file_path = os.path.join(
        CURRENT_PATH,
        'service_agent',
        'simple_agent.py')

    run('mkdir {}'.format(REMOTE_PATH))
    put(agent_file_path, REMOTE_PATH)


def start_agent(agent_file_path):
    run('python {} &'.format(agent_file_path))
    print "agent start success..."


@task
def deploy():
    upload_agent()
    start_agent(os.path.join(REMOTE_PATH, 'simple_agent.py'))


def main(hosts):
    hosts = hosts.split(',')
    env.user = USER
    env.password = PASSWORD
    execute(deploy, hosts=hosts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hosts', type=str, help='hosts to deply, split by `,`')
    args = parser.parse_args()
    main(args.hosts)
