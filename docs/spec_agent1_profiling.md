# Spécification — Agent 1 : Profilage & Diagnostic Qualité

> Contrat d'interface entre l'**Agent 1 (Profiling)** et l'**Agent 2 (Data Quality & Cleaning)**.
> Version : 0.1 — à valider par les deux responsables d'agents.

---

## 1. Rôle de l'agent

|                  |                                                                                                                                              |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objectif**     | Identifier la structure, les caractéristiques et les problèmes de qualité des datasets CSV du projet.                                        |
| **Entrée**       | Dossier de fichiers CSV (ex. `Datasets/Import&Export/data`).                                                                                 |
| **Sortie**       | Section `profiling` du state LangGraph, structurée et lisible par machine.                                                                   |
| **Principe clé** | L'agent **observe et diagnostique**, il **ne modifie jamais** les données. Il peut **suggérer** un traitement, l'Agent 2 décide et applique. |

---

## 2. Place dans le state LangGraph

Le state global contient une section par agent. L'Agent 1 **écrit uniquement** dans `profiling` et **lit** les entrées communes.

| Clé du state                     | Écrit par                   | Lu par                      | Contenu                                                |
| -------------------------------- | --------------------------- | --------------------------- | ------------------------------------------------------ |
| `input`                          | Orchestrateur / utilisateur | Agent 1                     | Chemin du dossier, liste des fichiers, contexte métier |
| `profiling`                      | **Agent 1**                 | Agent 2 (+ agents suivants) | Rapport de profilage complet (ce document)             |
| `cleaning`                       | Agent 2                     | Agents suivants             | Datasets nettoyés, journal des corrections             |
| `kpi`, `modeling`, `dashboard` … | Agents suivants             | …                           | …                                                      |
| `errors`                         | Tous                        | Orchestrateur               | Erreurs d'exécution                                    |

**Règle** : pas de DataFrame dans le state — uniquement des chemins de fichiers et des résultats d'analyse (sérialisables JSON).

---

## 3. Structure de la section `profiling`

```
profiling
├── metadata        → informations sur l'exécution et les fichiers
├── tables          → profil détaillé de chaque table et de chaque colonne
├── relationships   → relations détectées entre tables
├── issues          → liste de tous les problèmes de qualité détectés
├── summary         → synthèse globale (scores, compteurs)
└── artifacts       → chemins des rapports exportés (JSON pour l'Agent 2, Markdown pour lecture)
```

Le rapport complet est aussi exporté dans `outputs/profiling/profiling_report.json`.

---

## 4. `metadata`

| Champ          | Type                | Description                              | Exemple                       |
| -------------- | ------------------- | ---------------------------------------- | ----------------------------- |
| `run_id`       | texte               | Identifiant unique de l'exécution        | `Individus_2026-09-28_001`    |
| `generated_at` | date-heure ISO 8601 | Date de génération                       | `2026-09-28T10:15:00`         |
| `source_dir`   | texte               | Dossier analysé                          | `Datasets/Import&Export/data` |
| `spec_version` | texte               | Version de ce contrat                    | `0.1`                         |
| `llm`          | objet               | LLM utilisé : `enabled`, `model`, `status` | `{"enabled": true, "model": "openai/gpt-oss-120b", …}` |
| `files`        | liste               | Un élément par fichier (voir ci-dessous) |                               |

Pour chaque fichier dans `files` :

| Champ         | Type                       | Description                    | Exemple         |
| ------------- | -------------------------- | ------------------------------ | --------------- |
| `file_name`   | texte                      | Nom du fichier                 | `customers.csv` |
| `table_name`  | texte                      | Nom logique de la table        | `customers`     |
| `path`        | texte                      | Chemin complet                 |                 |
| `size_bytes`  | entier                     | Taille                         | `6758`          |
| `encoding`    | texte                      | Encodage détecté               | `ISO-8859-1`    |
| `delimiter`   | texte                      | Séparateur détecté             | `,`             |
| `has_header`  | booléen                    | Présence d'une ligne d'en-tête | `true`          |
| `read_status` | `ok` / `warning` / `error` | Résultat de la lecture         | `warning`       |

---

## 5. `tables`

### 5.1 Niveau table

| Champ                    | Type                             | Description                            | Exemple         |
| ------------------------ | -------------------------------- | -------------------------------------- | --------------- |
| `table_name`             | texte                            | Nom logique                            | `orders`        |
| `row_count`              | entier                           | Nombre de lignes (hors en-tête)        | `830`           |
| `column_count`           | entier                           | Nombre de colonnes                     | `8`             |
| `primary_key_candidates` | liste de listes                  | Colonne(s) unique(s) et non nulles     | `[["orderID"]]` |
| `duplicate_row_count`    | entier                           | Lignes entièrement dupliquées          | `0`             |
| `columns`                | liste                            | Profil de chaque colonne (5.2)         |                 |

