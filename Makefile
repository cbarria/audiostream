# Makefile for packaging and distributing the audio application

# Variables audio-app-1.0.tar.gz
PACKAGE_NAME = audio-app
PACKAGE_VERSION = 1.0
RPM_BUILD_DIR = ~/rpmbuild
DIST_DIR = dist
TAR_FILE = $(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz

.PHONY: all clean build install package distribute

all: build

clean:
	rm -rf $(DIST_DIR) $(RPM_BUILD_DIR) $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	rm -f $(TAR_FILE)

build:
	mkdir -p $(DIST_DIR)
	cp streamserver.py $(DIST_DIR)/
	cp streamclient.py $(DIST_DIR)/
	cp audioserver.service $(DIST_DIR)/
	chmod +x $(DIST_DIR)/streamserver.py
	chmod +x $(DIST_DIR)/streamclient.py

install:
	sudo cp $(DIST_DIR)/streamserver.py /usr/local/bin/
	sudo cp $(DIST_DIR)/streamclient.py /usr/local/bin/
	sudo cp $(DIST_DIR)/audioserver.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl start audioserver.service
	sudo systemctl enable audioserver.service

package: build
	mkdir -p $(RPM_BUILD_DIR)/{SOURCES,RPMS,BUILD,SPECS}
	mkdir $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	cp $(DIST_DIR)/* $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	tar --create --file $(TAR_FILE) $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	cp $(TAR_FILE) $(RPM_BUILD_DIR)/SOURCES/
	cp audio-app.spec $(RPM_BUILD_DIR)/SPECS/
	rpmbuild -ba $(RPM_BUILD_DIR)/SPECS/$(PACKAGE_NAME).spec
