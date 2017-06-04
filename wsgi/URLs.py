main_urls = {
    "/user": 'views.Users.User',
    "/login": "views.Users.Login",
    "/activation/<string:user_id>":"views.Users.Activation",
    "/user/<string:role>":"views.Users.Role"
}

debug_urls = {'/debug':'views.test.test'}

def get_urls(debug=False):
    if debug:
        main_urls.update(debug_urls)
        return main_urls
    return main_urls
