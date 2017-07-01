from views import BaseView
from Models.User import User
from Models.Business import Business as Business_model
from Models.GeneralEmbeddedDocuments import Address
from flask import g as global_storage
from Utils.Validation import RequestValidation
from bson import ObjectId

auth = User.auth

class Business(BaseView):

    @RequestValidation.parameters_assertion(parameters=['data'],args_or_form='json')
    @auth.login_required
    def post(self):
        user = global_storage.user

        user.assertion_role(User.OWNER_ROLE)

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
            name=data['name'],
            settings=data['settings'],
            address=address_object
        )

        business.save()
        user.set_owned_business(business)
        user.save()
        return business.to_mongo(fields=['_id'])

    @RequestValidation.parameters_assertion(parameters=['sort_by', 'facets'])
    def get(self):
        all_business = []
        for business in Business_model.objects:
            all_business.append(business.to_mongo())
        return all_business



class BusinessPeaple(BaseView):

    def post(self, business_id, type, user_id=None,**kwargs):

        business = Business_model.objects.get(id=ObjectId(business_id))
        user = User.objects.get(id=ObjectId(user_id))

        data = self.request.get_json()
        #TODO if data for any keyword is empty we should check if user has register and find info from user
        info = {'business': business}
        for key in ['alias', 'email', 'phone', 'description']:
            if key in data:
                info[key] = data[key]

        if type == User.TYPE_ADMIN:
            user.set_admin_business(business)
        elif type == User.TYPE_CLIENT:
            client = User.Client(**info)
            user.set_client_business(client)
        elif type == User.TYPE_EMPLOYEE:
            if 'description' in info:
                del info['description']
            employee = User.Employee(**info)
            user.set_employee_business(employee)
        elif user_id is None:
            return {'success': False}
        else:
            return {'success': False}

        user.save()

        return {'success': True}

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
