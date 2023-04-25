import requests
from bs4 import BeautifulSoup
import csv

LIST_KODE =['111', '112', '113', '114', '115', '116', '121', '122', '123', '131', '132', '133', '141', '142', '143', '144', '151', '152', '161', '171', '172', '181', '191', '192', '193', '311', '312', '321', '322', '323', '324', '331', '332', '333', '334', '335', '336', '341', '342', '351', '352', '353', '354', '355', '356', '357', '358', '361', '362', '363', '364', '365', '371', '372', '373', '374', '381', '382', '383', '384', '385', '386', '511', '521', '531', '532', '541', '542', '551', '611', '612', '613', '621', '631', '632', '711', '712', '713', '718', '721', '722', '731', '732', '741', '751', '752', '753', '811', '821', '911', '912', '913', '921']
rangkuman = []
for x in LIST_KODE:

    index_jur = 0
    kode_ptn = x

    KODE_JURUSAN = []
    tampung_2023 = []
    url = f"https://sidata-ptn-snpmb.bppp.kemdikbud.go.id/ptn_sb.php?ptn={kode_ptn}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                      "Safari/537.36 Edg/111.0.1661.41"
    }

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    item = soup.find_all("div", "tab-content")

    data_kode = []
    for it in item:
        table = it.find("table", "table table-striped vtop")
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [col.text.strip() for col in cols]
            data_kode.append(cols)

    index = 1

    for row in range(len(data_kode) - 1):
        cols = data_kode[index][1]
        tamp_2023 = data_kode[index][4]
        KODE_JURUSAN.append(cols)
        tampung_2023.append(tamp_2023)
        index += 1

    index_tamp = 0

    for i in KODE_JURUSAN:
        url_data = f"&prodi={i}&jenis=0"
        req = requests.get(url + url_data, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")

        item = soup.find_all("div", "panel panel-info")
        data = []
        for it in item:
            table = it.find("table", "table")
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols = [col.text.strip() for col in cols]
                data.append(cols)
        if "Baru diikutkan pada tahun 2023" in data[0]:
            data.pop(0)

        data_dict = {
            'kode': data[0][1],
            'program_studi': data[1][1],
            'jenjang': data[2][1],
            '[DT]2023': tampung_2023[index_tamp],
            '[JP]2022': data[5][5],
            '[DT]2022': data[6][5],
            '[JP]2021': data[5][4],
            '[DT]2021': data[6][4],
            '[JP]2020': data[5][3],
            '[DT]2020': data[6][3],
            '[JP]2019': data[5][2],
            '[DT]2019': data[6][2],
            '[JP]2018': data[5][1],
        }
        index_tamp += 1
        rangkuman.append(data_dict)
    print(f"aman bro {x}!!!")


# Get headers from keys of the first dict
headers = list(rangkuman[0].keys())

# Open csv file and write headers
with open('table.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    # Write data rows
    for row in rangkuman:
        writer.writerow(row)
