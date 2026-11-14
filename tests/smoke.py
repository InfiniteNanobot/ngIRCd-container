#!/usr/bin/env python3
"""Build the image and exercise an IRC connection with Podman."""

import os
from pathlib import Path
import socket
import subprocess
import time

ROOT = Path(__file__).resolve().parent.parent
IMAGE = os.environ.get("NGIRCD_TEST_IMAGE", "localhost/ngircd-container-smoke:latest")


def podman(*args):
    return subprocess.run(
        ["podman", *args], check=True, text=True, capture_output=True, timeout=300
    ).stdout.strip()


def main():
    subprocess.run(
        ["podman", "build", "-t", IMAGE, "-f", str(ROOT / "Containerfile"), str(ROOT)],
        check=True,
        timeout=900,
    )
    user = podman("image", "inspect", "--format", "{{.Config.User}}", IMAGE)
    if user != "ngircd:ngircd":
        raise RuntimeError(f"unexpected image user: {user!r}")
    podman("run", "--rm", IMAGE, "-t")

    container = podman("run", "-d", "--rm", "-p", "127.0.0.1::6667", IMAGE)
    try:
        address = podman("port", container, "6667/tcp")
        port = int(address.rsplit(":", 1)[1])
        deadline = time.monotonic() + 15
        while True:
            try:
                connection = socket.create_connection(("127.0.0.1", port), timeout=1)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.2)

        with connection:
            connection.settimeout(10)
            connection.sendall(b"NICK smoke\r\nUSER smoke 0 * :Smoke Test\r\n")
            response = b""
            while b" 376 " not in response:
                chunk = connection.recv(4096)
                if not chunk:
                    raise RuntimeError(f"connection closed: {response!r}")
                response += chunk
                if len(response) > 65536:
                    raise RuntimeError("unexpectedly large IRC response")
            if b" 001 smoke " not in response or b"Welcome to the IRC server." not in response:
                raise RuntimeError(f"unexpected IRC welcome: {response!r}")
            connection.sendall(b"PING :smoke-test\r\n")
            while b"PONG" not in response or b"smoke-test" not in response:
                chunk = connection.recv(4096)
                if not chunk:
                    raise RuntimeError(f"connection closed: {response!r}")
                response += chunk
                if len(response) > 65536:
                    raise RuntimeError("unexpectedly large IRC response")
        print("IRC smoke test passed")
    finally:
        subprocess.run(
            ["podman", "stop", "--time", "2", container],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
        )


if __name__ == "__main__":
    main()
