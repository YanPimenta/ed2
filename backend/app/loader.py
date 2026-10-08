import csv 
import re
import unicodedata

STATUS = {
    "hp": "HP Base",
    "atq": "Attack Base",
    "def": "Defense Base",
    "spa": "Special Attack Base",
    "spd": "Special Defense Base",
    "spe": "Speed Base",
}

# remove acentos e caracteres especiais
def regex_nome(nome:str) -> str:
    s = unicodedata.normalize("NFKD", nome).encode("ASCII", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower().strip())

# transforma os elementos dos pokemons em uma lista unica
def agrupar_elementos(elementos: str) -> list[str]:
    resultado = []
    for elemento in elementos.split(","):
        elemento = elemento.strip()
        if elemento:
            resultado.append(elemento)
    return resultado

# pega o float puro do status
def nmlz_float(carcteristicas: str) -> float:
    return float(carcteristicas.split()[0])

# pega o int puro do status
def nmlz_int(capturas: str) -> int:
    return int(nmlz_float(capturas))

# transforma as habilidades em uma lista de dicionarios
def nmlz_habilidades(habilidade: str) -> list[dict]:
    habilidades = []
    for item in agrupar_elementos(habilidade):
        oculta = "(hidden ability)" in item
        nome = item.replace("(hidden ability)", "").strip()
        if nome and nome[0].isdigit():
            nome = nome.split(" ", 1)[1]
        habilidades.append({"nome": nome, "oculta": oculta})
    return habilidades

# carrega o csv e transforma em uma lista de dicionarios
def carregar_csv(caminho: str) -> list[dict]:
    pokemons = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        for id_pokemon, linha in enumerate(csv.DictReader(arquivo), start=1):
            
            egg_grupo = agrupar_elementos(linha["Egg Groups"])
            
            pokemons.append({
                "id": id_pokemon,
                "nome": linha["Pokemon"],
                "nome_regex": regex_nome(linha["Pokemon"]),
                "elementos": agrupar_elementos(linha["Type"]),
                "altura": nmlz_float(linha["Height"]),
                "peso": nmlz_float(linha["Weight"]),
                "habilidades": nmlz_habilidades(linha["Abilities"]),
                "egg_grupo": egg_grupo,
                "tem_ovo": "Undiscovered" not in egg_grupo,
                "captura": nmlz_int(linha["Catch Rate"]),
                "status": {chave: int(linha[coluna]) for chave, coluna in STATUS.items()},
            })
    return pokemons
