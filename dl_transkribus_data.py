from io import BytesIO
import os
from urllib.request import urlopen
from zipfile import ZipFile

TRNANSKRIBUS_FOLDER = './transkribus_out'

os.makedirs(TRNANSKRIBUS_FOLDER, exist_ok=True )

TRANSKRIBUS_URL = "https://transkribus.eu/export/8280581275134541209/export_job_2759286.zip"

with urlopen(TRANSKRIBUS_URL) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(TRNANSKRIBUS_FOLDER)