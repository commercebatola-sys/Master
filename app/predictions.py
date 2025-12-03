# predictions.py

import pandas as pd

# ===============================
# 1 — Calcul des indicateurs financiers
# ===============================
def calculate_growth(current_value: float, previous_value: float) -> float:
    """
    Calcule le taux de croissance (%) entre deux périodes.
    """
    if previous_value == 0:
        return 0.0
    return ((current_value - previous_value) / previous_value) * 100


def calculate_margin(profit: float, revenue: float) -> float:
    """
    Calcule la marge nette (%) d'une entreprise.
    """
    if revenue == 0:
        return 0.0
    return (profit / revenue) * 100


def calculate_ratio(numerator: float, denominator: float) -> float:
    """
    Calcule un ratio simple.
    """
    if denominator == 0:
        return 0.0
    return numerator / denominator


# ===============================
# 2 — Prévision simple (baseline)
# ===============================
def forecast_next_period(current_value: float, growth_rate: float) -> float:
    """
    Prévoit la valeur de la prochaine période à partir de la valeur actuelle et d'un taux de croissance (%).
    """
    return current_value * (1 + growth_rate / 100)


# ===============================
# 3 — Analyse de séries temporelles
# ===============================
def calculate_cagr(start_value: float, end_value: float, periods: int) -> float:
    """
    Calcule le CAGR (Taux de croissance annuel composé).
    """
    if start_value <= 0 or periods <= 0:
        return 0.0
    return ((end_value / start_value) ** (1 / periods) - 1) * 100


def moving_average(data: list, window: int = 3) -> list:
    """
    Calcule la moyenne mobile sur une liste de données.
    """
    if not data or window <= 0:
        return []
    series = pd.Series(data)
    return series.rolling(window=window).mean().tolist()


# ===============================
# 4 — Génération de résumé chiffré
# ===============================
def generate_financial_summary(metrics: dict) -> str:
    """
    Génère un résumé chiffré à partir d'un dictionnaire d'indicateurs financiers.
    Exemple de metrics : {"Revenue": 1_000_000, "Profit": 200_000, "Debt": 300_000}
    """
    lines = ["### Résumé chiffré des indicateurs financiers :\n"]
    for key, value in metrics.items():
        lines.append(f"- **{key}** : {value:,}")
    return "\n".join(lines)
