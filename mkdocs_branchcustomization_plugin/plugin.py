import re

from mkdocs.plugins import BasePlugin, log
from mkdocs.config.config_options import Type
import git


class BranchPlugin(BasePlugin):
    config_scheme = (
        ('update_config', Type(list)),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = git.Repo('.', search_parent_directories=True)

    def on_config(self, config):
        branch_name = self.repo.active_branch.name
        if self.config['update_config']:
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
