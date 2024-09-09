# Algoritmo de Johnson com Visualização Dinâmica

Este repositório contém uma implementação do Algoritmo de Johnson para encontrar o caminho mais curto entre todos os pares de vértices em um grafo, com suporte para pesos de arestas negativos. A implementação inclui uma visualização dinâmica usando `matplotlib` e `networkx` para ilustrar o progresso do algoritmo.

## Funcionalidades

- **Adiciona um vértice fictício** ao grafo para permitir a execução do algoritmo de Bellman-Ford.
- **Repondera os pesos das arestas** para garantir que todos os pesos sejam não-negativos.
- **Executa o Algoritmo de Dijkstra** para encontrar os caminhos mais curtos entre todos os pares de vértices.
- **Visualiza dinamicamente** o grafo e destaca as arestas durante a execução do algoritmo.
- **Mostra uma tabela** com as distâncias mais curtas e os caminhos entre todos os pares de vértices.

## Dependências

Certifique-se de ter as seguintes bibliotecas instaladas:

- `networkx`
- `matplotlib`

Você pode instalar as dependências usando `pip`:

```bash
pip install networkx matplotlib
