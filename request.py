#!/usr/bin/env python
#coding=utf-8

"""test php api"""

import time
import random
import httplib
import threading
import logging
import signal
from optparse import OptionParser

STOP = False
THREADS = []


def init_log(fname):
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s - %(process)-6d - %(threadName)-10s - %(levelname)-8s]\t%(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='%s' % fname,
        filemode='w')
    
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    sh.setFormatter(formatter)
    logging.getLogger('').addHandler(sh)


def sig_handler(sig, frame):
    global STOP
    STOP = True
    logging.info('stop server ...')


class search(threading.Thread):
    """test search song api"""
    def __init__(self, song, count, host):
        threading.Thread.__init__(self)
        self._song = song
        self._count = count
        self._host = host
        self._api = '/search/song.php?keyword='
        logging.info('new thread to host ...')


    def run(self):
        """read song.list sh""" 
        lines = []
    
        with open(self._song) as f:
            lines = f.readlines()
            random.shuffle(lines)

        cnt = 1
        for line in lines:
            time.sleep(random.random())
            line = line.strip()
            start = time.time()

            conn = httplib.HTTPConnection(self._host)
            conn.request("GET", self._api + line.strip())
            ret = conn.getresponse()

            cost = time.time() - start

            #!!!urgly
            thread = self.__str__().split(',')[0][8:]

            logging.info('%s\t%s\t%.4f' % (thread, line.replace(' ', '_'), cost))

            cnt += 1
            if self._count and cnt > self._count:
                break

     
def register_options():
    parser = OptionParser()
    parser.add_option('-t', '--thread', type='int', dest='thread',
                     default=2, help='thread num')
    parser.add_option('-c', '--count', type='int', dest='count',
                     default=10, help='song count')
    parser.add_option('-s', '--song', dest='song',
                     default='song.list', help='song list')
    parser.add_option('-i', '--host', dest='host', 
                     default='192.168.1.199', help='specify host')
    parser.add_option('-l', '--log', dest='log',
                     default='request.log', help='specify log')

    (options, args) = parser.parse_args() 
    return options


if __name__ == '__main__':
    
    opts = register_options()

    init_log(opts.log)

    logging.info('start ...')

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    for i in range(opts.thread):
        THREADS.append(search(opts.song, opts.count, opts.host))

    for i in THREADS:
        i.setDaemon(True)
        i.start()

    # master thread to catch signal
    while not STOP:
        time.sleep(0.01)

    logging.info('stop ...')
