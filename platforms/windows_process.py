from __future__ import annotations
import subprocess

CREATE_NO_WINDOW = 0x08000000

def hidden_run(args: list[str], timeout: int = 5) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        creationflags=CREATE_NO_WINDOW,
    )


def hidden_popen(command: str) -> subprocess.Popen[str]:
    return subprocess.Popen(
        command,
        shell=True,
        creationflags=CREATE_NO_WINDOW,
    )
