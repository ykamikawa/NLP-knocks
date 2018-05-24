# jsonデータの読み込み
import gzip
import json

file_name = "../data/jawiki-country.json.gz"

with gzip.open(file_name, "rt") as f:
    for line in f:
        data_json = json.loads(line)
        if data_json["title"] == "イギリス":
            print(data_json["text"])
            break

