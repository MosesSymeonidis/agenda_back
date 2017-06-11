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
    '/bussiness':{
        'class':'views.Bussiness.Bussiness',
        'endpoint':'bussiness'},
#    '/service/<string:type':'',
    '/service':{
        'class':'views.Bussiness.Service',
        'endpoint':'service'},
    '/bussiness/<string:bussiness_id>/<string:role>/<string:user_id>':{
        'class':'views.Bussiness.BussinessPeaple',
        'endpoint':'bussiness_peaple'},
    '/bussiness/<string:bussiness_id>/settings':{
        'class':'views.Bussiness.Settings',
        'endpoint':'bussiness_settings'},
    '/appointment':{
        'class':'views.Appointment.Appointment',
        'endpoint':'new_appointment'},
    '/appointment/<string:id>':{
        'class':'views.Appointment.Appointment',
        'endpoint':'created_appointment'},
    '/schema':{
        'class':'views.Config.Config',
        'endpoint':'configs'}

}

debug_urls = {
    '/test':{
        'class':'views.test.test',
        'endpoint':'test'} }

def get_urls():
    main_urls.update(debug_urls)
    return main_urls
