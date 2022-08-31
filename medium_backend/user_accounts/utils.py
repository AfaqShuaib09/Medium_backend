import re

from user_accounts.constant import CNIC_REGEX, CONTACT_NO_REGEX, GENDER_CHOICES


def validate_cnic(cnic):
    """ Checks the format of cnic """
    return False if not re.match(CNIC_REGEX, cnic) and not cnic == '' else True

def validate_contact_number(contact_num):
    """ Checks the format of phone """
    return False if not re.match(CONTACT_NO_REGEX, contact_num) and not contact_num == '' else True

def validate_gender(gender):
    """ Validate gender is in gender choices """
    genders = [gender_choice[0] for gender_choice in GENDER_CHOICES]
    return True if gender in genders else False

def validate_email(email):
    """ Validate email """
    return False if not re.match(r'[^@]+@[^@]+\.[^@]+', email) and not email == '' else True

def validate_password(password):
    """ check password length """
    return False if len(password) < 8 else True

def validate_username(username):
    """ check django username validation """
    return False if not re.match(r'^[\w.@+-]+$', username) else True
