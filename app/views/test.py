from views.base import BaseView
import models
import random


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

        # for i in range(0,10):
        #     models.Cache.set(str(random.randint(0, 100000000)), 'test')
        # b = models.Business.objects.get(id='5946509744a72127222ac7c1')
        # b.test()
        # models.Cache.set('test', b,type='pickle')
        # models.Cache.get('test')

        # # print(models.Business.objects)
        # print(models.Business.objects.filter(name='asfdfasdfa').aggregation_builder.execute())
        # business.objects.aggregation_builder.limit(1).execute()
        # print(business)
        return 'jhjhgjhgjhg'
