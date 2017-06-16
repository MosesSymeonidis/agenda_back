from views import BaseView
from Models.Utils import Translation
from Utils.AdminManagement import admin_authorization

class Translations(BaseView):


    def get(self, lang=Translation.get_default_lang()):
        lang = lang.lower()
        is_ok = False
        for opt in Translation.get_possible_langs():
            if lang == opt.lower():
                lang = opt
                is_ok = True
                break
        if not is_ok:
            lang = Translation.get_default_lang()

        return Translation.get_translations(lang)

    @admin_authorization
    def post(self,**kwargs):

        from app import app
        from Models.Utils import Translation

        with app.app_context():
            csv = Translation.downloadCSV()
            Translation.importFromCSVFile(csv)

        return {'success':True}
