import pandas as pd
from datetime import datetime
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent
_df_kodewilayah = pd.read_csv(
    _DATA_DIR / 'kodewilayah_2025.csv', index_col='kodewilayah'
)


def validator(ktp):
    ktp_str = str(ktp)
    return ktp_str.isdigit() and len(ktp_str) == 16


def locator(kodewilayah):
    try:
        row = _df_kodewilayah.loc[int(kodewilayah)]
        return pd.Series([True, row['provinsi'], row['kabupatenkota'], row['kecamatan']])
    except (KeyError, ValueError):
        return pd.Series([False, '', '', ''])


def gender_checker(digit):
    digit = int(digit)
    if 0 <= digit <= 3:
        return 'Pria'
    elif 4 <= digit <= 6:
        return 'Wanita'
    return 'Not Valid'


def dob_checker(dob_digits):
    dob = int(dob_digits)
    if dob > 400000:
        dob -= 400000
    try:
        return datetime.strptime(str(dob), '%d%m%y')
    except ValueError:
        return 'Not Valid'


def _process_ktp(df):
    ktp_str = df['ktp'].astype(str)

    df['valid'] = df['ktp'].apply(validator)
    df['kodewilayah'] = ktp_str.str[:6]
    df[['location_valid', 'provinsi', 'kabupatenkota', 'kecamatan']] = df['kodewilayah'].apply(locator)
    df['gender'] = ktp_str.str[6:7].apply(gender_checker)
    df['dob'] = ktp_str.str[6:12].apply(dob_checker)

    return df


def kuaci_ktp_check(df_ktp):
    if not isinstance(df_ktp, pd.DataFrame):
        raise TypeError('Input is not a pandas DataFrame')
    if len(df_ktp.columns) > 1:
        raise ValueError('Input DataFrame must have exactly 1 column')

    df = df_ktp.copy()
    df.columns = ['ktp']
    return _process_ktp(df)


def kuaci_ktp_check_single(ktp_number):
    if not isinstance(ktp_number, (int, str)):
        raise TypeError('Input must be an integer or string')

    df = pd.DataFrame({'ktp': [ktp_number]})
    return _process_ktp(df)
