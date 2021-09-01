#!/usr/bin/env python3

import sys
from autopkglib import PlistEditor, ProcessorError

class InjectEnvSecrets(PlistEditor):
    description = __doc__
    input_variables = {
        "INJECTABLE_SECRETS": {
            "required": False,
            "description": (
                "List of names of secrets to find in env and inject."
            ),
        },
        "HARD_FAIL_SECRETS_INJECTION": {
            "required": False,
            "default": True,
            "description": (
                "Hard fail if secret cannot be found."
            )
        },
        "ENV_SECRETS_PREFIX": {
            "required": False,
            "description": (
                "Prefix for secrets in env. Ie, $<PREFIX>_<SECRET_NAME>. Defaults to $AUTOPKG_<UPPERCASE_RECIPE_NAME>"
            )
        }
    }

    @property
    def prefix(self):
        self.env.get("ENV_SECRETS_PREFIX", f"AUTOPKG_{self.env['NAME'].upper()}_")

    @property
    def secrets(self):
        self.env.get("INJECTABLE_SECRETS")

    @property
    def hard_fail(self):
        self.env.get("HARD_FAIL_SECRETS_INJECTION")

    def inject_secrets(self):
        for key in self.secrets:
            env_key = f"{self.prefix}_{key}"
            env_secret = os.environ.get(env_key)
            if key is None and self.hard_fail:
                raise ProcessorError(f"Could not find secret {key} for recipe {self.env['NAME']} - looked in environment at {env_key}")
            elif key is None:
                continue

            self.env[key] = env_secret

    def main(self):
        if not self.secrets:
            return

        self.inject_secrets()
