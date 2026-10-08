#ifndef SKIPLIST_H
#define SKIPLIST_H

/* Skip List ordenada por chave (string) com valor inteiro (id do Pokémon). */
typedef struct SkipList SkipList;

SkipList *sl_criar(void);
void sl_destruir(SkipList *sl);

/* Retorna 1 se inseriu, 0 se a chave já existia (o valor é atualizado), -1 em erro. */
int sl_inserir(SkipList *sl, const char *chave, int valor);

/* Retorna 1 e grava o valor em *valor se achou, 0 caso contrário. */
int sl_buscar(const SkipList *sl, const char *chave, int *valor);

/* Grava em saida os valores das chaves que começam com prefixo, em ordem alfabética,
 * até no máximo max resultados. Retorna quantos foram gravados. */
int sl_prefixo(const SkipList *sl, const char *prefixo, int *saida, int max);

int sl_tamanho(const SkipList *sl);

#endif
