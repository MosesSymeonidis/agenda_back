

main_urls = {
    '/auth':{
        'class':'views.users.token',
        'endpoint':'auth'},
    '/user/<string:role>':{
        'class':'views.users.UserView',
        'endpoint':'user_role'},
    '/user':{
        'class':'views.users.UserView',
        'endpoint':'user_guest'},
    '/activation/<string:user_id>':{
        'class':'views.users.Activation',
        'endpoint':'activation'},
    '/business':{
        'class':'views.business.Business',
        'endpoint':'business'},
#    '/service/<string:type':'',
    '/service':{
        'class':'views.business.Service',
        'endpoint':'service'},
    '/business/<string:business_id>/<string:type>/<string:user_id>':{
        'class':'views.business.BusinessPeaple',
        'endpoint':'business_peaple'},
    '/business/<string:business_id>/settings':{
        'class':'views.business.Settings',
        'endpoint':'business_settings'},
    '/appointment':{
        'class':'views.appointment.Appointment',
        'endpoint':'new_appointment'},
    '/appointment/<string:id>':{
        'class':'views.appointment.Appointment',
        'endpoint':'created_appointment'},
    '/schema':{
        'class':'views.config.Config',
        'endpoint':'configs'},
    '/translations/<string:lang>/':{
        'class':'views.translations.Translations',
        'endpoint':'translations'},
    '/<string:business_id>/<string:type>/CSV':{
        'class':'views.exportImport.CSV',
        'endpoint':'export_import_csv'},

}

debug_urls = {
    '/test/<model(model="Business"):business>':{
        'class':'views.test.test',
        'endpoint':'test'},
    '/test/': {
        'class': 'views.test.test',
        'endpoint': 'test2'},
}

def get_urls():
    main_urls.update(debug_urls)
    return main_urls
