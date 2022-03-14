import pandas as pd
import os
import sharepy

SHARE_POINT_BASE = "oeawacat.sharepoint.com"
SHARE_POINT_CREDENTIALS = {
    "username": os.environ.get('SP_USER'),
    "password": os.environ.get('SP_PW')
}
FILE_URL = "https://oeawacat.sharepoint.com/sites/ACDH-CH_p_EMT_FamiliensacheHandlungsspielraeumeEleonoraMagdalena/Freigegebene Dokumente/Transkribus/Gesamtliste korrigiert Letztstand Folderbereinigung.xlsx"
FILE_NAME = './tmp.xlx'
SHEET_NAME = 'gesamtliste_enriched'
CSV_NAME = './md.csv'

print(f"create connection to {SHARE_POINT_BASE}")
s = sharepy.connect(SHARE_POINT_BASE, **SHARE_POINT_CREDENTIALS)
print(f"downloading {FILE_URL} to {FILE_NAME}")
dl = s.getfile(FILE_URL, filename=FILE_NAME)
print(f"saving {FILE_URL} to {FILE_NAME}")

df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME)
df.to_csv(CSV_NAME, index=False)
os.remove(FILE_NAME)