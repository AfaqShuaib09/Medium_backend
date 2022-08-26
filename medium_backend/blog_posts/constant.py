''' Constants declaration for the blog_posts app '''

POST_REQ_FIELDS = ['title', 'content']
REPORT_CHOICES = [
    ('spam', 'It\'s spam'),
    ('hate-speech', 'Hate Speech and Symbol used'),
    ('false-information', 'False Information'),
    ('sensitive', 'Sensitive Content'),
    ('duplicate', 'Copyrited Content'),
]
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
DEFAULT_POST_SEAERCH_FIELDS = ['posted_by__username','title', 'content', 'assigned_tags__tag__name']
