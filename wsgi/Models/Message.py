from mongoengine import *
from flask_mail import Mail as FlaskMail
from flask_mail import Message as FlaskMessage
from flask import current_app as app


class Template(DynamicDocument):
    template_id = StringField(required=True)
    language = StringField(required=True,choices=('EN','GR'))
    meta = {'allow_inheritance': True}


class MailTemplate(Template):
    title = StringField(required=True)
    body = StringField(required=True)


class Notification(DynamicDocument):
    meta = {'allow_inheritance': True}
    pass


class Mail(Notification):
    send_from = EmailField(required=True)
    send_to = EmailField(required=True)
    compiled_title = StringField(required=True)
    compiled_body = StringField(required=True)
    from_template = ReferenceField(MailTemplate)

    def prepare(self, template_id, send_to, send_from='', language = 'EN', vars = {}):

        mail_template = MailTemplate.objects.get(template_id=template_id,language=language)

        self.from_template = mail_template
        self.compiled_body = self.from_template.title.format(**vars)
        self.compiled_title = self.from_template.body.format(**vars)
        self.send_to = send_to
        self.send_from = send_from

    def send(self):
        msg = FlaskMessage(
            subject=self.compiled_title,
            body=self.compiled_body,
            sender=self.send_from,
            recipients=[self.send_to])
        FlaskMail(app).send(message=msg)
        self.save()



