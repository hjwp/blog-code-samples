def _to_dict(issue):
    return dict(
        issue_id=str(issue.id),
        reporter_name=issue.reporter.name,
        reporter_email=issue.reporter.email,
        description=issue.description,
    )


def view_issue(start_uow, issue_id):
    with start_uow() as uow:
        return _to_dict(uow.issues.get(issue_id))

def list_issues(start_uow):
    with start_uow() as uow:
        return [_to_dict(i) for i in uow.issues.list()]
