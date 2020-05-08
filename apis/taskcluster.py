#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from components.utilities import logEntryExit, INeedsCommandProvider


class DefaultTaskclusterProvider(INeedsCommandProvider):
    def __init__(self, config):
        self._vcs_setup_initialized = False
        super().__init__(config)

    @logEntryExit
    def _vcs_setup(self):
        if not self._vcs_setup_initialized:
            self.run(["./mach", "vcs-setup", "--update"])
            self._vcs_setup_initialized = True
        self._vcs_setup_initialized = False

    @logEntryExit
    def submit_to_try(self, library):
        self._vcs_setup()
        ret = self.run(
            ["./mach", "try", "fuzzy", "--query", library.fuzzy_query])
        output = ret.stdout.decode()

        isNext = False
        try_link = "Unknown"
        for l in output.split("\n"):
            if isNext:
                try_link = l.replace("remote:", "").strip()
                break
            if "Follow the progress of your build on Treeherder:" in l:
                isNext = True

        try_link = try_link.replace(
            "https://treeherder.mozilla.org/#/jobs?repo=try&revision=", "")
        return try_link
