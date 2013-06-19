#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# COPYRIGHT: C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
# Este script genera automáticamente el archivo 'debian/control' para 
# hacer el empaquetado. Los valores son tomados del archivo locales.dict

from string import Template
import os

MYDIR = os.path.dirname(os.path.realpath(__file__))

I18N_PACKAGES = None
if not I18N_PACKAGES:
    f = open(MYDIR + '/../l10n_pkgs.dict', 'r')
    data = f.read()
    I18N_PACKAGES = eval(data)


def prepare_condition(pkgs):
    '''Resuelve el conflicto generado entre hunspell y myspell que no 
    permite instalarlos juntos. Para resolverlos concatena ambas
    dependencias en una sentencia de selección como
    (myspell-xx-xx | hunspell-xx-xx)'''
    i = 0
    for item in pkgs:
        if type(item) is type([]):
            condition = ""
            len_i=len(item)
            k = 0
            for p in item:
                if k > 0 and k < len_i:
                    condition += ' | '
                condition += p
                k += 1
            pkgs[i] = condition
            
        i += 1
    return pkgs


# Cabecera de la plantilla
tmplt_head = """Source: canaima-l10n
Section: metapackages
Priority: optional
Maintainer: Erick Birbe <erickcion@gmail.com>
Build-Depends: python,
	debhelper (>= 9)
Standards-Version: 3.9.4
Homepage: http://canaima.softwarelibre.gob.ve/
Vcs-Git: git://git.canaima.sotfwarelibre.gob.ve/canaima-l10n.git
Vcs-Browser: http://git.canaima.softwarelibre.gob.ve/?p=canaima-l10n.git;a=tree

Package: canaima-l10n
Architecture: all
Depends:python-notify,
	${python:Depends}
        ${misc:Depends}
Description: Check for language packs installation in Canaima GNU/Linux
 This package help users to install complete package support in Canaima
 GNU/Linux.
"""

# Plantilla de los paquetes a generar
tmplt = Template("""
Package: canaima-l10n-$lang
Architecture: all
Depends:$pkgs_list,
        $${misc:Depends}
Description: Package for '$lang' language in Canaima
 This metapackage privides the additional software for $lang language.
""")

# Ensamblaje de la plantilla
tmplt_list = ''
for lang in I18N_PACKAGES:
    if len(I18N_PACKAGES[lang]) > 0:        
        orig_list = prepare_condition(I18N_PACKAGES[lang])
        pkg_list = ''
        for pkg in orig_list:
            if pkg_list == '':
                pkg_list = pkg
            else:
                pkg_list = "%s,\n        %s" % (pkg_list, pkg)
        tmplt_list += tmplt.substitute(lang=lang, pkgs_list=pkg_list)

print tmplt_head + tmplt_list
