# ngIRCd Container

This repository contains the files needed to build and run ngIRCd as a container image based on AlmaLinux 10.

## Files

- `Containerfile` — installs ngIRCd from EPEL and runs it in the foreground as a non-root user.
- `config/ngircd.conf` — ngIRCd configuration file copied into the image.
- `config/ngircd.motd` — message of the day shown to connecting clients.
- `README_ja.md` — Japanese version of this document.

## Build and run

After adding the configuration files, build and run the image with Podman:

```sh
podman build -t ngircd-container -f Containerfile .
podman run --rm --name ngircd -p 6667:6667 ngircd-container
```

Connect an IRC client to TCP port `6667` on the host running the container.

To change the server configuration, edit `config/ngircd.conf` and rebuild the image. Review the configuration and access controls before exposing the server to the internet.

> **Note:** The `Containerfile` expects `config/ngircd.conf` and `config/ngircd.motd`. These files have not been added yet, so the image cannot be built until they are provided.
