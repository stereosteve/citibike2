import os
import sys
import glob
import multiprocessing
from zipfile import ZipFile
import csv
import json
from collections import Counter

in_dir = 'data/zip'
out_dir = 'data/csv'
os.makedirs(out_dir, exist_ok=True)


def extract_csv(zipname):
    z = ZipFile(zipname)
    for entry in z.infolist():
        # skip os files + editor working copies
        if entry.filename.startswith('20'):
            if os.path.isfile(os.path.join(out_dir, entry.filename)):
                continue
            print('extracting', entry.filename)
            z.extract(entry.filename, out_dir)


def extract_all():
    zipnames = [
        fn for fn in glob.glob(os.path.join(in_dir, '20*'))
        if '201307-201402' not in fn
    ]
    pool_size = multiprocessing.cpu_count()
    with multiprocessing.Pool(pool_size) as pool:
        pool.map(extract_csv, zipnames)


def find_headers():
    counter = Counter()
    c2 = Counter()
    c3 = Counter()
    for fn in glob.glob(os.path.join(out_dir, '*')):
        with open(fn, 'rt') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            # print(fn, row1)
            counter.update(row1)

            dest_names = [remap_column(c) for c in row1]
            c2.update(dest_names)
            # print(dest_names)

            c3.update([len(row1)])

    print(json.dumps(counter, indent=2))
    print(json.dumps(c2, indent=2, sort_keys=True))
    print(json.dumps(c3, indent=2))

    cols = sorted(list(c2.keys()))
    cols = [f' {c} String ' for c in cols]
    cols = ','.join(cols)
    sql = f'create table rides ( {cols} );'
    print(sql)
        


def remap_column(c: str):
    c = c.lower().replace(' ', '_')
    remap = {
        'end_station_latitude': 'end_lat',
        'end_station_longitude': 'end_lng',
        'start_station_latitude': 'start_lat',
        'start_station_longitude': 'start_lng',
        'bikeid': 'bike_id',
        'starttime': 'started_at', 
        'start_time': 'started_at',
        'stoptime': 'ended_at', 
        'stop_time': 'ended_at', 
        'tripduration': 'trip_duration', 
        'usertype': 'user_type',
    }
    return remap.get(c, c)

if __name__ == '__main__':
    extract_all()
    find_headers()