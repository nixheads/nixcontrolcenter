PREFIX ?= /usr
TARGET = nixcontrolcenter
ARCH= all
HOSTARCH=$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)
VERSION = 1.0


deb:
	sed -i "/Version:/c\Version: $(VERSION)" debian/DEBIAN/control
	install -d debian/usr/bin
	install -d debian/usr/share/doc/nixcontrolcenter
	gzip -c --best debian/DEBIAN/changelog >debian/DEBIAN/changelog.Debian.gz
	install -m 644  debian/DEBIAN/changelog.Debian.gz debian/usr/share/doc/nixcontrolcenter
	rm debian/DEBIAN/changelog.Debian.gz
	install -m 644 debian/DEBIAN/copyright debian/usr/share/doc/nixcontrolcenter
	install -d debian/usr/share/applications
	install -d debian/usr/share/pixmaps
	install -d debian/usr/share/nixcc
	install -d debian/usr/share/nixcc/frontend
	install -d debian/usr/share/nixcc/frontend/css
	install -d debian/usr/share/nixcc/frontend/js
	install -d debian/usr/share/nixcc/frontend/icons
	install -d debian/usr/share/nixcc/frontend/icons/modules
	install -d debian/usr/share/nixcc/frontend/images
	install -d debian/usr/share/nixcc/modules
	install -d debian/usr/share/nixcc/modules/hardware
	install -d debian/usr/share/nixcc/modules/software
	install -d debian/usr/share/nixcc/modules/networking
	install -d debian/usr/share/nixcc/modules/desktop
	install -d debian/usr/share/nixcc/modules/system
	install -d debian/usr/share/nixcc/scripts
	install -d debian/usr/share/nixcc/resources
	install -m 755 usr/bin/nixcontrolcenter debian/usr/bin
	install -m 644 usr/share/applications/nixcontrolcenter.desktop debian/usr/share/applications/nixcontrolcenter.desktop
	install -m 644 usr/share/applications/nixcontrolcenter.desktop debian/usr/share/applications/nixcontrolcenter.desktop
	install -m 644 usr/share/pixmaps/nixcontrolcenter.png debian/usr/share/pixmaps/nixcontrolcenter.png
	install -m 644 usr/share/nixcc/nixcontrolcenter.py  debian/usr/share/nixcc/nixcontrolcenter.py
	install -m 644 usr/share/nixcc/resources/* debian/usr/share/nixcc/resources
	install -m 755 usr/share/nixcc/scripts/*  debian/usr/share/nixcc/scripts
	install -m 644 usr/share/nixcc/modules/hardware/*  debian/usr/share/nixcc/modules/hardware
	install -m 644 usr/share/nixcc/modules/software/*  debian/usr/share/nixcc/modules/software
	install -m 644 usr/share/nixcc/modules/networking/*  debian/usr/share/nixcc/modules/networking
	install -m 644 usr/share/nixcc/modules/desktop/*  debian/usr/share/nixcc/modules/desktop
	install -m 644 usr/share/nixcc/modules/system/*  debian/usr/share/nixcc/modules/system
	install -m 644 usr/share/nixcc/frontend/css/*  debian/usr/share/nixcc/frontend/css
	install -m 644 usr/share/nixcc/frontend/js/*  debian/usr/share/nixcc/frontend/js
	install -m 644 usr/share/nixcc/frontend/icons/*.png  debian/usr/share/nixcc/frontend/icons
	install -m 644 usr/share/nixcc/frontend/icons/modules/*  debian/usr/share/nixcc/frontend/icons/modules
	install -m 644 usr/share/nixcc/frontend/images/*  debian/usr/share/nixcc/frontend/images
	install -m 644 usr/share/nixcc/frontend/*.html  debian/usr/share/nixcc/frontend



	fakeroot dpkg-deb --build debian $(TARGET)_$(VERSION)_$(ARCH).deb
	rm -rf debian/usr




all: deb
