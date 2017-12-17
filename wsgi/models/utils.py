from mongoengine import *
import datetime
from aggregation_builder import AggregateQuerySet

class Config(DynamicDocument):
    pass

class Traffic(DynamicDocument):
    meta = {'queryset_class': AggregateQuerySet}
    created_at = DateTimeField(default=datetime.datetime.now)

class Translation(DynamicDocument):

    _id = StringField(unique=True,primary_key=True)

    @staticmethod
    def get_default_lang():
        return Config.objects.get(config_id='general')['translations']['default_lang']

    @staticmethod
    def get_possible_langs():
        return Config.objects.get(config_id='general')['translations']['languages']


    @staticmethod
    def downloadCSV(csv_url = """https://docs.google.com/spreadsheets/d/1bINGrQDuslpBLjmssYDy1JGDb7A8Wu1_2MX9_RllWLU/export?format=csv&id=1bINGrQDuslpBLjmssYDy1JGDb7A8Wu1_2MX9_RllWLU&gid=0"""):
        import requests
        from io import StringIO
        csv = requests.get(url=csv_url,verify=False)
        csv.encoding = 'utf-8'
        return StringIO(csv.text)

    @staticmethod
    def importFromCSVFile(csvfile):
        import csv
        from utils.base import get_database
        reader_list = csv.DictReader(csvfile)
        i = 1
        db = get_database()
        translations = db.translation.initialize_unordered_bulk_op()
        for row in reader_list:

            try:
                entity = Translation()
                for field in row:
                    entity.__setattr__(field,row[field])

                    translations.find({'_id':entity.id}).upsert().update({'$set':entity.to_mongo()})
                print('The '+str(i)+' translation inserted')
                i += 1
            except ValidationError:
                pass

        print(translations)
        translations.execute()


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
