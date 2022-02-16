# import email
from django.core.mail import EmailMessage
import threading 

#lets put sending an email on a different thread.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email=email
        threading.Thread.__init__(self)#super class due to inheritance
    
    def run(self):
        self.email.send()

class Util:
    #we can aswell use the cls attribute to indicate that it is astatic mthd
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['email_subject'],body=data['email_body'],to=[data['to_email']]
        )
        #now leveraging our thread to send the email
        EmailThread(email).start()



