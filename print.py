#!/usr/bin/env python
#coding=utf-8

from prettytable import PrettyTable

x = PrettyTable(['#', 'Thread', 'Song', 'Time'])

x.align['Thread'] = "l"

x.padding_width = 1

with open('tmp.log') as f:
    cnt = 1
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        line = line.strip()

        parts = line.split()
        if len(parts) >= 9:
            thread, song, time = parts[6], parts[7], parts[8]
            x.add_row([cnt, thread, song, time])
            cnt += 1

print x
