#--------------------------------
# import modules
#--------------------------------
from anuga.validation_utilities.fabricate import *
from anuga.validation_utilities import run_validation_script
from anuga.validation_utilities import typeset_report


# Setup the python scripts which produce the output for this
# validation test
def build():
    run_validation_script('runup.py')
    run_validation_script('runuplot.py')
    typeset_report()

def clean():
    autoclean()

main()
