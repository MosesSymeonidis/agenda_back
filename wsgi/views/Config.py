from views import BaseView



class Config(BaseView):
    def get(self):
        from Models.Config import Config
        schema = Config.objects.exclude('id').get(config_id='schema')
        return schema
