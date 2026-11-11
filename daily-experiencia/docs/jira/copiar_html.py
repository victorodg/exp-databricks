"""Põe um .md na área de transferência como HTML formatado (CF_HTML) e texto puro, sem a linha do título."""
import ctypes, re, sys
import markdown

t = re.sub(r"^# [^\n]*\n\n", "", open(sys.argv[1], encoding="utf-8").read())
t = re.sub(r"^ {2,3}- ", "    - ", t, flags=re.M)  # o conversor só aninha listas recuadas com 4 espaços
corpo = markdown.markdown(t, extensions=["sane_lists"])
html = f"<html><body><!--StartFragment-->{corpo}<!--EndFragment--></body></html>"
cab = "Version:0.9\r\nStartHTML:{:010d}\r\nEndHTML:{:010d}\r\nStartFragment:{:010d}\r\nEndFragment:{:010d}\r\n"
tam = len(cab.format(0, 0, 0, 0).encode("utf-8"))
b = html.encode("utf-8")
ini = tam + b.index(b"<!--StartFragment-->") + len("<!--StartFragment-->")
fim = tam + b.index(b"<!--EndFragment-->")
cf_html = cab.format(tam, tam + len(b), ini, fim).encode("utf-8") + b + b"\x00"

k32, u32 = ctypes.windll.kernel32, ctypes.windll.user32
k32.GlobalAlloc.restype = ctypes.c_void_p; k32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
k32.GlobalLock.restype = ctypes.c_void_p; k32.GlobalLock.argtypes = [ctypes.c_void_p]
k32.GlobalUnlock.argtypes = [ctypes.c_void_p]
u32.SetClipboardData.restype = ctypes.c_void_p; u32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
u32.OpenClipboard.argtypes = [ctypes.c_void_p]
u32.RegisterClipboardFormatW.restype = ctypes.c_uint
def bloco(dados):
    h = k32.GlobalAlloc(0x0002, len(dados)); p = k32.GlobalLock(h); ctypes.memmove(p, dados, len(dados)); k32.GlobalUnlock(h); return h
assert u32.OpenClipboard(None)
u32.EmptyClipboard()
assert u32.SetClipboardData(u32.RegisterClipboardFormatW("HTML Format"), bloco(cf_html))
assert u32.SetClipboardData(13, bloco(t.replace("\n", "\r\n").encode("utf-16-le") + b"\x00\x00"))
u32.CloseClipboard()
print("copiado como HTML:", corpo.count("<h2>"), "títulos,", corpo.count("<li>"), "itens de lista,", corpo.count("<strong>"), "negritos")
