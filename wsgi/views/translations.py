from views import BaseView
import models
from utils.admin_management import admin_authorization

class Translations(BaseView):


    def get(self, lang=models.Translation.get_default_lang()):

        lang = lang.lower()
        is_ok = False
        for opt in models.Translation.get_possible_langs():
            if lang == opt.lower():
                lang = opt
                is_ok = True
                break
        if not is_ok:
            lang = models.Translation.get_default_lang()

        return models.Translation.get_translations(lang)

    @admin_authorization
    def post(self, lang, **kwargs):

        saved_lang = models.Config.objects.get(config_id='general')['admin']['translation_update_lang_parameter']

        if lang != saved_lang:
            raise Exception
        from flask import current_app as app
        with app.app_context():
            csv = models.Translation.downloadCSV()
            models.Translation.importFromCSVFile(csv)

        return {'success':True}
