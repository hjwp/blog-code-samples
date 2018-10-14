import json
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from issues.models import Issue, IssueReporter

@csrf_exempt
def list_issues(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reporter, _ = IssueReporter.objects.get_or_create(
            name=data['reporter_name'],
            email=data['reporter_email'],
        )
        issue = Issue.objects.create(
            description=data['problem_description'],
            reporter=reporter
        )
        return redirect(issue)

    return HttpResponse(json.dumps([
        issue.to_dict() for issue in Issue.objects.all()
    ]), content_type='application/json')

def view_issue(request, issue_id):
    return HttpResponse(json.dumps(
        Issue.objects.get(pk=issue_id).to_dict(),
    ), content_type='application/json')
