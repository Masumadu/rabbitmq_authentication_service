# from celery import shared_task
# from sendgrid import sendgrid, Mail
# from app.core.exceptions import AppException
# from flask_mail import Message
from app.extensions import celery

# from app import mail # causing circular imports


@celery.task
def sum(x, y):
    return x + y


# @shared_task
# def send_email():
#     msg = Message(
#         subject='Testing Emali Configuration',
#         sender='flask_app@test.com',
#         recipients=['paul@mailtrap.io'],
#         body="This is the body of the email"
#     )
#     mail.send(msg)







# EMAIL_PROVIDER_API = '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'
#
#
# @shared_task
# def send_email(email_parameters):
#     try:
#         sg = sendgrid.SendGridAPIClient(
#             api_key=EMAIL_PROVIDER_API)
#         msg = Mail(**email_parameters)
#         sg.send(msg)
#     except Exception as e:
#         raise AppException.OperationError(context=e.args[0])
