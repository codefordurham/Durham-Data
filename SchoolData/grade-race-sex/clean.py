import pandas as pd
import numpy as np
import subprocess
import os.path
import argparse

parser = argparse.ArgumentParser('Download and clean attendance data from '
                                 'www.ncpublicschools.org')
parser.add_argument('year', type=int, help='school year to get data for')
parser.add_argument('-l', '--filter-leas', action='append', help='only include data from the LEAS')

# Cache and clean the data from North Carolina Department of Public Instruction
# (DPI)
# for school attendance by grade, race, and sex.

BASE_URL = "http://www.ncpublicschools.org/docs/fbs/accounting/data/"

try:
    base_path = __path__
except NameError:
    base_path = os.path.dirname(__file__)
CACHE_DIR = os.path.join(base_path, "cached")
CLEAN_DIR = os.path.join(base_path, "data")

def local_cache_file(year):
    two_digit = '{:02}'.format(year - 2000)
    return os.path.join(CACHE_DIR, 'grs{}.xls'.format(two_digit))
    
def ncdpi_url(year):
    two_digit = '{:02}'.format(year - 2000)
    return '{}grs{}.xls'.format(BASE_URL, two_digit)

def update_cache(year):
    url = ncdpi_url(year)
    return subprocess.check_call(['wget', '-P', CACHE_DIR, '-N', url])

def parse_school_attendance(year):
    assert year != 2008, 'data format in 2008 is very different and parser needs upgrade to handle.'
    fname = local_cache_file(year)

    sht_name = 'by School Grade'
    school_attendance = pd.read_excel(fname, sht_name, header=None)
    
    # clean up the 2 level headers to a proper and consistent column name
    cols = []
    for c in school_attendance.columns:
        col = school_attendance[c]
        _0 = col[0] if not pd.isnull(col[0]) else _0
        _1 = col[1]
        #print (_0, _1), ' - '.join((_0, _1))
        cols.append(('_'.join((_0, _1)))
                    .replace(' ', '_')
                    .replace('.', '')
                    .replace('__', '_')
                    )
        
    school_attendance.columns = cols
    school_attendance = school_attendance.ix[2:]
   
    # normalize column names
    school_attendance = school_attendance.rename(columns={
        'School_No': 'school_number',
        'School_Name': 'school_name',
        'SCH_No': 'school_number',
        'LEA_No': 'lea_number',
        'LEA_Name': 'lea_name',
        'Grade_Level': 'grade_level',

    })
        
    # clean Grade_Level
    # strip off leading 0 on grades 1-9
    school_attendance['grade_level'] = school_attendance.grade_level.map(
            lambda x: str(x).lstrip('0'))
    # normalize KI and K to 0 for kindergarden
    school_attendance['grade_level'] = school_attendance.grade_level.map(
         lambda x: '0' if str(x).startswith('K') else x)
    
    # clean LEA and school numbers
    school_attendance['lea_number'] = school_attendance.lea_number.map(str)
    def clean_school_no(x):
        tmp = str(x)
        if tmp == '0':
            return '000'
        else:
            return tmp
    school_attendance['school_number'] = school_attendance.school_number.map(clean_school_no)
    
    # augment with the school year.  This is year ending by convention (think graduating class)
    school_attendance['school_year'] = year
    
    # filter out rows that are blank or have extra headers
    # this occurs in at least 2012 in rows 13046 - 13049 (extra header with
    # blanks)
    school_attendance = school_attendance[~school_attendance.lea_number.isin(('',
                                                                           'LEA',
                                                                           'No'))]
    school_attendance = school_attendance[school_attendance.lea_name.notnull()]
    return school_attendance

def reshape(school_attendance):
    # reshape the data into a more normal form
    x = pd.melt(school_attendance, id_vars=['school_year', 'lea_name',
                                            'lea_number', 'school_number',
                                            'school_name', 'grade_level'])
    
    def get_sex(v):
        if v.endswith('_Male'):
            return 'Male'
        if v.endswith('_Female'):
            return 'Female'
        assert False, 'can not get here'

    def get_race(v):
        if v.endswith('_Male'):
            return v[:-5].replace('_', ' ')
        if v.endswith('_Female'):
            return v[:-7].replace('_', ' ')
        assert False, 'can not get here'
        # did not work
        #return v.rstrip('_Male').rstrip('_Female')
    
    x['sex'] = x.variable.map(get_sex)
    x['race'] = x.variable.map(get_race)
    x['attendance'] = x.value
    del(x['variable'])
    del(x['value'])  
    
    return x

if __name__ == '__main__':
    args = parser.parse_args()

    year = args.year
    filter_leas = args.filter_leas
    
    update_cache(year)

    base = parse_school_attendance(year)
    #base.to_csv('{}/{}-cleaned.csv'.format(CLEAN_DIR, year), index=False)
    
    attendance = reshape(base)
    attendance = attendance[['school_year', 'lea_number', 'school_number',
                             'grade_level', 'sex', 'race', 'attendance']]
    attendance = attendance[attendance.attendance!=0]
    if filter_leas:
        attendance  = attendance[attendance.lea_number.isin(filter_leas)]
    attendance.to_csv('{}/{}-attendance.csv'.format(CLEAN_DIR, year), index=False)

    leas = base[['school_year', 'lea_number', 'lea_name']].drop_duplicates()
    if filter_leas:
        leas  = leas[leas.lea_number.isin(filter_leas)]
    leas.to_csv('{}/{}-leas.csv'.format(CLEAN_DIR, year), index=False)

    schools = base[['school_year', 'lea_number', 'school_number', 'school_name']].drop_duplicates()
    if filter_leas:
        schools  = schools[schools.lea_number.isin(filter_leas)]
    schools.to_csv('{}/{}-schools.csv'.format(CLEAN_DIR, year), index=False)

    # need to take a look at the column types
    # 1. grade_level 
    #    -  note that the values are strings 0-12 and XDY 09 - XDY 12 
    #       cannot coerce to int.
    
