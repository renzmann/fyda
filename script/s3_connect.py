import os
import boto3
from io import BytesIO
import pickle
import numpy as np
import json
import pandas as pd


READER_MAP = {
    '.pkl': pickle.load,
    '.npy': np.load,
    '.json': json.load,
    '.xlsx': pd.read_excel
}


def load_s3_obj(filename, **kwargs):

    ext = os.path.splitext(filename)[-1]
    reader = READER_MAP[ext]
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('renzmann-practice-bucket')

    with BytesIO() as data:
        bucket.download_fileobj(filename, data)
        data.seek(0)    # move back to the beginning after writing
        obj = reader(data, **kwargs)

    return obj


def main():

    x = load_s3_obj(os.path.join('data', 'x.npy'))
    print(x[:5])


if __name__ == '__main__':
    main()
