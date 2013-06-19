# Makefile


SHELL := sh -e
PKG_NAME := canaima-l10n
LIB_DIR := $(DESTDIR)/usr/lib/$(PKG_NAME)


all: build


build:
	@echo "No se hace nada"


install:
	mkdir -p $(LIB_DIR)
	cp -f check-l10n.py $(LIB_DIR)/

uninstall:
	rm -rf $(LIB_DIR)


clean:
	@echo "No se hace nada"


distclean:
	@echo "No se hace nada"


reinstall: uninstall install
