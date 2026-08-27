import re

# 1. Mots-clés et patterns sensibles / malveillants
BLOCKED_PATTERNS = [
    # Mots de passe & Clés
    r"mot\s*de\s*passe",
    r"password",
    r"clé\s*privée",
    r"private\s*key",
    r"token",
    r"api[_\s]*key",
    # Injection de Prompt / Jailbreak
    r"ignore\s*(all)?\s*previous\s*instructions",
    r"oublie\s*(toutes)?\s*tes\s*instructions",
    r"tu\s*es\s*maintenant",
    r"system\s*prompt",
    r"system\s*role",
    r"prompt\s*injection",
    # Mots vulgaires ou d'insultes fréquents
    r"con",
    r"merde",
    r"putain",
    r"fuck",
]

# Compilateur regex pour de meilleures performances
COMPILED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE) for pattern in BLOCKED_PATTERNS
]


import re


def is_meaningful_text(text: str) -> bool:
    """Détecte les saisies aléatoires au clavier."""
    text_clean = text.strip().lower()

    # 1. Longueur minimale
    if len(text_clean) < 2:
        return False

    # 2. Ignorer les mots très courts valides
    if text_clean in {"bac", "ia", "tic", "svt", "bti", "dut", "bts"}:
        return True

    # 3. Détection de répétition de caractères (ex: "wwazxwww")
    if re.search(r"(.)\1{2,}", text_clean):
        return False

    # 4. Suite de consonnes d'affilée (ex: "qfqdqf")
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{4,}", text_clean):
        return False

    # 5. Calcul de la proportion de voyelles
    words = text_clean.split()
    for word in words:
        if len(word) > 4:
            vowels = len(re.findall(r"[aeiouyàâéèêëîïôùûü]", word))
            ratio = vowels / len(word)
            # Si le mot a moins de 20% de voyelles, c'est du bruit (ex: "qfqdqfazs")
            if ratio < 0.20:
                return False

    return True

def is_safe_question(question: str) -> bool:
    """Vérifie la sécurité et la validité de la question saisie."""
    if not question or not isinstance(question, str):
        return False

    # 1. Vérification du bruit / texte incohérent
    if not is_meaningful_text(question):
        return False

    # 2. Vérification des motifs bloqués (Sécurité / Injection / Insultes)
    for pattern in COMPILED_PATTERNS:
        if pattern.search(question):
            return False

    return True