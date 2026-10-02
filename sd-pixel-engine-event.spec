block_cipher = None

a = Analysis(['sd_pixel_engine_event/__main__.py'],
             pathex=[],
             binaries=None,
             datas=None,
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
          name='sd-pixel-engine-event',
          contents_directory=".",
          debug=False,
          strip=False,
          upx=True,
          console=True,
          upx_exclude=[
            '_uuid.pyd',
            'vcruntime140.dll',
            'ucrtbase.dll',
            'python3.dll',
            'python311.dll',
            ],
          )
          
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='sd-pixel-engine-event')