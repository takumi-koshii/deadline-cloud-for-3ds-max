# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

from __future__ import annotations

import runpy
from unittest.mock import patch

import pytest


def test_running_as_module_starts_the_entrypoint_once() -> None:
    """`python -m deadline.max_adaptor.MaxAdaptor` must run the adaptor once.

    The background daemon is launched as `python -m deadline.max_adaptor.MaxAdaptor daemon _serve`.
    Running main() twice makes that process start a second backend after `daemon stop`, which then
    waits for a shutdown request that never comes, so the process never exits.
    """
    with patch("openjd.adaptor_runtime.EntryPoint") as mock_entrypoint:
        with pytest.raises(SystemExit) as exc_info:
            runpy.run_module("deadline.max_adaptor.MaxAdaptor", run_name="__main__", alter_sys=True)

    assert mock_entrypoint.return_value.start.call_count == 1
    assert exc_info.value.code == 0
