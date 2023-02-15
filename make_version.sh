#!/bin/bash

# Version updating rules:
#
# - If you restructure the package to a large extent, raise the major version.
# - If you add or modify the API of a function or a class and you think it may affect other people, raise the minor version.
# - If you make bug fixes, docstring updates or anything that does not change the API of the package, just run the script to get the patch version updated.
#
# To compare version strings, use:
#
# ```
# from packaging import version
# print(version.parse("1.1.3") > version.parse("1.100.4a"))
# ```

MAJOR_VERSION=1
MINOR_VERSION=0

VERSION_YEAR=`date -u +'%Y'`
VERSION_MONTH=`date -u +'%m'`
VERSION_DAY=`date -u +'%d'`
VERSION_DATE=`date -u +'%Y%m%d'`
VERSION_HOUR=`date -u +'%H'`
VERSION_MINUTE=`date -u +'%M'`

PATCH_VERSION=${VERSION_YEAR}${VERSION_MONTH}${VERSION_DAY}${VERSION_HOUR}${VERSION_MINUTE}

SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
VERSION_DIRPATH=${SCRIPT_PATH}/mb_utils/src
VERSION_FILEPATH=${VERSION_DIRPATH}/version.py

##Run the make_version file to update the version number and then run install package file to install the package and upload it to pipy.
# version.py
mkdir -p ${VERSION_DIRPATH}
echo "Updating ${VERSION_FILEPATH}..."
echo "VERSION_YEAR = ${VERSION_YEAR}"$'\r' > ${VERSION_FILEPATH}
echo "VERSION_MONTH = int('${VERSION_MONTH}')"$'\r' >> ${VERSION_FILEPATH}
echo "VERSION_DAY = int('${VERSION_DAY}')"$'\r' >> ${VERSION_FILEPATH}
echo "VERSION_HOUR = int('${VERSION_HOUR}')"$'\r' >> ${VERSION_FILEPATH}
echo "VERSION_MINUTE = int('${VERSION_MINUTE}')"$'\r\r' >> ${VERSION_FILEPATH}

echo "MAJOR_VERSION = ${MAJOR_VERSION}"$'\r' >> ${VERSION_FILEPATH}
echo "MINOR_VERSION = ${MINOR_VERSION}"$'\r' >> ${VERSION_FILEPATH}
echo "PATCH_VERSION = ${PATCH_VERSION}"$'\r' >> ${VERSION_FILEPATH}
echo "version_date = '${VERSION_YEAR}/${VERSION_MONTH}/${VERSION_DAY} ${VERSION_HOUR}:${VERSION_MINUTE}'"$'\r' >> ${VERSION_FILEPATH}
echo "version = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)"$'\r' >> ${VERSION_FILEPATH}

echo "__all__  = ['MAJOR_VERSION', 'MINOR_VERSION', 'PATCH_VERSION', 'version_date', 'version']"$'\r' >> ${VERSION_FILEPATH}
