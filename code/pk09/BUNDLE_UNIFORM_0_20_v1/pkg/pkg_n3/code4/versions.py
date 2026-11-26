# Print the versions of the numerical packages used by the certifier (for the review manifest).
import sys
import numpy, scipy, flint
print('python %s; numpy %s; scipy %s; python-flint %s' % (sys.version.split()[0], numpy.__version__, scipy.__version__, flint.__version__))
