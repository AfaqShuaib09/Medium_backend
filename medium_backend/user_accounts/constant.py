''' Constants declared to be used in user app '''
import re

from django.core.validators import RegexValidator

CNIC_VALIDATOR = RegexValidator("\d{5}\-\d{7}\-\d{1}", "CNIC format needs to be - XXXXX-XXXXXXX-X")
CONTACT_NO_VALIDATOR = RegexValidator("^\+\d{12}$", "Phone number format needs to be +XXXXXXXXXXXX")

GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('N/A', 'Do not specify')
)
CNIC_REGEX = re.compile("\d{5}\-\d{7}\-\d{1}")
CONTACT_NO_REGEX = re.compile("\+\d{12}$")
