from blog_posts.constant import STATUS_CHOICES

def vaidate_report_status(report_status):
    """ Check the validity of report status """
    status = [status_choice[0] for status_choice in STATUS_CHOICES]
    return True if report_status in status else False
