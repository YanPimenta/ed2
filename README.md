# trabalho-ed2

Pokédex com estruturas de dados implementadas em C (Skip List, Splay Tree, BST, Heap), expostas por uma API FastAPI via `ctypes` e consumidas por um frontend React.

## Estrutura

```
backend/
  app/    FastAPI e carregamento do CSV (Python)
  c/      estruturas de dados em C, compiladas para libed2.so
frontend/ React + Vite
data/     pokemon.csv
Makefile
```

## Requisitos

- Python 3.12+
- gcc e make
- Node.js 18+ e npm

## Como rodar

```
make dev
```

Instala as dependências (venv Python e `npm install`), compila a lib C e sobe os dois servidores:

- Backend: http://localhost:8000 (teste em `/health`)
- Frontend: http://localhost:5173

## Outros comandos

| Comando        | O que faz                          |
| -------------- | ---------------------------------- |
| `make install` | instala dependências do back/front |
| `make lib`     | compila `backend/c/libed2.so`      |
| `make back`    | sobe só o backend                  |
| `make front`   | sobe só o frontend                 |
| `make test`    | roda os testes do backend          |
| `make clean`   | remove a lib compilada             |

## Contrato da API

Base: `http://localhost:8000`. Todas as respostas são JSON e os nomes de campo seguem o `loader.py`.

### Objeto `Pokemon`

```json
{
  "id": 1,
  "nome": "Abomasnow",
  "elementos": ["Grass", "Ice"],
  "altura": 2.2,
  "peso": 135.5,
  "habilidades": [
    { "nome": "Snow Warning", "oculta": false },
    { "nome": "Soundproof", "oculta": true }
  ],
  "egg_grupo": ["Grass", "Monster"],
  "tem_ovo": true,
  "captura": 60,
  "status": { "hp": 90, "atq": 92, "def": 75, "spa": 92, "spd": 85, "spe": 60 }
}
```

### `source`

Indica qual estrutura respondeu:

| Valor      | Significado                          |
| ---------- | ------------------------------------ |
| `cache`    | acerto na Splay Tree                 |
| `skiplist` | busca exata ou por prefixo na Skip List |
| `fuzzy`    | candidato por distância de Levenshtein |

### `GET /search?q=<texto>&limite=10`

Busca por nome: exata, depois prefixo, depois fuzzy.

```json
{
  "source": "skiplist",
  "sugestao": null,
  "resultados": [ { "...Pokemon": "..." } ]
}
```

- `sugestao`: nome corrigido ("Você quis dizer...?"), preenchido só quando `source` é `fuzzy`; nos demais casos é `null`.
- Sem resultados: `resultados: []`.
- `q` ausente ou vazio: `400`.

### `GET /pokemon/{id}`

```json
{ "source": "cache", "pokemon": { "...Pokemon": "..." } }
```

`404` com `{ "erro": "Pokémon não encontrado" }` se o id não existir.

### `GET /filter`

Todos os parâmetros são opcionais e combinados com AND.

| Parâmetro               | Exemplo            | Descrição                               |
| ----------------------- | ------------------ | --------------------------------------- |
| `tipo`                  | `Fire`             | elemento (repetível: `tipo=Fire&tipo=Flying`) |
| `egg_grupo`             | `Monster`          | grupo de ovo                            |
| `tem_ovo`               | `true`             | se o Pokémon pode botar ovo             |
| `<stat>_min`/`<stat>_max` | `atq_min=100`    | intervalo; `<stat>` ∈ `hp`, `atq`, `def`, `spa`, `spd`, `spe` |
| `ordenar`               | `atq`              | campo de `status` para ordenar          |
| `ordem`                 | `desc`             | `asc` ou `desc` (padrão `desc`)         |
| `limite`                | `10`               | máximo de resultados (padrão 20)        |

```json
{ "total": 42, "resultados": [ { "...Pokemon": "..." } ] }
```

`total` é a quantidade antes de aplicar `limite`. Parâmetro inválido: `400`.

### `GET /cache/top?limite=5`

Pokémon mais acessados, exibidos ao focar a barra de busca.

```json
{ "resultados": [ { "pokemon": { "...Pokemon": "..." }, "acessos": 7 } ] }
```

Cache vazio: `resultados: []`.

### Erros

Formato único: `{ "erro": "mensagem" }`.
