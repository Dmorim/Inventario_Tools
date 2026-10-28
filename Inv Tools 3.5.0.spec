# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

RAIZ = Path(SPECPATH).resolve()
FIREBIRD = RAIZ / "Recursos" / "Firebird"
ICONE = RAIZ / "Outros" / "3246761_ghex_hex_software_technology_icon.ico"
VERSAO = RAIZ / "Outros" / "Version_Info.txt"

ARQUIVOS_FIREBIRD = (
    "fbclient.dll",
    "ib_util.dll",
    "icudt52.dll",
    "icudt52l.dat",
    "icuin52.dll",
    "icuuc52.dll",
    "msvcp100.dll",
    "msvcr100.dll",
    "zlib1.dll",
    "firebird.msg",
    "firebird.conf",
)

LOCALES_BABEL = ("pt", "en", "es", "root")

PREFIXOS_DESCARTADOS = (
    ("matplotlib", "mpl-data", "fonts", "afm"),
    ("matplotlib", "mpl-data", "fonts", "pdfcorefonts"),
    ("matplotlib", "mpl-data", "sample_data"),
    ("matplotlib", "mpl-data", "plot_directive"),
)


def descartar_data(nome):
    partes = Path(nome).parts
    if any(partes[:len(prefixo)] == prefixo for prefixo in PREFIXOS_DESCARTADOS):
        return True
    return (
        partes[:2] == ("babel", "locale-data")
        and Path(partes[-1]).stem.split("_")[0] not in LOCALES_BABEL
    )


a = Analysis(
    [str(RAIZ / "Inventario.py")],
    pathex=[str(RAIZ)],
    binaries=[],
    datas=[
        (str(FIREBIRD / nome), "Recursos/Firebird")
        for nome in ARQUIVOS_FIREBIRD
    ],
    hiddenimports=[
        "fdb",
        "pyperclip",
        "darkdetect",
        "matplotlib.backends.backend_tkagg",
    ],
    hookspath=[],
    hooksconfig={"matplotlib": {"backends": ["Agg", "TkAgg"]}},
    runtime_hooks=[],
    excludes=["pytest", "_pytest", "PIL.AvifImagePlugin", "_avif"],
    noarchive=False,
    optimize=0,
)

a.datas = [entrada for entrada in a.datas if not descartar_data(entrada[0])]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Inv Tools 3.5.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(ICONE)],
    version=str(VERSAO),
    contents_directory='Bin',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Inv Tools 3.5.0',
)
