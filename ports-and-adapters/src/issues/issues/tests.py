from django.test import TestCase
from issues.models import Issue, IssueReporter

# Create your tests here.

class IssueViewsTests(TestCase):

    def test_view_issue(self):
        reporter = IssueReporter.objects.create(name='jane', email='jane@example.com')
        issue = Issue.objects.create(reporter=reporter, description='nothing works')
        r = self.client.get(f'/issues/{issue.id}')
        self.assertEqual(r.json(), issue.to_dict())

    def test_list_issues(self):
        reporter = IssueReporter.objects.create(name='jane', email='jane@example.com')
        i1 = Issue.objects.create(reporter=reporter, description='nothing works')
        i2 = Issue.objects.create(reporter=reporter, description='no blue top milk in fridge')
        r = self.client.get('/issues/')
        self.assertEqual(r.json(), [i1.to_dict(), i2.to_dict()])