### 5.2 Niveau colonne

**Champs communs (toutes colonnes)**

| Champ            | Type                                                                             | Description                                | Exemple             |
| ---------------- | -------------------------------------------------------------------------------- | ------------------------------------------ | ------------------- |
| `column_name`    | texte                                                                            | Nom tel que dans le fichier                | `shippedDate`       |
| `position`       | entier                                                                           | Position (0 = première)                    | `5`                 |
| `detected_type`  | `integer` / `float` / `string` / `date` / `datetime` / `boolean` / `mixed`       | Type réel observé                          | `date`              |
| `expected_type`  | idem                                                                             | Type attendu (déduit du nom / contenu)     | `date`              |
| `semantic_role`  | `identifier` / `foreign_key` / `measure` / `date` / `category` / `text` / `flag` | Rôle métier probable                       | `date`              |
| `null_count`     | entier                                                                           | Valeurs manquantes (vides, NA, null…)      | `21`                |
| `null_pct`       | décimal 0–100                                                                    | % de manquants                             | `2.53`              |
| `distinct_count` | entier                                                                           | Nombre de valeurs distinctes               | `387`               |
| `unique_pct`     | décimal 0–100                                                                    | Distinct / total                           | `46.6`              |
| `is_unique`      | booléen                                                                          | Toutes les valeurs non nulles sont uniques | `false`             |
| `sample_values`  | liste (≤ 5)                                                                      | Exemples de valeurs                        | `["2013-07-16", …]` |
| `top_values`     | liste de `{value, count}` (≤ 5)                                                  | Valeurs les plus fréquentes                |                     |

**Champs spécifiques — numériques** (`integer`, `float`)

`min`, `max`, `mean`, `median`, `std`, `q1`, `q3`, `zero_count`, `negative_count`, `outlier_count` (méthode IQR, à préciser dans `outlier_method`).

**Champs spécifiques — dates**

`min_date`, `max_date`, `detected_formats` (liste, ex. `["YYYY-MM-DD"]`), `invalid_date_count`, `future_date_count`.

**Champs spécifiques — texte / catégorie**

