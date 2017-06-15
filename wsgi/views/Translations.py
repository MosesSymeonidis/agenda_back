from views import BaseView
from Models.Utils import Translation

class Translations(BaseView):


    def get(self,lang):
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
