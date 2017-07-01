main_urls = {
    '/auth':{
        'class':'views.Users.token',
        'endpoint':'auth'},
    '/user/<string:role>':{
        'class':'views.Users.UserView',
        'endpoint':'user_role'},
    '/user':{
        'class':'views.Users.UserView',
        'endpoint':'user_guest'},
    '/activation/<string:user_id>':{
        'class':'views.Users.Activation',
        'endpoint':'activation'},
    '/business':{
        'class':'views.Business.Business',
        'endpoint':'business'},
#    '/service/<string:type':'',
    '/service':{
        'class':'views.Business.Service',
        'endpoint':'service'},
    '/business/<string:business_id>/<string:type>/<string:user_id>':{
        'class':'views.Business.BusinessPeaple',
        'endpoint':'business_peaple'},
    '/business/<string:business_id>/settings':{
        'class':'views.Business.Settings',
        'endpoint':'business_settings'},
    '/appointment':{
        'class':'views.Appointment.Appointment',
        'endpoint':'new_appointment'},
    '/appointment/<string:id>':{
        'class':'views.Appointment.Appointment',
        'endpoint':'created_appointment'},
    '/schema':{
        'class':'views.Config.Config',
        'endpoint':'configs'},
    '/translations/<string:lang>/':{
        'class':'views.Translations.Translations',
        'endpoint':'translations'},
    '/<string:business_id>/<string:type>/CSV':{
        'class':'views.ExportImport.CSV',
        'endpoint':'export_import_csv'},

}

debug_urls = {
    '/test':{
        'class':'views.test.test',
        'endpoint':'test'} }

def get_urls():
    main_urls.update(debug_urls)
    return main_urls
