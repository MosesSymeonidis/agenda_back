from views import GeneralView
from flask import Response
from Models.Bussiness import Bussiness
from bson import ObjectId

class CSV(GeneralView):

    def get(self, bussiness_id, type, **kwargs):
        if type.lower() == 'service':
            objects = Bussiness.objects(id = ObjectId(bussiness_id)).services
            print(objects)
        else:
            return super(CSV,self).get()
        csv = '1,2,3\n4,5,6\n'
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition":"attachment; filename=myplot.csv"})
