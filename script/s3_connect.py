import os
from fyda import load_s3
from botocore.exceptions import ClientError


def main():

    try:
        print('Path-like load test:')
        x = load_s3(os.path.join('data', 'x.npy'),
                    bucket_name='renzmann-practice-bucket')
        print(x[:5])
    except ClientError as e:
        print('Path-like test failed, original error:', e)

    print('\nFull string load test:')
    x = load_s3('data/x.npy', bucket_name='renzmann-practice-bucket')
    print(x[:5])


if __name__ == '__main__':
    main()
