from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail


def contact(request):
    # get form values
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        advisor_email = request.POST['advisor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already made a request for this listing.')
                return redirect('/listings/' + listing_id)

        contact = Contact(
            listing=listing,
            listing_id=listing_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            user_id=user_id
        )

        contact.save()

        # Send email notification to user
        user_email_message = f'''Hi {name},

Thank you for your test drive request for {listing}!

We have received your request and a sales advisor will contact you shortly.

Your Request Details:
- Car: {listing}
- Name: {name}
- Email: {email}
- Phone: {phone}
- Message: {message}

Best regards,
Carss Auto Dealer Team
'''

        send_mail(
            'Your Carss Test Drive Request - Confirmation',
            user_email_message,
            'boy749377@gmail.com',
            [email],
            fail_silently=False
        )

        # Send email notification to admin
        admin_email_message = f'''NEW TEST DRIVE BOOKING!

A customer has requested a test drive:

Car Details:
- Car: {listing}
- Listing ID: {listing_id}

Customer Information:
- Name: {name}
- Email: {email}
- Phone: {phone}
- Message: {message}

Please contact the customer to schedule the test drive.

Time of Request: {contact.contact_date}
'''

        send_mail(
            f'New Test Drive Booking - {name} - {listing}',
            admin_email_message,
            'boy749377@gmail.com',
            ['boy749377@gmail.com'],
            fail_silently=False
        )

        messages.success(
            request, 'Your request has been submitted, a request confirmation is sent to your email. We will get back to you soon.')

        return redirect('/listings/' + listing_id)
