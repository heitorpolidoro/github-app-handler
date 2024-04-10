from typing import Optional

from github.CheckRun import CheckRun
from github.Repository import Repository


class EventCheckRun:
    def __init__(self, repository: Repository, name: str, sha: str):
        self.repository = repository
        self.name = name
        self.sha = sha
        self.check_run: Optional[CheckRun] = None

    def start(
        self,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        text: Optional[str] = None,
        status: str = "in_progress",
    ):
        """Start a check run"""
        output = {"title": title or self.name, "summary": summary or ""}
        if text:
            output["text"] = text

        self.check_run = self.repository.create_check_run(
            self.name,
            self.sha,
            status=status,
            output=output,
        )

    def update(self, status=None, conclusion=None, **output):
        """Updates the check run"""
        args = {}
        if status is not None:
            args["status"] = status

        if conclusion is not None:
            args["conclusion"] = conclusion
            args["status"] = "completed"

        if output:
            output["title"] = output.get("title", self.check_run.output.title)
            output["summary"] = output.get("summary", self.check_run.output.summary)
            args["output"] = output

        if args:
            self.check_run.edit(**args)
