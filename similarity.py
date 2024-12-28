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
