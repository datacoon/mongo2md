from copy import copy
import os
import csv
import json
from random import randint
from pymongo import MongoClient
from ..scheme import generate_scheme, schema2fieldslist
from pprint import pprint
import configparser
from bson.json_util import loads, dumps


def coll2md(table, schema, fieldlist, example):
    md = ""
    md += "## Collection %s, %s\n%s\n" % (
        table["name"],
        table["displayName"],
        table["description"],
    )
    md += schema2md(schema, fieldlist, example)
    return md


def schema2md(schema, fieldlist, example=None, prefix=None):
    objects = []
    object = []
    if prefix is not None:
        md = '\n\n### <a name="%s"></a>%s (%s)\n' % (
            fieldlist[prefix]["name"],
            fieldlist[prefix]["name"],
            fieldlist[prefix]["description"],
        )
    else:
        md = "\n\n"
    subschemes = []
    md += "| Name        | Type           | Description  |\n"
    md += "| ------------- |:-------------:| -----:|\n"
    for k in schema.keys():
        if prefix is None:
            name = k
        else:
            name = ".".join([".".join(prefix.split(".")), k])
        if "schema" not in schema[k].keys():
            if schema[k]["type"] == "array":
                md += "| %s | %s | %s\n" % (
                    k,
                    "list of [%s]" % schema[k]["subtype"],
                    fieldlist[name]["description"],
                )
            else:
                md += "| %s | %s | %s\n" % (
                    k,
                    schema[k]["type"],
                    fieldlist[name]["description"],
                )
        else:
            if prefix is not None:
                subprefix = copy(prefix) + "." + k

            #                subprefix.append(k)
            else:
                subprefix = k
            if schema[k]["type"] == "dict":
                md += "| %s | %s | %s\n" % (
                    k,
                    "dict as [%s](%s)" % (subprefix, subprefix),
                    fieldlist[name]["description"],
                )
                subschemes.append([schema[k]["schema"], subprefix])
            elif schema[k]["type"] == "array":
                md += "| %s | %s | %s\n" % (
                    k,
                    "list of [%s](%s)" % (subprefix, subprefix),
                    fieldlist[name]["description"],
                )
                subschemes.append([schema[k]["schema"], subprefix])
    if example is not None:
        md += "\n#### Example\n"
        md += "```javascript\n"
        md += dumps(example, indent=4, sort_keys=True, ensure_ascii=False) + "\n"
        md += "```"
    for sub in subschemes:
        md += schema2md(sub[0], fieldlist=fieldlist, example=None, prefix=sub[1])
    return md


class Documenter:
    def __init__(self, project_path=None, host="localhost", port=27017):
        self.project_path = os.getcwd() if project_path is None else project_path
        self.config_filename = os.path.join(self.project_path, "apibackuper.cfg")
        self.host = host
        self.port = port
        pass

    def __read_config(self, filename):
        if os.path.exists(self.config_filename):
            config = configparser.ConfigParser()
            config.read(filename)
            return config
        return None

    def prepare_documents(
        self, dbname, collname=None, scheme_limit=1000, projpath=None, example=True
    ):
        """Generates mock files for Markdown generation"""
        self.conn = MongoClient(self.host, self.port)
        db = self.conn[dbname]
        if collname:
            collnames = [
                collname,
            ]
        else:
            collnames = db.list_collection_names()
        if projpath is None:
            projpath = dbname
        if not os.path.exists(projpath):
            os.mkdir(projpath)

        tables = []
        for name in collnames:
            tables.append({"name": name, "displayName": "", "description": ""})
            scheme = generate_scheme(db[name], alimit=scheme_limit)
            outfile = os.path.join(projpath, "%s_schema.json" % name)
            f = open(outfile, "w", encoding="utf8", newline="")
            f.write(json.dumps(scheme, indent=4, sort_keys=True))
            f.close()

            fieldslist = schema2fieldslist(scheme)
            outfile = os.path.join(projpath, "%s_fields.csv" % name)
            f = open(outfile, "w", encoding="utf8", newline="")
            wr = csv.DictWriter(
                f, delimiter=";", fieldnames=["name", "type", "description"]
            )
            wr.writeheader()
            wr.writerows(fieldslist)
            f.close()

            if example:
                total = db[name].count()
                entry = db[name].find().limit(-1).skip(randint(0, total - 1)).next()
                outfile = os.path.join(projpath, "%s_example.json" % name)
                f = open(outfile, "w", encoding="utf8", newline="")
                f.write(dumps(entry, indent=4, sort_keys=True))
                f.close()
        self.conn.close()

        tab_file = open(
            os.path.join(projpath, "tables.csv"), "w", encoding="utf8", newline=""
        )
        wr = csv.DictWriter(
            tab_file, delimiter=";", fieldnames=["name", "displayName", "description"]
        )
        wr.writeheader()
        wr.writerows(tables)
        tab_file.close()

    def generate_documents(self, projpath, buildsingle=True):
        mdpath = os.path.join(projpath, "markdown")
        if not os.path.exists(mdpath):
            os.mkdir(mdpath)
        tab_file = open(os.path.join(projpath, "tables.csv"), "r", encoding="utf8")
        reader = csv.DictReader(tab_file, delimiter=";")
        tables = []
        for table in reader:
            tables.append(table)
        tab_file.close()

        if buildsingle:
            md = "# Data stuctures\n"
        for table in tables:
            f = open(
                os.path.join(projpath, "%s_schema.json" % table["name"]),
                "r",
                encoding="utf8",
            )
            schema = json.load(f)
            f.close()
            example_file = os.path.join(projpath, "%s_example.json") % table["name"]
            if os.path.exists(example_file):
                f = open(example_file, "r", encoding="utf8")
                example = loads(f.read())
                f.close()
            else:
                example = None

            fields = {}
            f = open(
                os.path.join(projpath, "%s_fields.csv" % table["name"]),
                "r",
                encoding="utf8",
            )
            reader = csv.DictReader(f, delimiter=";")
            for r in reader:
                fields[r["name"]] = r
            f.close()
            if buildsingle:
                md += coll2md(table, schema, fields, example) + "\n\n"
            else:
                f = open(
                    os.path.join(mdpath, "%s.md" % (table["name"])),
                    "w",
                    encoding="utf8",
                )
                f.write(coll2md(table, schema, fields, example))
                f.close()
                print("Wrote %s.md" % (table["name"]))

        if buildsingle:
            f = open(os.path.join(mdpath, "tables.md"), "w", encoding="utf8")
            f.write(md)
            f.close()
            print(
                "Wrote %s to tables.md" % ",".join([table["name"] for table in tables])
            )
