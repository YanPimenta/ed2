import ctypes
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "c" / "libed2.so"

_lib = ctypes.CDLL(str(LIB))

_lib.sl_criar.restype = ctypes.c_void_p
_lib.sl_destruir.argtypes = [ctypes.c_void_p]
_lib.sl_inserir.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
_lib.sl_inserir.restype = ctypes.c_int
_lib.sl_buscar.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
_lib.sl_buscar.restype = ctypes.c_int
_lib.sl_prefixo.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int,
]
_lib.sl_prefixo.restype = ctypes.c_int
_lib.sl_tamanho.argtypes = [ctypes.c_void_p]
_lib.sl_tamanho.restype = ctypes.c_int


# Skip List em C: chave = nome normalizado, valor = id do Pokémon
class SkipList:
    def __init__(self):
        self._sl = _lib.sl_criar()
        if not self._sl:
            raise MemoryError("falha ao criar a Skip List")

    def inserir(self, chave: str, valor: int) -> bool:
        resultado = _lib.sl_inserir(self._sl, chave.encode(), valor)
        if resultado < 0:
            raise MemoryError("falha ao inserir na Skip List")
        return resultado == 1

    def buscar(self, chave: str) -> int | None:
        valor = ctypes.c_int()
        if _lib.sl_buscar(self._sl, chave.encode(), ctypes.byref(valor)):
            return valor.value
        return None

    # ids cujo nome começa com o prefixo, em ordem alfabética
    def prefixo(self, prefixo: str, limite: int = 10) -> list[int]:
        if limite <= 0:
            return []
        saida = (ctypes.c_int * limite)()
        total = _lib.sl_prefixo(self._sl, prefixo.encode(), saida, limite)
        return list(saida[:total])

    def __len__(self) -> int:
        return _lib.sl_tamanho(self._sl)

    def __del__(self):
        if getattr(self, "_sl", None):
            _lib.sl_destruir(self._sl)
            self._sl = None
