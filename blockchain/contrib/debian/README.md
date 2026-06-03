
Debian
====================
This directory contains files used to package commoncoind/commoncoin-qt
for Debian-based Linux systems. If you compile commoncoind/commoncoin-qt yourself, there are some useful files here.

## commoncoin: URI support ##


commoncoin-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install commoncoin-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your commoncoin-qt binary to `/usr/bin`
and the `../../share/pixmaps/commoncoin128.png` to `/usr/share/pixmaps`

commoncoin-qt.protocol (KDE)

