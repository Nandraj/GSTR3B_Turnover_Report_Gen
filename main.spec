# -*- mode: python -*-

import os

path = os.path.abspath(".")

block_cipher = None

a = Analysis(['main.py'],
             pathex=[path],
             binaries=[],
             datas=[('N.ico', '.'), ('chromedriver.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='GSTR-3B Turnover Report',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='N.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='GSTR-3B Turnover Report')