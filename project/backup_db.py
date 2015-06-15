#!/usr/bin/env python
from os.path import join
from pymongo import MongoClient
import csv

def backup_steppodium_db():

client = MongoClient()
db = client.steppodium
collection = db.users


with open(filepath) as f:
records = csv.DictReader(f)
collection.insert(records)

if collection.count() > 0:
print "you have imported" + filepath + " in the MongoDatabase!"
print collection.count()
print collection.find_one()
print importCSV.__name__
print importCSV.__doc__
else:
print "Error: failed to import"

importCSV("readingplan", "chapters", "/home/josh/bible/biblereadingplan2.csv")
