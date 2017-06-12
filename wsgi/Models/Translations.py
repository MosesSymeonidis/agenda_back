from mongoengine import *
EN_us = 'EN_us'
GR_el = 'GR_el'


class Translation(DynamicDocument):

    _id = StringField(unique=True,primary_key=True)

    @staticmethod
    def downloadCSV(csv_url = """https://docs.google.com/spreadsheets/d/1bINGrQDuslpBLjmssYDy1JGDb7A8Wu1_2MX9_RllWLU/export?format=csv&id=1bINGrQDuslpBLjmssYDy1JGDb7A8Wu1_2MX9_RllWLU&gid=0"""):
        import requests
        from io import StringIO
        csv = requests.get(csv_url)
        csv.encoding = 'utf-8'
        return StringIO(csv.text)

    @staticmethod
    def importFromCSVFile(csvfile):
        import csv
        reader_list = csv.DictReader(csvfile)
        i = 1
        for row in reader_list:

            try:
                entity = Translation()
                for field in row:
                    entity.__setattr__(field,row[field])
                entity.save()
                print('The '+str(i)+' translation inserted')
                i += 1
            except ValidationError:
                print(ValidationError)
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
