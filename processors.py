import sys

from datamodels import *
import importlib


class PayloadProcessor:
    def __init__(self, config: dict, model: BaseModel) -> None:
        self.config = config
        self.model = model
        self.process_payload()

    def process_payload(self):
        self.process_jobs(self.config['jobs'])

    def process_jobs(self, jobs: dict):
        try:
            for job in jobs:
                self.process_job(job=job)
        except KeyError:
            pass

    def process_job(self, job: dict):
        if self.validate_rules(rules=job['rules']):
            self.process_actions(job['actions'])

    def validate_rules(self, rules: dict) -> bool:
        try:
            for rule in rules:
                if self.validate_rule(rule=rule):
                    return True
        except KeyError:
            return True
        return False

    def validate_rule(self, rule: str) -> bool:
        model = self.model
        return eval(rule)

    def process_actions(self, actions: dict):
        for action in actions:
            self.process_action(action=action)

    def process_action(self, action: dict):
        try:
            spec = importlib.util.find_spec("."+action['module'], package=".builtins")
            m = importlib.util.module_from_spec(spec)
            sys.modules[".builtins."+action['module']] = m
            spec.loader.exec_module(m)
            class_ = getattr(m, str(action['module']).capitalize())
            instance = class_(config=self.config, action=action)
            method = getattr(instance, str(action['action']))
            result = method()
        except KeyError:
            print(f"Module configuration for {action['module']} is not valid")
            pass
