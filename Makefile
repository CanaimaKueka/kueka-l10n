# Makefile


SHELL := sh -e
PKG_NAME := canaima-l10n
LIB_DIR := $(DESTDIR)/usr/lib/$(PKG_NAME)
AUTOSTART_DIR := $(DESTDIR)/etc/xdg/autostart

all: build


build:
	@echo "No se hace nada"


install:
	mkdir -p $(LIB_DIR)
	cp -f check-l10n.py $(LIB_DIR)/
	chmod +x $(LIB_DIR)/check-l10n.py

	# Inicio automatico
	mkdir -p $(AUTOSTART_DIR)
	cp check-l10n.desktop.in $(AUTOSTART_DIR)/check-l10n.desktop


uninstall:
	rm -rf $(LIB_DIR)


clean:
	@echo "No se hace nada"


distclean:
	@echo "No se hace nada"


reinstall: uninstall install
