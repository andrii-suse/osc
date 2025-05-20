import sys

import osc.commandline_git


class PullRequestListCommand(osc.commandline_git.GitObsCommand):
    """
    List pull requests in a repository
    """

    name = "list"
    parent = "PullRequestCommand"

    def init_arguments(self):
        self.add_argument_owner_repo(nargs="+")
        self.add_argument(
            "--state",
            choices=["open", "closed", "all"],
            default="open",
            help="State of the pull requests (default: open)",
        )
        self.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format (default: open)",
        )
        self.add_argument(
            "--json",
            action="store_true",
            help="Print output in json",
        )

    def run(self, args):
        from osc import gitea_api
        from osc.output.formatter_creator import FormatterCreator

        self.print_gitea_settings()

        formatter = FormatterCreator().formatter_from_args(args)
        formatter.start()

        total_entries = 0
        for owner, repo in args.owner_repo:
            pr_obj_list = gitea_api.PullRequest.list(self.gitea_conn, owner, repo, state=args.state)

            if pr_obj_list:
                total_entries += len(pr_obj_list)
                pr_obj_list.sort()
                formatter.format_list(pr_obj_list)

        formatter.finish(f"Total entries: {total_entries}")
