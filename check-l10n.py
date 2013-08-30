#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  check-l10n.py
#  
#  Copyright 2013 Erick Birbe <erick@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import gobject
import gettext
import gtk
import locale
import os
import pynotify
import subprocess

# Busqueda del directorio por defecto para los locales
lc_dir = os.path.join(os.path.dirname(__file__), 'locale')
if os.path.exists(lc_dir):
    GETTEXT_LOCALEDIR = lc_dir
else:
    GETTEXT_LOCALEDIR = '/usr/share/locale'  # Directorio por defecto

GETTEXT_DOMAIN = "canaima-l10n"


def gettext_install():
    gettext.install(GETTEXT_DOMAIN, GETTEXT_LOCALEDIR)


gettext_install()


APP_NAME = "canima-l10n"
MAIN_LOOP = gobject.MainLoop()


def get_language():
	return locale.getdefaultlocale()[0].replace("_","-").lower()


def get_pkg_name(lang):
	return "canaima-l10n-{}".format(lang)


def is_lang_available(lang):
	pkg_name = get_pkg_name(lang)
	cmd =  "apt-cache pkgnames --generate | grep ^{0}$ | wc -l".format(pkg_name)
	rslt = subprocess.check_output(cmd, shell=True).strip()
	if rslt == "0":
		print _("{} is not available.").format(pkg_name)
		return False
	else:
		print _("{} is available.").format(pkg_name)
		return True


def is_lang_installed(lang):
	pkg_name = get_pkg_name(lang)
	cmd = "aptitude search ~i^{0}$ | wc -l".format(pkg_name)
	rslt = subprocess.check_output(cmd, shell=True).strip()
	if rslt == "0":
		print _("{} is not installed.").format(pkg_name)
		return False
	else:
		print _("{} is installed.").format(pkg_name)
		return True

#TODO: Hacer esto compatible con otros gestores de paquetes
def install(n, action, lang):
	pkg_name = get_pkg_name(lang)
	subprocess.call(["software-center", pkg_name])
	quit_notify(n)


def quit_notify(widget):
	if MAIN_LOOP.is_running():
		MAIN_LOOP.quit()


def main():
	lang = get_language()
	if is_lang_available(lang) and not is_lang_installed(lang):

		n = pynotify.Notification(_("Additional Translations"), _("Your system \
support some additional translations but they are not yet installed."))
		n.connect("closed", quit_notify)
		n.set_urgency(pynotify.URGENCY_NORMAL)
		n.set_timeout(pynotify.EXPIRES_NEVER)
		n.add_action("install", _("Install Now"), install, lang)
		
		try:
			helper = gtk.Button()
			icon = helper.render_icon(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
			n.set_icon_from_pixbuf(icon)
		except:
			print _("Can't load the icon for notification")
			
		n.show()
		MAIN_LOOP.run()


if __name__ == '__main__':
	pynotify.init(APP_NAME)
	main()
	pynotify.uninit()
