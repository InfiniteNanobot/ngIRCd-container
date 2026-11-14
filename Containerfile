# ngIRCd is not currently packaged in EPEL 10. Download the signed EPEL 9
# package for the target architecture and install it on AlmaLinux 10.
FROM almalinux:9 AS epel-package

RUN dnf -y install epel-release \
    && dnf -y install --downloadonly --downloaddir=/tmp/rpms ngircd

FROM almalinux:10

COPY --from=epel-package /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-9 /tmp/RPM-GPG-KEY-EPEL-9
COPY --from=epel-package /tmp/rpms/ /tmp/rpms/

RUN rpm --import /tmp/RPM-GPG-KEY-EPEL-9 \
    && dnf -y --setopt=localpkg_gpgcheck=1 install /tmp/rpms/ngircd-*.rpm \
    && mkdir -p /run/ngircd \
    && chown ngircd:ngircd /run/ngircd \
    && dnf clean all \
    && rm -rf /var/cache/dnf /tmp/rpms /tmp/RPM-GPG-KEY-EPEL-9

COPY config/ngircd.conf /etc/ngircd.conf
COPY config/ngircd.motd /etc/ngircd.motd

USER ngircd:ngircd

EXPOSE 6667/tcp

ENTRYPOINT ["/usr/sbin/ngircd", "-n", "-f", "/etc/ngircd.conf"]
