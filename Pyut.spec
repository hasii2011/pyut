# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Pyut.py'],
             pathex=['/Users/humberto.a.sanchez.ii/PycharmProjects/PyUt/src'],
             binaries=[],
             datas=[('org/pyut/resources/loggingConfiguration.json', 'org.pyut.resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Pyut',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='Pyut.app',
             icon=None,
             bundle_identifier=None)
