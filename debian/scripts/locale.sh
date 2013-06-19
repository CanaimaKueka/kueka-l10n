#!/bin/bash -e


apt-get update

OUT_FILE="locales.out"
SIZE=0
LIST=""
LOCALES="$( cat /usr/share/i18n/SUPPORTED | tr '[:upper:]' '[:lower:]' | sed 's/_/-/;s/[.@ ].*//' | sort -u )"

echo "" > $OUT_FILE
echo "{" | tee -a $OUT_FILE

for L in ${LOCALES}; do
	ROOTLC="${L%-*}"
	BUFFER="["
	for P in manpages hunspell myspell ispell aspell guacharo-l10n \
	cunaguaro-l10n libreoffice-l10n libreoffice-help; do
		if apt-get --print-uris download "$P-$L" 1>/dev/null 2>&1; then
			BUFFER="${BUFFER}'$P-$L', "
			LIST="${LIST} $P-$L"
			SIZE="$( apt-cache show "$P-$L" | grep "Installed-Size: " | awk '{print $2}' )+${SIZE}"
		elif apt-get --print-uris download "$P-$ROOTLC" 1>/dev/null 2>&1; then
			BUFFER="${BUFFER}'$P-$ROOTLC', "
			LIST="${LIST} $P-$ROOTLC"
			SIZE="$( apt-cache show "$P-$ROOTLC" | grep "Installed-Size: " | awk '{print $2}' )+${SIZE}"
		fi
	done
	echo "'$L': ${BUFFER}]," | tee -a $OUT_FILE
done
echo "}" | tee -a $OUT_FILE

echo "La lista de paquetes a incluir en el pool de la ISO:"
echo "${LIST}" | sort -u

echo "EL tamaño sin comprimir de todos los paquetes:"
echo "${SIZE}" | bc
