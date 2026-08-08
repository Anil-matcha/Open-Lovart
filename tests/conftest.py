"""Shared test configuration.

tagopen.config instantiates Settings at import time, which requires the two
Slack tokens. Provide dummies so unit tests run without a real environment.
"""

import os

os.environ.setdefault("SLACK_BOT_TOKEN", "xoxb-test")
os.environ.setdefault("SLACK_APP_TOKEN", "xapp-test")
