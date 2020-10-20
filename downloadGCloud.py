import requests
import pandas as pd
import datetime, os, time
from google.cloud import bigquery
import createImage
GOES_PUBLIC_BUCKET='gcp-public-data-goes-16'
outdir = '/media/emannuell/hd2/mayday/output/dataset/CMI/'

def get_objectId_at(dt, product='ABI-L2-CMIPF', channel='C11'):
    # get first 11-micron band (C14) at this hour
    # See: https://www.goes-r.gov/education/ABI-bands-quick-info.html
    # print('Looking for data collected on {}'.format(dt))
    dayno = dt.timetuple().tm_yday
    gcs_prefix = '{}/{}/{:03d}/{:02d}/'.format(product, dt.year, dayno, dt.hour)
    gcs_patterns = [channel, 's{}{:03d}{:02d}'.format(dt.year, dayno, dt.hour)]
    blobs = list_gcs(GOES_PUBLIC_BUCKET, gcs_prefix, gcs_patterns)
    if len(blobs) > 0:
        objectId = blobs[0].path.replace('%2F','/').replace('/b/{}/o/'.format(GOES_PUBLIC_BUCKET),'')
        return objectId
    else:
        print('No matching files found for gs://{}/{}* containing {}'.format(GOES_PUBLIC_BUCKET, gcs_prefix, gcs_patterns))
        return None

def list_gcs(bucket, gcs_prefix, gcs_patterns):
    import google.cloud.storage as gcs
    bucket = gcs.Client().get_bucket(bucket)
    blobs = bucket.list_blobs(prefix=gcs_prefix, delimiter='/')
    result = []
    for b in blobs:
        match = True
        # if not gcs_patterns[1] in b.path and str('C'+gcs_patterns[0]) in b.path:
        for pattern in gcs_patterns:
            if not pattern in b.path:
                match = False
        if match:
            result.append(b)
    return result

def copy_fromgcs(bucket, objectId, destdir):
    import google.cloud.storage as gcs
    bucket = gcs.Client().get_bucket(bucket)
    blob = bucket.blob(objectId)
    basename = os.path.basename(objectId)
    # print('Downloading {}'.format(basename))
    dest = os.path.join(destdir, basename)
    blob.download_to_filename(dest)
    return dest

def download_goes_nc(objectId, band, outdir):
    if objectId == None:
        print('Skipping GOES object creation since no GCS file specified')
        return
    
    if not os.path.exists(outdir + band):
        os.makedirs(outdir + band)
    local_file = copy_fromgcs('gcp-public-data-goes-16', objectId, outdir + band)
    # jpgfile = os.path.join(outdir + band, os.path.basename(outfilename))
    # print('Created from ', os.path.basename(local_file))
    return local_file


data = pd.read_csv('storm_list.txt', delimiter=",", header=None)
df = pd.DataFrame(data)
filterLines = df[(df[8] > 2017) & (df[9] == ' HU')]
# downloaded = ['BERYL', 'CHRIS', 'HELENE', 'FABIO', 'BUD', 'ALETTA', 'ISAAC', 'LESLIE', 'OSCAR', 'WILLA', 'SERGIO', 'JOHN', 'PABLO', 'JERRY', 'ALVIN', 'NANA', 'MARCO', 'LORENA', 'BARBARA', 'PAULETTE', 'DOUGLAS', 'MARIE', 'GENEVIEVE']
downloaded = []
for index, line in filterLines.iterrows():
    if not line[0].strip() in downloaded:
        client = bigquery.Client()
        quer = "SELECT name, latitude, longitude, iso_time, dist2land FROM `bigquery-public-data.noaa_hurricanes.hurricanes` WHERE season = '"+str(line[8])+"' AND name LIKE '"+line[0].strip()+"'"
        print(line[8], line[0])
        query_job = client.query(quer)  # Make an API request.
        bands = ['C15']
        # bands = ['C01', 'C02', 'C03']
        # ncFilesList = open('nc_file_list.txt', 'w')
        # print(query_job)
        for row in query_job:
            # print(row['iso_time'])
            # mixBands = []
            for band in bands:
                try:
                    objectId = get_objectId_at(row['iso_time'], channel=band)
                    fileName = outdir + band + '/' + objectId.split('/')[-1:][0]
                    if not os.path.exists(fileName):
                        bandFile = download_goes_nc(objectId, band, outdir)
                        print(fileName)
                except Exception as e:
                    time.sleep(3)
                    print(e)
                    # time.sleep(1)
            # print(int(row['iso_time'].timestamp()))
        # mixBands.append(bandFile)
    # ncFilesList.write('{}{:02d}{:02d}{:02d}{:02d}\n'.format(row['iso_time'].year, row['iso_time'].month, row['iso_time'].day, row['iso_time'].hour, row['iso_time'].second))
    # outfilename = os.path.join(outdir + 'images', '{}{:02d}{:02d}{:02d}{:02d}.jpg'.format(row['iso_time'].year, row['iso_time'].month, row['iso_time'].day, row['iso_time'].hour, row['iso_time'].second))
    # print(outfilename)
    # createImage.myRemapMix(mixBands[0], mixBands[1], mixBands[2], outfilename)

# ncFilesList.close()
# print(jpgfile)
# txtFile = requests.get('https://ftp.nhc.noaa.gov/atcf/index/storm_list.txt')
# print(txtFile.status_code)
# if txtFile.status_code != 200:
#     print('Download storm list error')
    # exit()

# print("Downloaded txtFile")
exit()
