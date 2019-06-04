import re
import pandas as pd
import requests
from datetime import datetime
from furl import furl


df_kodewilayah = pd.read_csv('kodewilayah_v2.csv', index_col='kodewilayah')


def facebook_search(name, key, em=True):
    f = furl('https://www.googleapis.com/customsearch/v1')
    f.args['key'] = key
    f.args['cx'] = '013743239855164640998:wdyn0oqb1ia'
    f.args['q'] = name
    if em:
        f.args['exactTerms'] = name
    f.args['siteSearch'] = 'www.facebook.com'

    ret = requests.get(f.url)
    result = ret.json()

    return ret.json()['queries']['request'][0]['totalResults']


def instagram_search(name, key, em=True):
    f = furl('https://www.googleapis.com/customsearch/v1')
    f.args['key'] = key
    f.args['cx'] = '013743239855164640998:wdyn0oqb1ia'
    f.args['q'] = name
    if em:
        f.args['exactTerms'] = name
    f.args['siteSearch'] = 'www.instagram.com'

    ret = requests.get(f.url)
    result = ret.json()

    return ret.json()['queries']['request'][0]['totalResults']


def google_search(name, key, em=True):
    f = furl('https://www.googleapis.com/customsearch/v1')
    f.args['key'] = key
    f.args['cx'] = '013743239855164640998:wdyn0oqb1ia'
    f.args['q'] = name
    if em:
        f.args['exactTerms'] = name

    ret = requests.get(f.url)
    result = ret.json()

    return ret.json()['queries']['request'][0]['totalResults']


def validator(ktp):

    if len(str(ktp)) != 16:
        return False
    else:
        return True


def locator(kodewilayah):

    kodewilayah = int(kodewilayah)

    try:
        df_tmp = df_kodewilayah.loc[kodewilayah]
        valid = True
        provinsi = df_tmp['provinsi']
        kabupatenkota = df_tmp['kabupatenkota']
        kecamatan = df_tmp['kecamatan']
    except KeyError as error:
        valid = False
        provinsi = ''
        kabupatenkota = ''
        kecamatan = ''
    finally:
        return pd.Series([valid, provinsi, kabupatenkota, kecamatan])


def gender_checker(gender_num):
    gender_num = int(gender_num)
    if gender_num in [0, 1, 2, 3]:
        return 'Pria'
    elif gender_num in [4, 5, 6]:
        return 'Wanita'
    else:
        return 'Not Valid'


def dob_checker(dob):
    dob = int(dob)
    if dob > 400000:
        dob = dob - 400000

    dob = str(dob)

    try:
        dateformat_dob = datetime.strptime(dob, '%d%m%y')
    except:
        dateformat_dob = 'Not Valid'
    return dateformat_dob


def kuaci_ktp_check(df_ktp):

    if not isinstance(df_ktp, pd.DataFrame):
        raise Exception('Input is not a pandas dataframe')
        if len(df_ktp.columns > 1):
            raise Exception('Input columns more than 1')

    df_ktp['ktp'] = df_ktp[df_ktp.columns[0]]

    if df_ktp.columns[0] != 'ktp':
        del df_ktp[df_ktp.columns[0]]

    df_ktp['valid'] = df_ktp['ktp'].apply(validator)
    df_ktp['kodewilayah'] = df_ktp['ktp'].astype(str).str[:6]
    df_ktp[['location_valid', 'provinsi', 'kabupatenkota', 'kecamatan']] = df_ktp['kodewilayah'].apply(locator)
    df_ktp['gender'] = df_ktp['ktp'].astype(str).str[6:7].apply(gender_checker)
    df_ktp['dob'] = df_ktp['ktp'].astype(str).str[6:12].apply(dob_checker)

    return df_ktp