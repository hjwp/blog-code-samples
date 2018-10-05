import uuid
from pathlib import Path
import json

from issues.domain.model import Issue, IssueReporter
from issues.domain.ports import IssueLog, UnitOfWork

DB_PATH = Path('/tmp/abc123')
BUS = None

def set_bus(bus):
    global BUS
    BUS = bus


def _to_dict(issue):
    return dict(
        issue_id=str(issue.id),
        reporter_name=issue.reporter.name,
        reporter_email=issue.reporter.email,
        description=issue.description,
    )

def _from_dict(d):
    return Issue(
        issue_id=uuid.UUID(d['issue_id']),
        description=d['description'],
        reporter=IssueReporter(
            name=d['reporter_name'],
            email=d['reporter_email'],
        )
    )



class IssueRepository(IssueLog):

    def __init__(self):
        DB_PATH.mkdir(exist_ok=True)
        self.issues = {}

    def add(self, issue: Issue) -> None:
        self.issues[issue.id] = issue

    def _path(self, issue_id):
        return DB_PATH / str(issue_id)

    def _get_from_storage(self, issue_id):
        return _from_dict(json.loads(self._path(issue_id).read_text()))

    def _get(self, issue_id) -> Issue:
        try:
            return self.issues[issue_id]
        except KeyError:
            i = self._get_from_storage(issue_id)
            self.issues[issue_id] = i
            return i

    def list(self):
        yield from self.issues.values()
        for issue_id in DB_PATH.iterdir():
            if issue_id not in self.issues:
                yield self._get_from_storage(issue_id)

    def flush(self):
        for issue in self.issues.values():
            self._path(issue.id).write_text(json.dumps(_to_dict(issue)))


class SlashtmpUnitofWork(UnitOfWork):

    def __init__(self, bus):
        self.bus = bus
        self.issues_repository = IssueRepository()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.publish_events()

    def commit(self):
        self.issues_repository.flush()

    def rollback(self):
        self.issues_repository.issues = {}

    def publish_events(self):
        for issue in self.issues_repository.issues.values():
            for event in issue.events:
                self.bus.handle(event)

    @property
    def issues(self):
        return self.issues_repository


def start_unit_of_work():
    return SlashtmpUnitofWork(BUS)
