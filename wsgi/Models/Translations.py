from mongoengine import *
from pymongo import UpdateOne
import os
EN_us = 'EN_us'
GR_el = 'GR_el'

class Translation(DynamicDocument):
    _id = StringField(unique=True,primary_key=True)

    @staticmethod
    def importFromCSV(csv_path = os.getcwd()+'/translations.csv'):
        import csv
        with open(csv_path ) as csvfile:
             reader = csv.DictReader(csvfile)

             for row in reader:
                 try:
                     entity = Translation()
                     for field in row:
                         entity.__setattr__(field,row[field])

                     entity.save()
                 except ValidationError:
                     pass
    @staticmethod
    def get_translations(lang):
        translations = Translation.objects.fields(**{
            '_id':1,
            lang:1
        })
        res = {}
        for translation in translations:
            res.update({translation['_id']:translation[lang]})

        return res
