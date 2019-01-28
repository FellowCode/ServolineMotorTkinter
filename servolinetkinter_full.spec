# -*- mode: python -*-

block_cipher = None

app_name = 'ServolineMotor'


a = Analysis(['src\\main.py'],
     pathex=['C:\\Users\\Admin\\Desktop\\SpeedSensorCompile'],
     binaries=None,
     datas=[('src\\img\\*.png', 'img'),
            ('src\\icon.ico', '.'),],
     hiddenimports=[],
     hookspath=None,
     runtime_hooks=None,
     excludes=None,
     cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
     cipher=block_cipher)

exe = EXE(pyz,
  a.scripts,
  exclude_binaries=True,
  name=app_name,
  debug=False,
  strip=False,
  upx=True,
  console=False,
  icon='src\\icon.ico')

coll = COLLECT(exe,
  a.zipfiles,
  a.binaries,
  a.datas,
  strip=False,
  upx=True,
  name=app_name)