""" Functions to be used in the views """
from rest_framework import filters, request

from blog_posts.constant import DEFAULT_POST_SEAERCH_FIELDS, STATUS_CHOICES


def vaidate_report_status(report_status):
    """ Check the validity of report status """
    status = [status_choice[0] for status_choice in STATUS_CHOICES]
    return True if report_status in status else False


class DynamicSearchFilter(filters.SearchFilter):
    """ SearchFilter class to search for a specific field """
    def get_search_fields(self, view, request):
        """ Dynamically search fields based on parameter passed in request """
        return request.GET.getlist('search_fields', DEFAULT_POST_SEAERCH_FIELDS)
