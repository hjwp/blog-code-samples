from django.db import models
from django.urls import reverse

class IssueReporter(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()



class Issue(models.Model):
    description = models.TextField()
    reporter = models.ForeignKey(IssueReporter, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'issue_id': self.id,
            'description': self.description,
            'reporter_name': self.reporter.name,
            'reporter_email': self.reporter.email,
        }

    def get_absolute_url(self):
        return reverse('issues_view', args=[self.id])

