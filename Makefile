# Makefile

SHELL := sh -e
PKG_NAME := canaima-l10n
LIB_DIR := $(DESTDIR)/usr/lib/$(PKG_NAME)
AUTOSTART_DIR := $(DESTDIR)/etc/xdg/autostart

# Variables de tradicciones
DOMAIN_NAME = canaima-l10n
LC_DIRS = $(shell ls locale)

all: build


build: gen-mo-files


install:
	mkdir -p $(LIB_DIR)
	cp -f check-l10n.py $(LIB_DIR)/
	chmod +x $(LIB_DIR)/check-l10n.py

	# Inicio automatico
	mkdir -p $(AUTOSTART_DIR)
	cp check-l10n.desktop.in $(AUTOSTART_DIR)/check-l10n.desktop
	
	# Instalar traducciones
	mkdir -p $(DESTDIR)/usr/share/locale/
	for LC in $(LC_DIRS); do \
		LOCALE_DIR=locale/$${LC}; \
		if [ -d $${LOCALE_DIR} ]; then \
			cp -r $${LOCALE_DIR} $(DESTDIR)/usr/share/locale/; \
		fi; \
	done


uninstall:
	rm -rf $(LIB_DIR)

	# Desinstalar traducciones
	rm -f $(DESTDIR)/usr/share/locale/*/LC_MESSAGES/$(DOMAIN_NAME).mo


clean: clean-mo-files


distclean:
	@echo "No se hace nada"


reinstall: uninstall install


gen-pot-template:
	mkdir -p locale/
	find . -type f -name \*.py | xgettext --language=Python --copyright-holder \
	"Erick Birbe <erickcion@gmail.com>" --package-name "$(PKG_NAME)" \
	--msgid-bugs-address "desarrolladores@canaima.softwarelibre.gob.ve" -F \
	-o locale/messages.pot -f -


update-po-files: gen-pot-template
	msgmerge locale/es.po locale/messages.pot -o locale/es.po


gen-mo-files:
	mkdir -p locale/es/LC_MESSAGES/
	msgfmt locale/es.po -o locale/es/LC_MESSAGES/$(DOMAIN_NAME).mo


clean-mo-files:
	for LC in $(LC_DIRS); do \
		LOCALE_DIR=locale/$${LC}; \
		if [ -d $${LOCALE_DIR} ]; then \
			rm -r $${LOCALE_DIR}/; \
		fi; \
	done
