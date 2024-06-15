from django.shortcuts import render,redirect,HttpResponse
from .models import MailList,Contact,ShortEstimate,LongEstimate,Question
import smtplib
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'service.html')

def contact(request):
    user_messages = False
    errors = []
    success = []
    name = ''
    email = ''
    message = ''
    subject = ''
    try:
        if request.method == 'POST':
            name = request.POST['name'].title().strip()
            email = request.POST['email'].lower().strip()
            subject_main = request.POST['subject'].strip()
            message = request.POST['message'].strip()

            subject = "We recieved your enquiry!"
            from_email = "Admin | LitDeal Global <noreply@litdealglobal.co.uk>"
            recipient_list = [email]

            # Render the HTML template for the email content
            html_content = render_to_string('user-mail.html', {
                'user_name': f'{name}',
                'headline':'Thank you for contacting LitDeal Global',
                'message':['Thank you for reaching out to us! We have received your message and appreciate the time you took to contact LitDeal Global. Our team will review your inquiry and get back to you as soon as possible.','Please be assured that your inquiry is important to us. We strive to respond to all messages within 12-48 hours. In the meantime, if your matter is urgent, please do not hesitate to contact us directly at +44 during our business hours.'],
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            # Create a plain text version of the email
            text_content = strip_tags(html_content)

            # Create the EmailMultiAlternatives object and attach both text and HTML versions
            processed_email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            processed_email.attach_alternative(html_content, "text/html")

            user_contact = Contact(
                name=name,
                email=email,
                subject=subject_main,
                message=message
            )
            # Send the email
            processed_email.send()
            user_contact.save()
            # Send an email to administrators
            subject_admin = "New Enquiry from a User"
            from_email_admin = f"User Enquiries <noreply@litdealglobal.co.uk>"
            recipient_list_admin = ["admin@litdealglobal.co.uk"] 

            html_content_admin = render_to_string('admin-contact-mail.html', {
                'user_name': f'{name}',
                'user_email': email,
                'user_subject': subject_main,
                'user_message': message,
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            text_content_admin = strip_tags(html_content_admin)
            processed_email_admin = EmailMultiAlternatives(subject_admin, text_content_admin, from_email_admin, recipient_list_admin)
            processed_email_admin.attach_alternative(html_content_admin, "text/html")
            processed_email_admin.send()
            if MailList.objects.filter(email=email).exists():
                # If email exists, update the name
                mail_list = MailList.objects.get(email=email)
                mail_list.name = name  # Update the name with the provided name
                mail_list.save()
            else:
                # If email does not exist, create a new record
                mail_list = MailList(name=name, email=email)
                mail_list.save()
            success.append('Your enquiry has been submitted.')
            user_messages = True
            context = {
                "user_messages": user_messages,
                "success": success,
            }

            return render(request, 'contact.html',context)
    except smtplib.SMTPRecipientsRefused:
        errors.append("Please enter a valid email.")
        user_messages = True
        context = {
            "errors": errors,
            "user_messages": user_messages,
            "name":name,
            "email":email,
            "subject":subject_main,
            "message":message,
            }
        return render(request, 'contact.html',context)
    
    return render(request, 'contact.html')

def request_estimate(request):
    try:
        if request.method == 'POST':
            # Get the form data from the POST request
            name = request.POST.get('name').title().strip()
            phone = request.POST.get('phone').strip()
            email = request.POST.get('email').lower().strip()
            service = request.POST.get('consultation')
            frequency = request.POST.get('frequency')
            pub = request.POST.get('pub')
            comments = request.POST.get('comments','N/A')

            subject = "We recieved your request!"
            from_email = "Admin | LitDeal Global <noreply@litdealglobal.co.uk>"
            recipient_list = [email]

            # Render the HTML template for the email content
            html_content = render_to_string('user-mail.html', {
                'user_name': f'{name}',
                'headline':f'Our Team received your request for {service}',
                'message':[f'Thank you for reaching out to us! We have received your request for an estimate for {service}. Our team will get back to you shortly'],
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            # Create a plain text version of the email
            text_content = strip_tags(html_content)

            # Create the EmailMultiAlternatives object and attach both text and HTML versions
            processed_email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            processed_email.attach_alternative(html_content, "text/html")

            # Create a new EstimateRequest instance and save it to the database
            new_request = LongEstimate(
                name=name,
                phone_number=phone,
                email=email,
                service=service,
                service_frequency=frequency,
                publicity=pub,
                comments=comments if comments else 'N/A'  # Set comments to None if it's empty
            )
            processed_email.send()
            new_request.save()
            # Send an email to administrators
            subject_admin = "New Enquiry from a User"
            from_email_admin = f"Estimate Requests <info@litdealglobal.co.uk>"
            recipient_list_admin = ["admin@litdealglobal.co.uk"] 

            html_content_admin = render_to_string('admin-mail.html', {
                'user_name': f'{name}',
                'headline':f'New request for {service}',
                'message':[f'Client Name: {name}.',f'Client Email: {email}.',f'Client Phone Number: {phone}.',f'Service Requested: {service}.',f'Service Frequency: {frequency}.',f'How did {name} hear about us: {pub}.',f'Additional Comments: {comments}.','',f'Date Requested: {datetime.now().strftime("%a %d %b %Y %I:%M%p")}'],
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            text_content_admin = strip_tags(html_content_admin)
            processed_email_admin = EmailMultiAlternatives(subject_admin, text_content_admin, from_email_admin, recipient_list_admin)
            processed_email_admin.attach_alternative(html_content_admin, "text/html")
            processed_email_admin.send()
            if MailList.objects.filter(email=email).exists():
                # If email exists, update the name
                mail_list = MailList.objects.get(email=email)
                mail_list.name = name  # Update the name with the provided name
                mail_list.save()
            else:
                # If email does not exist, create a new record
                mail_list = MailList(name=name, email=email)
                mail_list.save()
            
            # Redirect to a success page or return a success message
            return HttpResponse('Your estimate request has been submitted successfully!')
        return render(request, 'request-estimate.html')
    except smtplib.SMTPRecipientsRefused:
        return HttpResponse('Enter a valid email!')
    
    except Exception:
        return render(request, 'request-estimate.html')


def request_short_estimate(request):
    try:
        if  request.method == 'POST':
            name = request.POST['client-name'].title().strip()
            email = request.POST['client-email'].lower().strip()
            service = request.POST['consultation'].strip()

            subject = "We recieved your request!"
            from_email = "Admin | LitDeal Global <info@litdealglobal.co.uk>"
            recipient_list = [email]

            # Render the HTML template for the email content
            html_content = render_to_string('user-mail.html', {
                'user_name': f'{name}',
                'headline':f'Our Team received your request for {service}',
                'message':[f'Thank you for reaching out to us! We have received your request for an estimate for {service}. Our team will get back to you shortly'],
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            # Create a plain text version of the email
            text_content = strip_tags(html_content)

            # Create the EmailMultiAlternatives object and attach both text and HTML versions
            processed_email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            processed_email.attach_alternative(html_content, "text/html")

            user_contact = ShortEstimate(
                name=name,
                email=email,
                service=service,
            )
            # Send the email
            processed_email.send()
            user_contact.save()
            # Send an email to administrators
            subject_admin = "New Enquiry from a User"
            from_email_admin = f"User Enquiries <info@litdealglobal.co.uk>"
            recipient_list_admin = ["admin@litdealglobal.co.uk"] 

            html_content_admin = render_to_string('admin-mail.html', {
                'user_name': f'{name}',
                'headline':f'New request for {service}',
                'message':[f'User {name} has requested for an estimate for {service}.',f'Contact {name} on {email}.','',f'Date Requested: {datetime.now().strftime("%a %d %b %Y %I:%M%p")}'],
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            text_content_admin = strip_tags(html_content_admin)
            processed_email_admin = EmailMultiAlternatives(subject_admin, text_content_admin, from_email_admin, recipient_list_admin)
            processed_email_admin.attach_alternative(html_content_admin, "text/html")
            processed_email_admin.send()
            if MailList.objects.filter(email=email).exists():
                # If email exists, update the name
                mail_list = MailList.objects.get(email=email)
                mail_list.name = name  # Update the name with the provided name
                mail_list.save()
            else:
                # If email does not exist, create a new record
                mail_list = MailList(name=name, email=email)
                mail_list.save()
            return HttpResponse('Request submitted successfully!')

        return redirect('index')
    except smtplib.SMTPRecipientsRefused:
        return HttpResponse('Enter a valid email!')
    
    except Exception as e:
        return HttpResponse(f'Error processing your request. Try again later! {e}')

def faqs(request):
    try:
        if request.method == 'POST':
            # Get the form data from the POST request
            name = request.POST.get('name').title().strip()
            email = request.POST.get('email').strip().lower()
            question = request.POST.get('message').strip()

            subject = "We recieved your question!"
            from_email = "Admin | LitDeal Global <info@litdealglobal.co.uk>"
            recipient_list = [email]

            # Render the HTML template for the email content
            html_content = render_to_string('user-mail.html', {
                'user_name': f'{name}',
                'headline':f'Our Team received your question for',
                'message':[f'Thank you for reaching out to us! We have received your question:', f'{question}','','Our team will get back to you shortly'],
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            # Create a plain text version of the email
            text_content = strip_tags(html_content)

            # Create the EmailMultiAlternatives object and attach both text and HTML versions
            processed_email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            processed_email.attach_alternative(html_content, "text/html")

            new_request = Question(
                name=name,
                email=email,
                question = question
            )
            processed_email.send()
            new_request.save()
            # Send an email to administrators
            subject_admin = "New Enquiry from a User"
            from_email_admin = f"User Enquiries <noreply@litdealglobal.co.uk>"
            recipient_list_admin = ["admin@litdealglobal.co.uk"] 

            html_content_admin = render_to_string('admin-mail.html', {
                'user_name': f'{name}',
                'headline':f'New question from {name}',
                'message':[f'Client Name: {name}.',f'Client Email: {email}.',f'Question: {question}.','',f'Date Submitted: {datetime.now().strftime("%a %d %b %Y %I:%M%p")}'],
                'host':ensure_https(request.get_host()),
                'year':str(datetime.now().year)
            })

            text_content_admin = strip_tags(html_content_admin)
            processed_email_admin = EmailMultiAlternatives(subject_admin, text_content_admin, from_email_admin, recipient_list_admin)
            processed_email_admin.attach_alternative(html_content_admin, "text/html")
            processed_email_admin.send()
            if MailList.objects.filter(email=email).exists():
                # If email exists, update the name
                mail_list = MailList.objects.get(email=email)
                mail_list.name = name  # Update the name with the provided name
                mail_list.save()
            else:
                # If email does not exist, create a new record
                mail_list = MailList(name=name, email=email)
                mail_list.save()
            
            # Redirect to a success page or return a success message
            return HttpResponse('Your question has been submitted successfully!')
        return render(request, 'faqs.html')
    except smtplib.SMTPRecipientsRefused:
        return HttpResponse('Enter a valid email!')
    
    except Exception as e:
        return HttpResponse(f'Error processing your request! {e}')

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
@csrf_exempt
def subscribe_newsletter(request):    
    try:
        if request.method == 'POST':
            email = request.POST.get('email').lower().strip()
            if "@" not in email:
                print("here")
                return HttpResponse("Invalid email address")
                
            print("email", email)
            if not MailList.objects.filter(email = email).exists():

                # Sending welcome email
                subject = "Welcome to Our Newsletter!"
                from_email = settings.DEFAULT_FROM_EMAIL  #"Newsletter | LitDeal Global <newsletter@nmefranltd.co.uk>"
                print("from_email", from_email)
                recipient_list = [email]

                # Render the HTML template for the email content
                html_content = render_to_string('subscribe-mail.html', {
                    'email': email,
                    'host':ensure_https(request.get_host()),
                    'year':str(datetime.now().year)
                })

                # Create a plain text version of the email
                text_content = strip_tags(html_content)

                # Send the email
                processed_email = send_mail(subject, 
                                            # text_content, 
                                            from_email, 
                                            recipient_list, 
                                            html_message=html_content)
                
                # Create the EmailMultiAlternatives object and attach both text and HTML versions
                # processed_email = EmailMultiAlternatives(subject, text_content, recipient_list)
                # processed_email.attach_alternative(html_content, "text/html")

                # # Send the email
                # processed_email.send()
                
                if processed_email:
                    print("Email sent")
                    print(processed_email)
                    mail_list = MailList(email=email)
                    mail_list.save()
                    
                else:
                    print("Email not sent")
                
            # if 
        
            # Check if there's a 'next' parameter in the query string (referring page)
        #     if 'next' in request.GET:
        #         redirect_url = request.GET['next']
        #         return redirect(redirect_url)

        #     # If 'next' is not present in the query parameters, redirect to a default page
        #     return redirect('index')
        # return redirect('index')  # Change 'home' to the appropriate URL name for your default page

    except Exception as e:
        print("yes")
        print(e)
        # Check if there's a 'next' parameter in the query string (referring page)
        if 'next' in request.GET:
            redirect_url = request.GET['next']
            return redirect(redirect_url)
        # If 'next' is not present in the query parameters, redirect to a default page
        return redirect('index')  # Change 'home' to the appropriate URL name for your default page



def unsubscribe_newsletter(request):
    if 'mail' in request.GET:
        email = request.GET['mail'].lower()
        try:
            # Check if the email exists in the SubscribedEmail model
            subscriber = MailList.objects.get(email=email)
            # Unsubscribe the user
            subscriber.delete()
            # Render a template confirming successful unsubscribe
            return render(request, 'unsubscribe-success.html')
        except MailList.DoesNotExist:
            # Email not found, render a template with an error message
            return redirect('index')
    else:
        # If 'mail' parameter is missing, redirect to a generic error page
        return redirect('index')
    
def page_not_found(request, exception):
    return render(request, '404.html')

def ensure_https(host):
    # Ensure the URL always has the "https://" scheme
    return 'https://' + host.lstrip('https://').lstrip('http://')

# views.py

from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)
@csrf_exempt  # Temporarily disable CSRF protection for testing
def send_bulk_email(request):
    if request.method == 'POST':
        emails = MailList.objects.values_list('email', flat=True)
        email_list = list(emails)
        
        try:
            send_mail(
                subject = 'Subject here',
                message = 'Here is the message.',
                from_email= 'info@litdealglobal.co.uk',  # From email
                recipient_list= email_list ,  # To email
                fail_silently=False,
            )
            return HttpResponse("Email sent")
        except Exception as e:
            logger.error("Error sending email: %s", e)
            return HttpResponse("Error sending email", status=500)
    return HttpResponse("Send a POST request to send the email")