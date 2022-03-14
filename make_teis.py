import glob
import jinja2
import os
import shutil
import pandas as pd
from acdh_tei_pyutils.tei import TeiReader
from dateutil.parser import parse, ParserError
from datetime import date
import lxml.etree as ET


templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('./templates/tei_template.xml')
out_folder = ('./data/tmp')

main_df = pd.read_csv('md.csv')
main_df = main_df[main_df['folder'].notna()]
filtered_df = main_df[main_df['folder'].str.startswith('Kasten_blau_45_9')]
# filtered_df = main_df
files = glob.glob('./transkribus_out/*/*.xml', recursive=True)
print(len(files))

shutil.rmtree(out_folder)
os.makedirs(out_folder, exist_ok=True)

for gr, df in filtered_df.groupby('folder'):
    file_name = f"{out_folder}/{gr}.xml"
    with open(file_name, 'w') as f:
        row = df.iloc[0]
        item = {}
        item['settlement'] = "München"
        item['repositor'] = "some archive in munich"
        item['id'] = gr.lower()
        item['file_name'] = f"{gr}.xml".lower()
        item['title'] = f"{row['weranwen']}, {row['Ort']} am {row['Datum']}"
        try:
            item['sender'] = row['weranwen'].split()[0]
        except:
            item['sender'] = 'NN'
        try:
            item['receiver'] = row['weranwen'].split()[-1]
        except:
            item['receiver'] = 'NN'
        item['place'] = row['Ort']
        item['writte_date'] = row['Datum']
        item['current_date'] = f"{date.today()}"
        try:
            item['parsed_date'] = parse(item['writte_date'])
        except:
            item['parsed_date'] = None
        item['pages'] = []
        for i, nrow in df.iterrows():
            f_name = f"{nrow['Dateiname'].split('.')[0]}"
            trs_file_name = f"./transkribus_out/*/{f_name}.xml"
            print(trs_file_name)
            print(glob.glob(f"./transkribus_out/*/{f_name}.xml"))
            try:
                legacy_xml_name = glob.glob(f"./transkribus_out/*/{f_name}.xml")[0]
            except IndexError:
                legacy_xml_name = False
            p = {}
            if legacy_xml_name:
                print(legacy_xml_name)
                doc = TeiReader(legacy_xml_name)
                facs = doc.any_xpath('.//tei:surface')[0]
                facs_string = ET.tostring(facs, encoding='utf-8', pretty_print=True).decode('utf-8')
                body = doc.any_xpath('.//tei:body/tei:div[1]')[0]
                body_string = ET.tostring(body, encoding='utf-8', pretty_print=True).decode('utf-8')
                p['facs_string'] = facs_string
                p['body_string'] = body_string
            p['width'] = nrow['width']
            p['height'] = nrow['height']
            p['url'] = f"https://iiif.acdh.oeaw.ac.at/kem/{f_name}"
            item['pages'].append(p)
        f.write(template.render(**item))
