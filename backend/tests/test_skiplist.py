import unittest
from pathlib import Path

from app.loader import carregar_csv
from app.skiplist import SkipList

CSV = Path(__file__).resolve().parents[2] / "data" / "pokemon.csv"


class TestSkipList(unittest.TestCase):
    def test_vazia(self):
        sl = SkipList()
        self.assertEqual(len(sl), 0)
        self.assertIsNone(sl.buscar("pikachu"))

    def test_inserir_e_buscar(self):
        sl = SkipList()
        self.assertTrue(sl.inserir("pikachu", 25))
        self.assertEqual(sl.buscar("pikachu"), 25)
        self.assertIsNone(sl.buscar("pikachuu"))
        self.assertIsNone(sl.buscar("pika"))

    def test_chave_repetida_atualiza_valor(self):
        sl = SkipList()
        self.assertTrue(sl.inserir("mew", 1))
        self.assertFalse(sl.inserir("mew", 2))
        self.assertEqual(len(sl), 1)
        self.assertEqual(sl.buscar("mew"), 2)

    def test_todos_os_nomes_do_csv(self):
        pokemons = carregar_csv(str(CSV))
        sl = SkipList()
        for p in pokemons:
            self.assertTrue(sl.inserir(p["nome_regex"], p["id"]))
        self.assertEqual(len(sl), len(pokemons))
        for p in pokemons:
            self.assertEqual(sl.buscar(p["nome_regex"]), p["id"])

    def test_prefixo(self):
        sl = SkipList()
        for chave, valor in [("pichu", 1), ("pikachu", 2), ("pidgey", 3), ("raichu", 4)]:
            sl.inserir(chave, valor)
        self.assertEqual(sl.prefixo("pi"), [1, 3, 2])  # ordem alfabética
        self.assertEqual(sl.prefixo("pika"), [2])
        self.assertEqual(sl.prefixo("pi", limite=2), [1, 3])
        self.assertEqual(sl.prefixo("x"), [])
        self.assertEqual(sl.prefixo("pikachuu"), [])
        self.assertEqual(sl.prefixo("pi", limite=0), [])

    def test_prefixo_pika_no_csv(self):
        pokemons = carregar_csv(str(CSV))
        sl = SkipList()
        for p in pokemons:
            sl.inserir(p["nome_regex"], p["id"])
        nomes = {p["id"]: p["nome"] for p in pokemons}
        self.assertIn("Pikachu", [nomes[i] for i in sl.prefixo("pika")])
        # todo resultado começa com o prefixo e nenhum candidato foi perdido
        esperado = sorted(p["nome_regex"] for p in pokemons if p["nome_regex"].startswith("char"))
        obtido = [next(p["nome_regex"] for p in pokemons if p["id"] == i) for i in sl.prefixo("char", 100)]
        self.assertEqual(obtido, esperado)


if __name__ == "__main__":
    unittest.main()
