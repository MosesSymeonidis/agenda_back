from mongoengine import *
from flask_mail import Mail as FlaskMail
from flask_mail import Message as FlaskMessage
from flask import render_template


class Template(DynamicDocument):
    template_id = StringField(required=True)
    language = StringField(required=True,choices=('EN','GR'))
    meta = {'allow_inheritance': True}


class MailTemplate(Template):
    title = StringField(required=True)
    # body_params = ListField(DictField(), required=True)
    template_path = StringField(required=True)


class Notification(DynamicDocument):
    meta = {'allow_inheritance': True}
    pass


class Mail(Notification):
    send_from = EmailField(required=True)
    send_to = EmailField(required=True)
    compiled_title = StringField(required=True)
    compiled_body = StringField(required=True)
    from_template = ReferenceField(MailTemplate)
    body_params = DictField()

    def __init__(self, template_id, send_to, send_from='', language = 'EN', vars = {}):
        super(Mail, self).__init__()
        self.prepare(template_id, send_to, send_from, language , vars)

    def prepare(self, template_id, send_to, send_from='', language = 'EN', vars = {}):
        mail_template = MailTemplate.objects.get(template_id=template_id,language=language)
        print(mail_template.id)
        self.from_template = mail_template
        self.compiled_body = render_template(self.from_template.template_path, **vars)
        self.compiled_title = self.from_template.title.format(**vars)
        self.send_to = send_to
        self.send_from = send_from
        self.body_params = vars

    def send(self):
        from flask_mail import Message as FlaskMessage
        from flask_mail import Mail as FlaskMail

        msg = FlaskMessage(
            subject=self.compiled_title,
            html=self.compiled_body,
            sender=self.send_from,
            recipients=[self.send_to])
        mail = FlaskMail()
        mail.send(message=msg)

        self.save()



