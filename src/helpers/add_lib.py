import os
import sys

# remove clutter in dist folder by moving non-critical parts of the application to lib/
sys.path.append(os.path.join(os.getcwd(), 'lib'))
