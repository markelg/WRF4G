#!/bin/bash
version="3.1"
thisdir=$(pwd)
wrf4gdir="$(dirname $(dirname $(dirname $0)))/wn"

while test -n "$1"; do
  case $1 in
    "-basedir")
      basedir=$2
      shift
      ;;
    "-tag")
      tag=$2
      shift
      ;;
    "-destdir")
      destdir=$2
      shift
      ;;
    *)
      echo "Usage: $(basename $0) [-tag tag] [-basedir /wrf/bin/base] [-destdir /destination/for/file.tar.gz]" 
      exit
      ;;
  esac
  shift
done

if test -z "${basedir}"; then
  basedir="${wrf4gdir}"
fi
if test -z "${destdir}"; then
  destdir="${thisdir}"
fi

echo "      <<<< BASEDIR: $basedir"

revision=`svn info ${basedir}/WRFV3 | grep 'Last Changed Rev:' | awk -F: '{print $2}' | tr -d ' '`

tardir="tarball${RANDOM}"

mkdir ${tardir}
cd ${tardir}
  mkdir -p WPS/metgrid
  mkdir -p WPS/ungrib
  mkdir -p WRFV3/run

  ln -s ${wrf4gdir}/WPS/ungrib/Variable_Tables_WRF4G WPS/ungrib/

  ln -s ${basedir}/WPS/metgrid/metgrid.exe WPS/metgrid/metgrid.exe
  ln -s ${basedir}/WPS/metgrid/METGRID.TBL.ARW WPS/metgrid/METGRID.TBL
  ln -s ${basedir}/WPS/ungrib/ungrib.exe WPS/ungrib/ungrib.exe
  ln -s ${basedir}/WPS/link_grib.csh WPS/
  
  ln -s ${basedir}/WRFV3/configure.wrf WRFV3
  ln -s ${basedir}/WRFV3/run/*.TBL WRFV3/run
  ln -s ${basedir}/WRFV3/run/*_DATA* WRFV3/run
  ln -s ${basedir}/WRFV3/run/*formatted WRFV3/run/
  ln -s ${basedir}/WRFV3/run/tr* WRFV3/run
  ln -s ${basedir}/WRFV3/run/real.exe WRFV3/run
  ln -s ${basedir}/WRFV3/run/wrf.exe WRFV3/run 
  

  tar czhv --exclude=".svn" \
  -f ${destdir}/WRF4Gbin-${version}_r${revision}${tag}.tar.gz *
cd ..
rm -rf ${tardir}
