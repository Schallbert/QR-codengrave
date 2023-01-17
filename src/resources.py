import sys

"""This file just exists to get asset and resources paths right - depending on OS and development environment"""
if 'unittest' in sys.modules:
    asset_path = '../src/assets'
else:
    asset_path = 'src/assets'

if sys.platform.startswith('linux'):  # could be "linux", "linux2", "linux3", ...
    app_icon_path = asset_path + '/qruwu.xbm'
elif sys.platform.startswith('win32'):
    app_icon_path = asset_path + '/qruwu.ico'

app_image_path = asset_path + '/qruwu.png'
app_persistence_path = asset_path + '/persistence.dat'
