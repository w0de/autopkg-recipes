#!/usr/bin/env python3

import os
from autopkglib import PlistEditor, ProcessorError

class InjectEnvSecrets(PlistEditor):
    description = __doc__
    input_variables = {
        "injectable_secrets": {
            "required": False,
            "description": (
                "List of names of secrets to find in env and inject."
            ),
        },
        "hard_fail_secrets_injection": {
            "required": False,
            "default": True,
            "description": (
                "Hard fail if secret cannot be found."
            )
        },
        "injectable_secrets_env_prefix": {
            "required": False,
            "description": (
                "Prefix for secrets in env. Ie, $<PREFIX>_<SECRET_NAME>. Defaults to $AUTOPKG_<UPPERCASE_RECIPE_NAME>"
            )
        }
    }

    @property
    def prefix(self):
        return self.env.get("injectable_secrets_env_prefix", f"AUTOPKG_{self.env['NAME'].upper()}")

    @property
    def secrets(self):
        return self.env.get("injectable_secrets")

    @property
    def hard_fail(self):
        return self.env.get("hard_fail_secrets_injection")

    def inject_secrets(self):
        for key in self.secrets:
            env_key = f"{self.prefix}_{key}"
            env_secret = os.environ.get(env_key)
            if env_secret is None and self.hard_fail:
                raise ProcessorError(f"Could not find secret {key} for recipe {self.env['NAME']} - looked in environment at {env_key}")
            elif env_secret is None:
                continue

            self.env[key] = env_secret

    def main(self):
        if not self.secrets:
            return None

        if not isinstance(self.secrets, list):
            raise ProcessorError(f"'injectable_secrets' must be an array if set.")

        self.inject_secrets()
