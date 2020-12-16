#!/usr/bin/env python3
"""
This file transforms MOOSXXX.alog files to time-var.csv.
Therefore it uses alogsplit from the MOOS-IvP software.
Location of the MOOSXXX.alog is assumed to be in the current dir.
By Gerben Peeters
"""
from pathlib import Path
from subprocess import call
import glob
import os
import csv


if __name__ == '__main__':
    #
    # I. Split alog to klogs - moos-ivp software functions used
    #
    CUR_PATH = Path.cwd()
    os.chdir(CUR_PATH)
    for file in glob.glob("*.alog"):
        print('Found the following *alog file in ./ ')
        print(file)
    call(["alogsplit", file]) 
    print('Succesfully splitted ', file, 'into klog files')
    #
    # II. Convert klog (white space seperated) to csv
    #
    CSV_OUT_DIR = CUR_PATH / 'csv/'
    Path(CSV_OUT_DIR).mkdir(parents=True, exist_ok=True)
    MISSION = os.path.splitext(file)[0]
    K_DIR = MISSION + '_alvtmp'
    KLOGPATH = CUR_PATH / K_DIR
    klogs = os.listdir(KLOGPATH)
    # open every klog, delete whitespaces and save comma seperated
    for f in klogs:
        with open(os.path.join(KLOGPATH, f), 'r') as fin, open(
            os.path.join(CSV_OUT_DIR, os.path.splitext(f)[0] + ".csv"), 'w') as fout:
                # from white space
                reader = csv.reader(fin, delimiter=' ')
                # to csv
                writer = csv.writer(fout, delimiter=',')
                for row in reader:
                    row = list(filter(None, row))  # remove random whitespaces
                    writer.writerow(row)
    print('Succesfully converted klog to csv')
