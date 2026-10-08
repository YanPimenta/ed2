import unittest
from pathlib import Path

from app.fuzzy import buscar_fuzzy, levenshtein
from app.loader import carregar_csv
from app.skiplist import SkipList

CSV = Path(__file__).resolve().parents[2] / "data" / "pokemon.csv"


class TestFuzzy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pokemons = carregar_csv(str(CSV))
        cls.sl = SkipList()
        for p in cls.pokemons:
            cls.sl.inserir(p["nome_regex"], p["id"])
        cls.nomes = {p["id"]: p["nome_regex"] for p in cls.pokemons}
        cls.por_nome = {p["nome"]: p["id"] for p in cls.pokemons}

    def busca(self, consulta, limite=5):
        return buscar_fuzzy(self.sl, self.nomes, consulta, limite)

    def test_levenshtein(self):
        self.assertEqual(levenshtein("", ""), 0)
        self.assertEqual(levenshtein("abc", "abc"), 0)
        self.assertEqual(levenshtein("abc", ""), 3)
        self.assertEqual(levenshtein("kitten", "sitting"), 3)
        self.assertEqual(levenshtein("pikchu", "pikachu"), 1)

    def test_pikchu(self):
        self.assertEqual(self.busca("pikchu")[0], self.por_nome["Pikachu"])

    def test_charisard(self):
        self.assertEqual(self.busca("charisard")[0], self.por_nome["Charizard"])

    def test_normaliza_consulta(self):
        self.assertEqual(self.busca("PIKCHU!")[0], self.por_nome["Pikachu"])

    def test_sem_candidatos(self):
        self.assertEqual(self.busca("zzzzzzzz"), [])
        self.assertEqual(self.busca(""), [])

    def test_respeita_limite_e_distancia(self):
        resultado = self.busca("charmande", limite=2)
        self.assertLessEqual(len(resultado), 2)
        for id_pokemon in resultado:
            self.assertLessEqual(levenshtein("charmande", self.nomes[id_pokemon]), 2)


if __name__ == "__main__":
    unittest.main()