`min_length`, `max_length`, `leading_trailing_spaces_count`, `case_variants_count` (ex. `France` / `FRANCE`), `invalid_char_count` (caractères d'encodage cassés, ex. `�`).

---

## 6. `relationships`

Relations clé étrangère → clé primaire détectées (par nom de colonne identique et/ou recouvrement de valeurs).

| Champ                        | Type                                          | Description                         | Exemple                |
| ---------------------------- | --------------------------------------------- | ----------------------------------- | ---------------------- |
| `relationship_id`            | texte                                         | Identifiant                         | `REL-001`              |
| `from_table` / `from_column` | texte                                         | Côté clé étrangère                  | `orders.customerID`    |
| `to_table` / `to_column`     | texte                                         | Côté clé primaire                   | `customers.customerID` |
| `cardinality`                | `many_to_one` / `one_to_one` / `many_to_many` | Cardinalité                         | `many_to_one`          |
| `match_pct`                  | décimal 0–100                                 | % de valeurs FK trouvées dans la PK | `100.0`                |
| `orphan_count`               | entier                                        | Valeurs FK sans correspondance      | `0`                    |
| `orphan_samples`             | liste (≤ 5)                                   | Exemples de valeurs orphelines      |                        |
| `detection_method`           | `name_match` / `value_overlap` / `both`       | Comment la relation a été trouvée   | `both`                 |
| `confidence`                 | décimal 0–1                                   | Confiance de la détection           | `0.95`                 |

Relations attendues sur le jeu actuel (pour validation) :

- `orders.customerID → customers.customerID`
- `orders.employeeID → employees.employeeID`
- `orders.shipperID → shippers.shipperID`
- `order_details.orderID → orders.orderID`
- `order_details.productID → products.productID`
- `products.categoryID → categories.categoryID`
- `employees.reportsTo → employees.employeeID` (auto-référence / hiérarchie)

---

## 7. `issues` — cœur du contrat

Chaque problème détecté est **un élément indépendant** de la liste. C'est ce que l'Agent 2 parcourt pour décider des traitements.

### 7.1 Champs d'un issue

| Champ                      | Type                                            | Obligatoire | Description                                                                                      |
| -------------------------- | ----------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `issue_id`                 | texte                                           | ✅          | Identifiant unique et stable (`ISS-001`, …)                                                      |
| `table`                    | texte                                           | ✅          | Table concernée                                                                                  |
| `column`                   | texte ou `null`                                 | ✅          | Colonne concernée (`null` si problème au niveau table)                                           |
| `issue_type`               | énuméré (7.2)                                   | ✅          | Catégorie du problème                                                                            |
| `severity`                 | `critical` / `high` / `medium` / `low` / `info` | ✅          | Gravité (7.3)                                                                                    |
| `description`              | texte                                           | ✅          | Explication lisible par un humain                                                                |
| `affected_rows`            | entier                                          | ✅          | Nombre de lignes touchées                                                                        |
| `affected_pct`             | décimal 0–100                                   | ✅          | % de lignes touchées                                                                             |
| `examples`                 | liste (≤ 5)                                     | ✅          | Exemples concrets (valeur + identifiant de ligne si possible)                                    |
| `rule`                     | texte                                           | ✅          | Règle/critère ayant déclenché la détection                                                       |
| `is_expected`              | booléen                                         | ⬜          | `true` si le problème est probablement légitime (ex. `shippedDate` vide = commande non expédiée) |
| `suggested_action`         | énuméré (7.4)                                   | ⬜          | Traitement suggéré (non appliqué)                                                                |
| `suggested_action_details` | texte                                           | ⬜          | Précisions (ex. « relire en ISO-8859-1 »)                                                        |
| `related_issues`           | liste d'`issue_id`                              | ⬜          | Liens entre problèmes (ex. encodage → caractères invalides)                                      |
| `detected_by`              | `rule` / `llm`                                  | ⬜          | Détection déterministe ou par LLM                                                                |
| `confidence`               | décimal 0–1                                     | ⬜          | Confiance (surtout pour `detected_by = llm`)                                                     |

### 7.2 Types de problèmes (`issue_type`)

| Valeur                 | Niveau          | Signification                                            |
| ---------------------- | --------------- | -------------------------------------------------------- |
| `encoding_error`       | fichier/colonne | Encodage non UTF-8 ou caractères cassés (`�`)            |
| `missing_values`       | colonne         | Valeurs vides / nulles                                   |
| `duplicate_rows`       | table           | Lignes entièrement identiques                            |
| `duplicate_keys`       | colonne         | Doublons sur une clé primaire candidate                  |
| `type_mismatch`        | colonne         | Type détecté ≠ type attendu (ex. nombre stocké en texte) |
| `mixed_types`          | colonne         | Plusieurs types dans une même colonne                    |
| `inconsistent_format`  | colonne         | Formats hétérogènes (dates, téléphones, devises…)        |
| `invalid_date`         | colonne         | Date non parsable ou incohérente                         |
| `date_logic_violation` | table           | Incohérence entre dates (ex. `shippedDate < orderDate`)  |
| `out_of_range`         | colonne         | Valeur hors domaine (prix négatif, remise > 1…)          |
| `outlier`              | colonne         | Valeur statistiquement aberrante                         |
| `whitespace`           | colonne         | Espaces en début/fin                                     |
| `case_inconsistency`   | colonne         | Variantes de casse d'une même valeur                     |
| `typo_suspected`       | colonne         | Faute de saisie probable (ex. `Blondesddsl`)             |
| `orphan_foreign_key`   | relation        | Clé étrangère sans correspondance                        |
| `constant_column`      | colonne         | Une seule valeur distincte (peu utile)                   |
| `high_cardinality`     | colonne         | Catégorie avec trop de valeurs distinctes                |
| `other`                | —               | Autre (à décrire dans `description`)                     |

> Toute nouvelle valeur doit être ajoutée à cette liste **d'un commun accord** avec l'Agent 2.

### 7.3 Grille de sévérité

| Sévérité   | Critère                                   | Exemple                                                                 |
| ---------- | ----------------------------------------- | ----------------------------------------------------------------------- |
| `critical` | Empêche le chargement ou fausse le modèle | Clé primaire dupliquée, fichier illisible                               |
| `high`     | Fausse directement des KPI                | Clés étrangères orphelines, montants négatifs, types de mesure en texte |
| `medium`   | Dégrade l'analyse ou l'affichage          | Encodage cassé sur des noms, formats de date mixtes                     |
| `low`      | Cosmétique                                | Espaces superflus, casse incohérente                                    |
| `info`     | Observation, pas forcément un problème    | Manquants légitimes (`reportsTo` du directeur)                          |

### 7.4 Actions suggérées (`suggested_action`)

`reencode`, `drop_rows`, `drop_duplicates`, `impute_mean`, `impute_median`, `impute_mode`, `impute_constant`, `keep_as_null`, `cast_type`, `standardize_format`, `trim_whitespace`, `normalize_case`, `correct_value`, `cap_outliers`, `flag_only`, `investigate`, `no_action`.

### 7.5 Exemple d'issue (tiré du jeu actuel)

```json
{
  "issue_id": "ISS-001",
  "table": "customers",
  "column": null,
  "issue_type": "encoding_error",
  "severity": "medium",
  "description": "Le fichier est encodé en ISO-8859-1 : lu en UTF-8, les caractères accentués sont remplacés par '�'.",
  "affected_rows": 0,
  "affected_pct": 0,
  "examples": ["Antonio Moreno Taquer�a", "Berglunds snabbk�p", "Lule�"],
  "rule": "Encodage détecté différent de UTF-8",
  "is_expected": false,
  "suggested_action": "reencode",
  "suggested_action_details": "Relire le fichier en ISO-8859-1 puis sauvegarder en UTF-8.",
  "related_issues": [],
  "detected_by": "rule",
  "confidence": 1.0
}
```

_(`affected_rows` est à calculer lors du profilage réel.)_

---

## 8. `summary`

| Champ                    | Type          | Description                                                                           |
| ------------------------ | ------------- | ------------------------------------------------------------------------------------- |
| `tables_count`           | entier        | Nombre de tables analysées                                                            |
| `total_rows`             | entier        | Total des lignes                                                                      |
| `issues_count`           | entier        | Nombre total d'issues                                                                 |
| `issues_by_severity`     | objet         | Ex. `{critical: 0, high: 2, medium: 3, low: 5, info: 2}`                              |
| `issues_by_type`         | objet         | Compteur par `issue_type`                                                             |
| `quality_score_by_table` | objet         | Score 0–100 par table (formule à définir, ex. 100 − pénalités pondérées par sévérité) |
| `global_quality_score`   | décimal 0–100 | Score global                                                                          |
| `ready_for_cleaning`     | booléen       | `true` si le profilage s'est terminé sans erreur bloquante                            |
| `narrative`              | texte         | Résumé en langage naturel (peut être rédigé par un LLM)                               |

---

## 9. Problèmes déjà repérés sur le jeu `Import&Export` (à confirmer par l'agent)

| Table       | Colonne       | Type                                                  | Sévérité pressentie |
| ----------- | ------------- | ----------------------------------------------------- | ------------------- |
| `customers` | (fichier)     | `encoding_error` (ISO-8859-1)                         | medium              |
| `products`  | (fichier)     | `encoding_error` (ISO-8859-1)                         | medium              |
| `customers` | `companyName` | `typo_suspected` (`Blondesddsl père et fils`)         | low                 |
| `orders`    | `shippedDate` | `missing_values` (~21 lignes, probablement légitimes) | info                |
| `employees` | `reportsTo`   | `missing_values` (1 ligne = directeur, légitime)      | info                |

---

## 10. Règles de fonctionnement

1. **Lecture seule** : aucun fichier source n'est modifié.
2. **Déterminisme** : les statistiques et détections par règles doivent donner le même résultat à chaque exécution. Le LLM n'intervient que pour l'interprétation (rôle sémantique, fautes probables, résumé), et ses issues sont marquées `detected_by = llm` avec une `confidence`.
3. **Sérialisable** : toute la section `profiling` doit pouvoir être exportée en JSON (aussi sauvegardée dans un fichier `profiling_report.json` pour traçabilité).
4. **Pas de DataFrame dans le state.**
5. **Erreurs** : si un fichier est illisible, il est marqué `read_status = error` dans `metadata`, une issue `critical` est créée, et l'agent continue avec les autres fichiers.
6. **Versionnement** : tout changement de ce contrat incrémente `spec_version` et est validé par les deux parties.

---

## 11. Points à valider avec l'Agent 2

- [ ] La liste des `issue_type` est-elle suffisante ?
- [ ] La grille de sévérité convient-elle pour prioriser les traitements ?
- [ ] L'Agent 2 veut-il les `suggested_action` ou préfère-t-il décider seul ?
- [ ] Faut-il des identifiants de ligne précis (numéros de ligne / clés) pour toutes les lignes affectées, ou seulement des exemples ?
- [ ] Formule du score de qualité.
- [ ] Format de l'export fichier (JSON unique ou un fichier par table).
