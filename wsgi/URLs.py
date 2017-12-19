import views

__main_urls__ = [
    dict(route='/auth',
         cls=views.users.token,
         endpoint='auth'),
    dict(route='/user/<string:role>',
         cls=views.users.UserView,
         endpoint='user_role'),
    dict(route='/user',
         cls=views.users.UserView,
         endpoint='user_guest'),
    dict(route='/activation/<string:user_id>',
         cls=views.users.Activation,
         endpoint='activation'),
    dict(route='/business',
         cls=views.business.Business,
         endpoint='business'),
    dict(route='/service',
         cls=views.business.Service,
         endpoint='service'),
    dict(route='/business/<string:business_id>/<string:type>/<string:user_id>',
         cls=views.business.BusinessPeaple,
         endpoint='business_peaple'),
    dict(route='/business/<string:business_id>/settings',
         cls=views.business.Settings,
         endpoint='business_settings'),
    dict(route='/appointment',
         cls=views.appointment.Appointment,
         endpoint='new_appointment'),
    dict(route='/appointment/<string:id>',
         cls=views.appointment.Appointment,
         endpoint='created_appointment'),
    dict(route='/schema',
         cls=views.config.Config,
         endpoint='configs'),
    dict(route='/translations/<string:lang>/',
         cls=views.translations.Translations,
         endpoint='translations'),
    dict(route='/<string:business_id>/<string:type>/CSV',
         cls=views.exportImport.CSV,
         endpoint='export_import_csv')
]

__debug_urls__ = [
    dict(route='/test/<Business:business>',
         cls=views.test,
         endpoint='test234'),
    dict(route='/test/',
         cls=views.test,
         endpoint='test2')
]


def get_urls():
    main_urls = __main_urls__
    main_urls += __debug_urls__
    return main_urls
