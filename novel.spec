# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['novel.py', 'catalog.py', 'novel_glob.py', 'content.py', 'debug.py', 'highlighter.py', 'log.py', 'purify.py', 'QDialog_ReadNetJson.py', 'QFrame_BookShelfImage.py'],
             pathex=['D:\\PythonProject\\毕业设计'],
             binaries=[],
             datas=[],
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
          name='novel',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='D:\\PythonProject\\毕业设计\\Resource\\favicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='novel')
