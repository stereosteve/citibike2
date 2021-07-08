import os
import sys
import glob
import pyarrow
import pyarrow.parquet
import pandas as pd
import numpy as np
import multiprocessing
from zipfile import ZipFile

in_dir = 'data/zip/'
out_dir = 'data/parquet/'

old_schema = {
    'duration': float,
    'start_ts': str,
    'end_ts': str,
    'start_id': str,
    'start_name': str,
    'start_lat': float,
    'start_lng': float,
    'end_id': str,
    'end_name': str,
    'end_lat': float,
    'end_lng': float,
    'bike_id': str,
    'user_type': str,
    'birth_year': float,
    'gender': str,
}

new_schema = {
    'ride_id': str,
    'rideable_type': str,
    'start_ts': str,
    'end_ts': str,
    'start_name': str,
    'start_id': str,
    'end_name': str,
    'end_id': str,
    'start_lat': float,
    'start_lng': float,
    'end_lat': float,
    'end_lng': float,
    'member_casual': str
}


def csv_to_df(infile):
    header = pd.read_csv(infile, nrows=1)
    num_cols = len(header.columns)

    if num_cols == 15:
        schema = old_schema
    elif num_cols == 13:
        schema = new_schema
    else:
        assert(False)

    df = pd.read_csv(infile,
                     header=1,
                     names=list(schema.keys()),
                     dtype=schema,
                     infer_datetime_format=True,
                     parse_dates=['start_ts', 'end_ts'],
                     na_values=['\\N'])

    df.dropna(subset=['start_id', 'end_id'], inplace=True)

    if schema == old_schema:
        df.birth_year.fillna(0, inplace=True)
        # df.drop('duration', inplace=True, axis=1)

        df['is_member'] = df.user_type == 'Subscriber'
        df.drop('user_type', inplace=True, axis=1)

        df['rideable_type'] = ''
        df['ride_id'] = ''
    else:
        df['duration'] = (df.end_ts - df.start_ts).dt.total_seconds()

        df['is_member'] = df.member_casual == 'member'
        df.drop('member_casual', inplace=True, axis=1)

        df['bike_id'] = ''
        df['gender'] = ''
        df['birth_year'] = 0
        df['user_type'] = ''

    return df


def csv_to_parquet(infile):
    df = csv_to_df(infile)
    d = df.start_ts.iloc[0]
    parquet_file = f'{out_dir}{d.date()}.parquet'

    table = pyarrow.Table.from_pandas(df)
    pyarrow.parquet.write_table(
        table,
        parquet_file,
        use_deprecated_int96_timestamps=True,
    )

    return parquet_file


def zip_csv_to_parquet(zipname):
    z = ZipFile(zipname)
    for entry in z.infolist():
        # skip os files + editor working copies
        if entry.filename.startswith('20'):
            print('starting', entry.filename)
            csv_to_parquet(z.open(entry.filename))



def clean():
    list(map(os.remove, glob.glob(os.path.join(out_dir, '*.parquet'))))


def run():
    clean()
    os.makedirs(out_dir, exist_ok=True)

    zipnames = [
        fn for fn in glob.glob(os.path.join(in_dir, '20*'))
        if '201307-201402' not in fn
    ]

    with multiprocessing.Pool(4) as p:
        p.map(zip_csv_to_parquet, zipnames)


if __name__ == '__main__':
    run()
    # old = set(old_schema.keys())
    # new = set(new_schema.keys())
    # print(old - new)
    # print(new - old)
    # print(sorted(old | new))