#!/usr/bin/env python3

import sys
from autopkglib import PlistEditor

class InjectEnvSecrets(PlistEditor):
    description = __doc__
    input_variables = {
        "secrets": {
            "required": True,
            "description": (
                "List of names of secrets to find in env and inject."
            ),
        },
        "hard_fail": {
            "required": False,
            "default": True,
            "description": (
                "Hard fail if secret cannot be found."
            )
        }
    }

    def main(self):
        print(self.env)
        sys.exit(1)
