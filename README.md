# ngIRCd-container

This repository contains the files needed to build and run ngIRCd as a container image based on AlmaLinux 10.

## Files

- `Containerfile` — installs ngIRCd from EPEL and runs it in the foreground as a non-root user.
- `config/ngircd.conf` — ngIRCd configuration file copied into the image.
- `config/ngircd.motd` — message of the day shown to connecting clients.
- `tests/smoke.py` — builds the image and tests an IRC connection with Podman.
- `README_ja.md` — Japanese version of this document.

## Build and run

Build and run the image with Podman:

```sh
podman build -t ngircd-container -f Containerfile .
podman run --rm --name ngircd -p 127.0.0.1:6667:6667 ngircd-container
```

Connect an IRC client to `127.0.0.1:6667` on the host. This example publishes the port only on the host loopback interface.

The sample configuration has no authentication or TLS. It is intended for local testing, not public deployment. Before accepting remote connections, configure access controls and TLS, review the server name and settings, and change the published host address as needed. IRC passwords are sent in plaintext without TLS.

To change the server configuration or MOTD, edit the files in `config/` and rebuild the image. The configuration and MOTD must be readable by the `ngircd` user. The server must listen on a container-accessible address; if a PID file is configured, place it under `/run/ngircd`.

## Test

With Podman and Python 3 installed, run `python3 tests/smoke.py` to build the image, validate the configuration and test an IRC connection. The test binds a temporary port on host loopback and removes its container afterward. Set `NGIRCD_TEST_IMAGE` to override the test image tag.

> **Note:** EPEL 10 does not currently package ngIRCd, so the AlmaLinux 10 image installs the signed EPEL 9 package.
