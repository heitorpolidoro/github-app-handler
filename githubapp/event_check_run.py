"""Class to represents an Event Check Run, a wrapper to Github CheckRun"""

from enum import Enum
from typing import Optional, Any

from github.CheckRun import CheckRun
from github.Repository import Repository

from githubapp import Config


class CheckRunStatus(Enum):
    """The CheckRun Status"""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    WAITING = "waiting"
    REQUESTED = "requested"
    PENDING = "pending"


class CheckRunConclusion(Enum):
    """The CheckRun Conclusion"""

    FAILURE = "failure"
    ACTION_REQUIRED = "action_required"
    CANCELLED = "cancelled"
    NEUTRAL = "neutral"
    STALE = "stale"
    TIMED_OUT = "timed_out"
    SUCCESS = "success"
    SKIPPED = "skipped"


ICONS_DEFAULT = {
    "circle": {
        CheckRunStatus.IN_PROGRESS: "orange_circle",
        CheckRunConclusion.SUCCESS: "green_circle",
        CheckRunConclusion.FAILURE: "red_circle",
        CheckRunConclusion.SKIPPED: "black_circle",
    },
}

ICONS = {}


def set_icons() -> None:
    global ICONS
    if icons_set := Config.SUB_RUNS_ICONS:
        if isinstance(icons_set, str):
            if ICONS := ICONS_DEFAULT.get(icons_set) is None:
                raise AttributeError(
                    f"There is no icon set '{icons_set} in default configuration. {ICONS_DEFAULT.keys()}"
                )


class EventCheckRun:
    """
    EventCheckRun

    This class represents a check run for a GitHub repository commit. It allows starting, updating
    and completing a check run.

    Attributes:
      - repository: The GitHub Repository object
      - name: The name of the check run
      - sha: The commit SHA being checked
      - check_run: The GitHub CheckRun object, populated after starting the run

    Methods:
      - start: Starts a new check run
      - update: Updates an in-progress check run
      - complete: Completes a check run with a conclusion
    """

    class SubRun:
        def __init__(
            self,
            parent_check_run: "EventCheckRun",
            name: str,
            status: CheckRunStatus = None,
            summary: str = None,
        ) -> None:
            self.parent_check_run = parent_check_run
            self.name = name
            self.status = status
            self.summary = summary
            self.conclusion = None
            self.title = ""

        def __repr__(self) -> str:
            _dict = self.__dict__.copy()
            _dict.pop("parent_check_run")
            return f"SubRun({_dict})"

        def update(
            self,
            title: str = None,
            status: CheckRunStatus = None,
            summary: str = None,
            conclusion: CheckRunConclusion = None,
            update_check_run: bool = True,
        ) -> None:
            self.title = title or self.title
            self.status = status or self.status
            self.conclusion = conclusion or self.conclusion
            if self.conclusion:
                self.status = CheckRunStatus.COMPLETED
            self.summary = summary or self.summary
            if update_check_run:
                self.parent_check_run.update_sub_runs(title=self.title)

    def __init__(self, repository: Repository, name: str, sha: str):
        self.repository = repository
        self.name = name
        self.sha = sha
        self._check_run: Optional[CheckRun] = None
        self.sub_runs = []

    def __repr__(self) -> str:
        _dict = self.__dict__.copy()
        _dict.pop("repository")
        _dict.pop("_check_run")
        _dict.pop("sub_runs")
        return f"EventCheckRun({_dict})"

    def __getattr__(self, attr: str) -> Optional[str]:
        if self._check_run:
            if hasattr(self._check_run, attr):
                result = getattr(self._check_run, attr)
            elif hasattr(self._check_run.output, attr):
                result = getattr(self._check_run.output, attr)
            else:
                raise AttributeError(f"'CheckRun' object has no attribute '{attr}'")
            if result:
                if attr == "status":
                    result = CheckRunStatus[result.upper()]
                elif attr == "conclusion":
                    result = CheckRunConclusion[result.upper()]
            return result
        return None

    def start(
        self,
        status: CheckRunStatus = CheckRunStatus.WAITING,
        summary: str = None,
        title: str = None,
        text: str = None,
    ):
        """Start a check run"""
        output = {"title": title or self.name, "summary": summary or ""}
        if text:
            output["text"] = text

        self._check_run = self.repository.create_check_run(
            self.name,
            self.sha,
            status=status.value,
            output=output,
        )

    def update_sub_runs(self, title: str = None) -> None:
        summary = self.build_summary(self.sub_runs)
        self.update(title=title, summary=summary)

    @staticmethod
    def build_summary(sub_runs):
        runs_summary = []
        for run in sub_runs:
            if run_status_icon := ICONS.get(run.conclusion or run.status, ""):
                run_status_icon = f":{run_status_icon}: "
            runs_summary.append(f"{run_status_icon}{run.name}: {run.title}")
            if run.summary:
                runs_summary.append(run.summary)
        summary = "\n".join(runs_summary)
        return summary

    def update(
        self,
        title: str = None,
        status: CheckRunStatus = None,
        summary: str = None,
        conclusion: CheckRunConclusion = None,
        text: str = None,
        **output,
    ) -> None:
        """Updates the check run"""

        def clean_dict(d: dict[str, Any]) -> dict[str, Any]:
            """Remove keys if no value"""
            return {k: v for k, v in d.items() if v is not None}

        if conclusion is not None:
            status = CheckRunStatus.COMPLETED
        output.update(
            {
                "title": title,
                "summary": summary,
                "text": text,
            }
        )

        output = clean_dict(output) or None
        args = {
            "status": status.value if isinstance(status, Enum) else status,
            "conclusion": conclusion.value if isinstance(conclusion, Enum) else conclusion,
            "output": output,
        }
        if args := clean_dict(args):
            self._check_run.edit(**args)

    def finish(
        self,
        title: str = None,
        status: CheckRunStatus = None,
        summary: str = None,
        conclusion: CheckRunConclusion = None,
        text: str = None,
        **output,
    ) -> None:
        """Finish the Check Run"""
        # TODO

        conclusions_list_order = {c: i for i, c in enumerate(CheckRunConclusion)}
        for sub_run in self.sub_runs:
            if not sub_run.conclusion:
                sub_run.update(conclusion=CheckRunConclusion.CANCELLED, update_check_run=False)
            if conclusion is None or conclusions_list_order[sub_run.conclusion] < conclusions_list_order[conclusion]:
                conclusion = sub_run.conclusion
                title = None
            if title is None and conclusion == sub_run.conclusion:
                title = sub_run.title

        if conclusion is None:
            conclusion = CheckRunConclusion.STALE
            title = self.name
        if conclusion == CheckRunConclusion.SUCCESS:
            title = "Done"
        elif conclusion == CheckRunConclusion.SKIPPED:
            title = "Skipped"
        elif title is None:
            title = f"{title}: {conclusion.value}"

        summary = self.build_summary(self.sub_runs) or None

        self.update(conclusion=conclusion, title=title, summary=summary)

    def create_sub_run(self, name: str) -> SubRun:
        sub_run = self.SubRun(self, name, status=CheckRunStatus.WAITING)
        self.sub_runs.append(sub_run)
        return sub_run
