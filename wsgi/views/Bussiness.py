from views import BaseView
from Models.User import User
from Models.Bussiness import Bussiness
from Models.GeneralEmbeddedDocuments import Address
from flask import g as global_storage
from Utils.Validation import RequestValidation

auth = User.auth

class Bussiness(BaseView):

    @RequestValidation.parameters_assertion(parameters=['data'])
    @auth.login_required
    def post(self):
        user = global_storage.user
        user.check_role(User.SHOP_OWNER_ROLE)
        data = self.request.args['data']
        RequestValidation.parameter_assertion(data,['name','settings','plan','address'])
        address = data['address']
        RequestValidation.parameter_assertion(address,['country','area','city','street','geolocation'])
        address = Address(
            country=address['country'],
            area=address['area'],
            city=address['city'],
            street=address['street'],
            geolocation=address['geolocation']
                          )
        bussiness = Bussiness(
            name=data['name'],
            settings=data['settings'],
            plan=data['plan'],
            address=address
        )

        bussiness.save()

        return user.to_mongo(fields=['_id'])

    @RequestValidation.parameters_assertion(parameters=['q'])
    def get(self):
        all_bussiness = []
        for bussiness in Bussiness.objects:
            all_bussiness.append(bussiness.to_mongo())
        return all_bussiness

