#include <stdlib.h>
#include <string.h>

#include "skiplist.h"

#define NIVEL_MAX 16

typedef struct No {
    char *chave;
    int valor;
    struct No *prox[];
} No;

struct SkipList {
    No *cabeca;
    int nivel;
    int tamanho;
    unsigned int semente;
};

static No *criar_no(int nivel, const char *chave, int valor) {
    No *no = calloc(1, sizeof(No) + nivel * sizeof(No *));
    if (!no) return NULL;
    if (chave) {
        no->chave = strdup(chave);
        if (!no->chave) {
            free(no);
            return NULL;
        }
    }
    no->valor = valor;
    return no;
}

/* xorshift: gerador simples e determinístico, suficiente para sortear níveis */
static unsigned int proximo_aleatorio(SkipList *sl) {
    unsigned int x = sl->semente;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    sl->semente = x;
    return x;
}

/* cada nível extra tem probabilidade 1/2 */
static int nivel_aleatorio(SkipList *sl) {
    int nivel = 1;
    while (nivel < NIVEL_MAX && (proximo_aleatorio(sl) & 1)) nivel++;
    return nivel;
}

SkipList *sl_criar(void) {
    SkipList *sl = malloc(sizeof(SkipList));
    if (!sl) return NULL;
    sl->cabeca = criar_no(NIVEL_MAX, NULL, 0);
    if (!sl->cabeca) {
        free(sl);
        return NULL;
    }
    sl->nivel = 1;
    sl->tamanho = 0;
    sl->semente = 2463534242u;
    return sl;
}

void sl_destruir(SkipList *sl) {
    if (!sl) return;
    No *no = sl->cabeca;
    while (no) {
        No *prox = no->prox[0];
        free(no->chave);
        free(no);
        no = prox;
    }
    free(sl);
}

int sl_inserir(SkipList *sl, const char *chave, int valor) {
    No *anterior[NIVEL_MAX];
    No *atual = sl->cabeca;

    for (int i = sl->nivel - 1; i >= 0; i--) {
        while (atual->prox[i] && strcmp(atual->prox[i]->chave, chave) < 0)
            atual = atual->prox[i];
        anterior[i] = atual;
    }

    No *candidato = atual->prox[0];
    if (candidato && strcmp(candidato->chave, chave) == 0) {
        candidato->valor = valor;
        return 0;
    }

    int nivel = nivel_aleatorio(sl);
    for (int i = sl->nivel; i < nivel; i++) anterior[i] = sl->cabeca;
    if (nivel > sl->nivel) sl->nivel = nivel;

    No *novo = criar_no(nivel, chave, valor);
    if (!novo) return -1;
    for (int i = 0; i < nivel; i++) {
        novo->prox[i] = anterior[i]->prox[i];
        anterior[i]->prox[i] = novo;
    }
    sl->tamanho++;
    return 1;
}

int sl_buscar(const SkipList *sl, const char *chave, int *valor) {
    const No *atual = sl->cabeca;

    for (int i = sl->nivel - 1; i >= 0; i--) {
        while (atual->prox[i] && strcmp(atual->prox[i]->chave, chave) < 0)
            atual = atual->prox[i];
    }

    const No *candidato = atual->prox[0];
    if (candidato && strcmp(candidato->chave, chave) == 0) {
        *valor = candidato->valor;
        return 1;
    }
    return 0;
}

int sl_prefixo(const SkipList *sl, const char *prefixo, int *saida, int max) {
    const No *atual = sl->cabeca;
    size_t tam = strlen(prefixo);

    /* posiciona no último nó com chave < prefixo; o próximo é o primeiro >= prefixo */
    for (int i = sl->nivel - 1; i >= 0; i--) {
        while (atual->prox[i] && strcmp(atual->prox[i]->chave, prefixo) < 0)
            atual = atual->prox[i];
    }

    int total = 0;
    for (const No *no = atual->prox[0]; no && total < max; no = no->prox[0]) {
        if (strncmp(no->chave, prefixo, tam) != 0) break;
        saida[total++] = no->valor;
    }
    return total;
}

int sl_tamanho(const SkipList *sl) {
    return sl->tamanho;
}
