'''
procesa datos de pm2.5 de la RAMA a un formato estándar
cambia nr por nan y el formato del horario a ISO

'''
from sys import argv
import datetime as dt

filename= argv[1]
outname = filename.split('_')
outname[0] = outname[0] + 'proc'
idpre = '_'.join(outname[:2])
outname = '_'.join(outname)
utc = -6

print (filename, outname)
col_data = 8
headerlen = 1

data = {}

with open(filename) as file:
    for i, line in enumerate(file):
        #skip header
        if i < headerlen:
            continue
        cols = line.split(',')
        if i == headerlen:
            continue
        idate = cols[0].split('-')
        idate = dt.datetime(int(idate[2]),
                            int(idate[1]),
                            int(idate[0]),
                            int(cols[1])-1,
                            )
        idate -= dt.timedelta(hours=utc)
        idate = idate.isoformat(timespec='seconds')
        idate += '{:03d}'.format(utc)
        idata = cols[col_data]
        if idata == 'nr':
            idata = 'nan'
        data[idate] = idata

print('saving', outname)
with open(outname, 'w') as file:
    print('id','fecha','pm2.5', sep=',', file=file)

with open(outname, 'a') as file:
    for k in data.keys():
        print(idpre, k, data[k], sep=',', file=file )

