from views import BaseView
from Models.Translations import Translation, EN_us, GR_el

class Translations(BaseView):


    def get(self,lang):
        lang = lang.lower()
        is_ok = False
        for opt in [EN_us, GR_el]:
            if lang == opt.lower():
                lang = opt
                is_ok = True
                break
        if not is_ok:
            lang = EN_us

        return Translation.get_translations(lang)
