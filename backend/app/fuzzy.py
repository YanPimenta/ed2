from app.loader import regex_nome
from app.skiplist import SkipList

DISTANCIA_MAX = 2


# distância de edição (inserção, remoção, troca) entre duas strings
def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    anterior = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        atual = [i]
        for j, cb in enumerate(b, start=1):
            atual.append(min(
                anterior[j] + 1,
                atual[j - 1] + 1,
                anterior[j - 1] + (ca != cb),
            ))
        anterior = atual
    return anterior[-1]


# candidatos pelas primeiras letras na Skip List; devolve ids com distância <= 2, mais próximos primeiro
def buscar_fuzzy(sl: SkipList, nomes: dict[int, str], consulta: str, limite: int = 5) -> list[int]:
    consulta = regex_nome(consulta)
    if not consulta:
        return []

    for tam in (3, 2):
        candidatos = sl.prefixo(consulta[:tam], len(sl))
        proximos = []
        for id_pokemon in candidatos:
            distancia = levenshtein(consulta, nomes[id_pokemon])
            if distancia <= DISTANCIA_MAX:
                proximos.append((distancia, nomes[id_pokemon], id_pokemon))
        if proximos:
            proximos.sort()
            return [id_pokemon for _, _, id_pokemon in proximos[:limite]]
    return []
