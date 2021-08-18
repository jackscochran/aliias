from ..data import emails


def add_email(email):

    if emails.Email.objects(email_string=email).first() is not None:
        return False# if email exists

    email_object = emails.Email()
    email_object.email_string = email
    email_object.save()

    return True

