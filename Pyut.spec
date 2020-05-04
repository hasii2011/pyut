# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'src/org/pyut/resources/loggingConfiguration.json', 'org/pyut/resources/' ),
         ( 'src/org/pyut/resources/Help.txt', 'org/pyut/resources/' ),
         ( 'src/org/pyut/resources/Kilroy-Pyut.txt', 'org/pyut/resources/' ),
         ( 'src/org/pyut/resources/Kudos.txt', 'org/pyut/resources/' )
         ]
a = Analysis(['src/Pyut.py'],
             pathex=['/Users/humberto.a.sanchez.ii/PycharmProjects/PyUt'],
             binaries=[],
             datas=added_files,
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
          [],
          exclude_binaries=True,
          name='Pyut',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Pyut')
