from jarowinkler import jarowinkler_similarity
from rapidfuzz.fuzz import ratio

# Strings de exemplo
string1 = "casa"
string2 = "casarão"

# Similaridade Jaro-Winkler
similaridade_jw = jarowinkler_similarity(string1, string2)
print(f"Similaridade Jaro-Winkler: {similaridade_jw:.2f}")

# Similaridade RapidFuzz (Ratio)
similaridade_rf = ratio(string1, string2) / 100  # RapidFuzz retorna valores entre 0 e 100
print(f"Similaridade RapidFuzz (Ratio): {similaridade_rf:.2f}")


###################################################################

import numpy as np
import pandas as pd
from jarowinkler import jarowinkler_similarity

def preprocess_phrase(phrase):
    """Divide a frase por vírgulas e normaliza os elementos."""
    return [element.strip().lower() for element in phrase.split(",")]

def is_valid_transposition(word1, word2):
    """Verifica se há transposição de apenas 1 letra entre duas palavras."""
    if len(word1) != len(word2):
        return False
    differences = sum(c1 != c2 for c1, c2 in zip(word1, word2))
    return differences == 2  # Considera apenas uma transposição de 1 letra

def has_space_between_words(word):
    """Verifica se há espaços entre as palavras."""
    return " " in word

def apply_rules(similarity, word1, word2, threshold=0.9):
    """Aplica as regras quando a similaridade está entre 0.8 e 0.9."""
    if similarity >= 0.8 and similarity < threshold:
        # Se há espaço entre as palavras
        if has_space_between_words(word1) or has_space_between_words(word2):
            word1_parts = word1.split() if has_space_between_words(word1) else [word1]
            word2_parts = word2.split() if has_space_between_words(word2) else [word2]
            # Comparar partes das palavras separadas por espaço
            for part1 in word1_parts:
                for part2 in word2_parts:
                    sub_similarity = jarowinkler_similarity(part1, part2)
                    if sub_similarity == 1.0:
                        return sub_similarity  # Considera igual se a similaridade for 1
            return similarity  # Caso contrário, mantém a similaridade original

        # Se não há espaço e há transposição de 1 letra
        if is_valid_transposition(word1, word2):
            return 1.0  # Considera como palavras iguais

    return similarity

def calculate_similarity_with_rules(phrase1, phrase2, threshold=0.9):
    """Calcula a similaridade entre duas frases aplicando regras de transposição e espaços."""
    # Pré-processamento
    elements1 = preprocess_phrase(phrase1)
    elements2 = preprocess_phrase(phrase2)

    # Construir matriz de similaridade inicial
    n, m = len(elements1), len(elements2)
    initial_similarity_matrix = np.zeros((n, m))
    secondary_similarity_matrix = np.zeros((n, m))
    
    for i in range(n):
        for j in range(m):
            # Calcular a similaridade inicial
            initial_similarity = jarowinkler_similarity(elements1[i], elements2[j])
            initial_similarity_matrix[i, j] = initial_similarity

            # Aplicar regras para matriz secundária
            secondary_similarity = apply_rules(initial_similarity, elements1[i], elements2[j], threshold)
            secondary_similarity_matrix[i, j] = secondary_similarity
    
    return initial_similarity_matrix, secondary_similarity_matrix, elements1, elements2

# Exemplo de frases
phrase1 = "Transtorno psicótico, dislexia, dislalia, autismo"
phrase2 = "dislexia, TDAH, autismo, dislexia moderada"

# Calcular as duas matrizes de similaridade
initial_matrix, secondary_matrix, elements1, elements2 = calculate_similarity_with_rules(phrase1, phrase2, threshold=0.9)

# Exibir resultados
print(f"Matriz Inicial de Similaridade:")
df_initial = pd.DataFrame(initial_matrix, index=elements1, columns=elements2)
print(df_initial)

print(f"\nMatriz Secundária de Similaridade (Com Regras Aplicadas):")
df_secondary = pd.DataFrame(secondary_matrix, index=elements1, columns=elements2)
print(df_secondary)
