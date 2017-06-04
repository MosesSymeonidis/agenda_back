main_urls = {
    '/auth/':'views.Users.token',#this returns user's token
    '/user/<string:role>':'views.Users.User',#create/update/delete a user
    '/user':'views.Users.User',#get user and same as the above for the guests
     '/activation/<string:user_id>':'views.Users.Activation',
    '/bussiness':'views.Bussiness.Bussiness',
#    '/service/<string:type':'',
    '/service':'views.Bussiness.Service',
    '/bussiness/<string:bussiness_id>/<string:role>/<string:user_id>':'views.Bussiness.BussinessPeaple',
    '/bussiness/<string:bussiness_id>/settings':'views.Bussiness.Settings',
    '/appointment':'views.Appointment.Appointment',
    '/appointment/<string:id>':'views.Appointment.Appointment'

}

debug_urls = {'/debug':'views.test.test'}

def get_urls(debug=False):
    if debug:
        main_urls.update(debug_urls)
        return main_urls
    return main_urls
