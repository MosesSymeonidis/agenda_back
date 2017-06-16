from views import BaseView
from Models.User import User
from Models.Business import Business as Business_model
from Models.GeneralEmbeddedDocuments import Address
from flask import g as global_storage
from Utils.Validation import RequestValidation

auth = User.auth

class Business(BaseView):

    @RequestValidation.parameters_assertion(parameters=['data'],args_or_form='json')
    @auth.login_required
    def post(self):
        user = global_storage.user

        user.assertion_role(User.SHOP_OWNER_ROLE)

        user.assertion_of_businesses_num()

        data = self.request.get_json()['data']
        RequestValidation.parameter_assertion(data,['name','settings','plan','address'])
        address = data['address']
        RequestValidation.parameter_assertion(address,['country','area','city','street','geolocation'])
        address_object = Address(
            country=address['country'],
            area=address['area'],
            city=address['city'],
            street=address['street'],
            number=int(address['number'])
            # geolocation=address['geolocation']
                          )
        print(address_object.to_json())
        business = Business_model(
            owner=user,
            name=data['name'],
            settings=data['settings'],
            plan=data['plan'],
            address=address_object
        )

        business.save()

        return user.to_mongo(fields=['_id'])

    @RequestValidation.parameters_assertion(parameters=['sort_by', 'facets'])
    def get(self):
        all_business = []
        for business in Business_model.objects:
            all_business.append(business.to_mongo())
        return all_business



class BusinessPeaple(BaseView):

    def post(self,**kwargs):
        return {}

    def get(self,**kwargs):
        return {}

    def put(self, **kwargs):
        return {}

    def delete(self,**kwargs):
        return {}


class Settings(BaseView):

    def post(self,**kwargs):
        return {}

    def get(self,**kwargs):
        return {}

    def put(self, **kwargs):
        return {}

    def delete(self,**kwargs):
        return {}


class Service(BaseView):

    def post(self,**kwargs):
        return {}

    def get(self,**kwargs):
        return {}

    def put(self, **kwargs):
        return {}

    def delete(self,**kwargs):
        return {}
