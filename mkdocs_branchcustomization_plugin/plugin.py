import re

from mkdocs.plugins import BasePlugin, log
from mkdocs.config.config_options import Type
import git


def get_best_branch_name(repo):
    head = repo.head
    # We're on a branch, just go with it
    if not head.is_detached:
        return repo.active_branch.name
    # This commit is the current master
    if repo.heads.master.commit == head.commit:
        return 'master'
    # Check local branches in lexical order
    for ref in repo.heads:
        if ref.commit == head.commit:
            return ref.name

    # Get names from remotes, prioritizing origin and upstream
    remote_refs = []
    if 'origin' in repo.remotes:
        remote_refs += repo.remotes.origin.refs
    if 'upstream' in repo.remotes:
        remote_refs += repo.remotes.upstream.refs
    for remote in repo.remotes:
        remote_refs += remote.refs

    for ref in remote_refs:
        if ref.remote_head == 'HEAD':
            continue
        if ref.commit == head.commit:
            return ref.remote_head

    return None


class BranchPlugin(BasePlugin):
    config_scheme = (
        ('update_config', Type(list)),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = git.Repo('.', search_parent_directories=True)

    def on_config(self, config):
        branch_name = get_best_branch_name(self.repo)
        log.debug(f"Detected HEAD name: {branch_name}")
        if branch_name is not None and self.config['update_config']:
            for rule in self.config['update_config']:
                match = rule.pop('branch', None)
                if match is None or (match[0], match[-1]) != ('/', '/'):
                    log.error(f"Invalid update_config entry (branch: {match})")
                    continue
                if re.match(match[1:-1], branch_name):
                    log.info(f"Branch {branch_name} matched rule {match}; "
                             f"updating {tuple(rule.keys())}")
                    config.update(rule)
                
        return config
