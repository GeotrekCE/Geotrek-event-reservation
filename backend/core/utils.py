
import csv
import io
from werkzeug.datastructures import Headers
from flask import Response


def to_csv_resp(filename, data, columns, separator=";"):
    headers = Headers()
    headers.add("Content-Type", "text/plain")
    headers.add("Content-Disposition", "attachment", filename="export_%s.csv" % filename)
    out = generate_csv_content(columns, data, separator)
    return Response(out, headers=headers)


def generate_csv_content(columns, data, separator):
    fp = io.StringIO()
    writer = csv.DictWriter(
        fp, columns, delimiter=separator, quoting=csv.QUOTE_ALL, extrasaction="ignore"
    )
    writer.writeheader()  # ligne d'entête

    for line in data:
        writer.writerow(line)
    fp.seek(0)  # Rembobinage du "fichier"
    return fp.read()  # Retourne une chaine


def transform_obj_to_flat_list(fields, data):
    flat_data = []
    for res in data:
        exp_res = {}
        for field in fields:
            tmp_res = res
            for i in field.split("."):
                atmp_res = tmp_res[i]
            exp_res[field] = tmp_res
        flat_data.append(exp_res)
    return flat_data
