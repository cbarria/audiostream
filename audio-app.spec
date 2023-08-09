Name: audio-app
Version: 1.0
Release: 1%{?dist}
Summary: Audio Streaming Microphone Application
License: Unlicense
URL: http://nowebsite.com
Source0: %{name}-%{version}.tar.gz

Requires: systemd

%description
This is an Audio Streaming Microphone Application.

%prep
%setup -q

%install
mkdir -p %{buildroot}/usr/local/bin
cp streamserver.py %{buildroot}/usr/local/bin/
cp streamclient.py %{buildroot}/usr/local/bin/
chmod +x %{buildroot}/usr/local/bin/streamserver.py
chmod +x %{buildroot}/usr/local/bin/streamclient.py

mkdir -p %{buildroot}/etc/systemd/system
cp audioserver.service %{buildroot}/etc/systemd/system/
chmod 644 %{buildroot}/etc/systemd/system/audioserver.service

%files
/usr/local/bin/streamserver.py
/usr/local/bin/streamclient.py
/etc/systemd/system/audioserver.service

%post
systemctl daemon-reload
systemctl start audioserver.service
systemctl enable audioserver.service

%postun
# Remove the service on uninstall
if [ $1 -eq 0 ]; then
    systemctl disable audioserver.service >/dev/null 2>&1 || :
fi

%changelog
