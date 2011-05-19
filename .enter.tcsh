# To activate this file: chmod 600 .enter.tcsh
# To deactivate this file: chmod 640 .enter.tcsh
# To turn off the virtualenv, type: deactivate

# Don't do anything if a virtual environment is already loaded
if ( ${?VIRTUAL_ENV} == "1" ) exit 0

printf 'Activating the "%s" virtual environment.\n' `basename $PWD`
source bin/activate.csh >& /dev/null
