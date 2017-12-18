from views import BaseView
import models


class test(BaseView):
    def get(self, business=None):
        # from flask_mail import Message as FlaskMessage
        # from flask_mail import Mail
        #
        # msg = FlaskMessage(
        #     subject='bourda',
        #     body='yolo',
        #     sender='info@taxicab.me',
        #     recipients=['msymewnidhs2113@yahoo.gr'])
        # mail = Mail()
        # mail.send(message=msg)
        # from Models.Utils import Traffic
        #
        # print(Traffic.objects.aggregation_builder.group(id='response.data.0',first_obj=FIRST('$$ROOT')).skip(5).limit(7))
        #
        # return [d for d in Traffic.objects.aggregation_builder.group(id='response.data',first_obj=FIRST('$$ROOT')).skip(5).limit(7).execute()]
        #
        # from Models.Message import Mail, MailTemplate
        # # MailTemplate(template_id='test', language='EN',title='aaaaaaaaaaa', template_path='mails/activation_mail.html').save()
        # mail = Mail(language='EN',template_id='test',send_to='msymewnidhs2113@yahoo.gr', send_from='info@taxicab.me',vars={'yolo':'asdfasd'})
        # mail.send()
        # models.Business.objects.get(id='5916c4a6982bce88511cec8c')
        print(business)
        return {'yolo': True}
