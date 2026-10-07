# Trace de nettoyage clean_20260930T213550207058Z

Statut : **WARN** · 23 correction(s) appliquée(s) · 0 refusée(s) par le LLM · 2 point(s) à valider

Planificateur : llm · modèle `openai/gpt-oss-120b`

## Fichiers lus

- `categories.csv` (utf-8-sig, séparateur ',') : tables ['categories'] · sha256 247a58c07dab…
- `customers.csv` (cp1252, séparateur ',') : tables ['customers'] · sha256 1108622425a4…
- `employees.csv` (utf-8-sig, séparateur ',') : tables ['employees'] · sha256 5ff38be204c8…
- `order_details.csv` (utf-8-sig, séparateur ',') : tables ['order_details'] · sha256 c3ff191cf94a…
- `orders.csv` (utf-8-sig, séparateur ',') : tables ['orders'] · sha256 9f6138249c69…
- `products.csv` (cp1252, séparateur ',') : tables ['products'] · sha256 004a8ac1cecb…
- `shippers.csv` (utf-8-sig, séparateur ',') : tables ['shippers'] · sha256 5776d6984154…

## Table `categories`

8 -> 8 lignes, 3 -> 3 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table categories contient 8 lignes, chaque ligne représente une catégorie unique (grain catégorie). La clé probable est categoryID, qui est actuellement en texte mais ne comporte aucun zéro initial. Aucun null, aucune valeur dupliquée apparente, description et nom sont déjà remplis. Risque faible de perte d'information métier en convertissant l'ID en nombre.

- Recommandation : Appliquer trim_whitespace sur toutes les colonnes textuelles
- Recommandation : Vérifier l'encodage des accents avec fix_encoding
- Recommandation : Utiliser flag_duplicate_keys pour confirmer l'unicité de categoryID
- Recommandation : Supprimer les colonnes vides éventuelles avec drop_empty_columns

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 1 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Pas de zéros initiaux ni de format spécial ; convertir categoryID en numérique simplifie les jointures sans perdre d'information. | 0 |

## Table `customers`

91 -> 91 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table customers, grain au niveau client avec customerID comme clé primaire, 91 enregistrements uniques, aucune valeur manquante, peu de colonnes textuelles, qualité globalement bonne mais quelques espaces superflus possibles.

- Recommandation : Vérifier l'unicité des clés avec flag_duplicate_keys
- Recommandation : Standardiser les noms de pays via normalize_country
- Recommandation : Unifier les variantes d'écriture de city si besoin avec merge_category_variants
- Recommandation : Supprimer d'éventuels doublons exacts avec drop_duplicates

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 2 | Supprimer les espaces superflus | companyName | applied | 1 valeur(s) avec espaces superflus | LLM : Supprimer les espaces superflus ne modifie pas le sens du nom d'entreprise et corrige le seul cas détecté. | 1 |

## Table `employees`

9 -> 9 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table employees, grain au niveau de chaque salarié, clé probable employeeID, colonne reportsTo comme clé étrangère vers le manager, 9 lignes, aucune valeur manquante sauf 1 dans reportsTo, pas d'espaces superflus apparents, risque de perte d'information faible.

- Recommandation : Appliquer trim_whitespace sur toutes les colonnes textuelles
- Recommandation : Standardiser les valeurs de country avec normalize_country
- Recommandation : Vérifier l'unicité de employeeID avec flag_duplicate_keys
- Recommandation : Envisager imputation ou validation manuelle du champ reportsTo manquant

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 3 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Les IDs sont déjà numériques sans zéros initiaux, la conversion ne perd aucune information métier. | 0 |
| 4 | Convertir en nombre | reportsTo | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : reportsTo contient uniquement des nombres ou null, la conversion aligne le type avec employeeID. | 0 |
| 5 | Signaler les valeurs manquantes | reportsTo | flagged | 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine | LLM : Le flag ne modifie pas les données et signale utilement la valeur manquante du manager. | 0 |

## Table `order_details`

2155 -> 2155 lignes, 5 -> 5 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : fait) : Table order_details contient les lignes de détail d'une commande (grain: ligne d'ordre, clé probable composite orderID+productID). Les colonnes sont toutes des chaînes contenant uniquement des nombres, sans zéros initiaux. Aucun null, pas d'espaces visibles. Risque faible de perte d'information métier lors de la conversion numérique. Les outliers détectés sur unitPrice et quantity méritent une validation manuelle avant toute modification.

- Recommandation : Appliquer les casts numériques validés ci‑dessus.
- Recommandation : Vérifier l'unicité de la clé composite (orderID,productID) et éventuellement ajouter un flag_duplicate_keys.
- Recommandation : Contrôler les éventuels doublons exacts avec drop_duplicates.
- Recommandation : Surveiller les valeurs négatives ou manquantes même si aucune n'est détectée actuellement.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 6 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : orderID est purement numérique, la conversion en entier ne supprime aucune information métier. | 0 |
| 7 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : productID est un identifiant numérique, le cast en nombre est sans risque. | 0 |
| 8 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : unitPrice représente un prix, le convertir en décimal facilite les calculs. | 0 |
| 9 | Convertir en nombre | quantity | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : quantity est un compte d'articles, le cast en entier est approprié. | 0 |
| 10 | Convertir en nombre | discount | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : discount est un taux décimal, la conversion en nombre est sûre. | 0 |
| 25 | Ramener les valeurs extrêmes | unitPrice | kept | 60 valeurs extrêmes : 60 au-dessus de 92 | conservé à la demande de l'utilisateur | 0 |
| 26 | Ramener les valeurs extrêmes | quantity | kept | 24 valeurs extrêmes : 24 au-dessus de 90 | conservé à la demande de l'utilisateur | 0 |

## Table `orders`

830 -> 830 lignes, 8 -> 8 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 6898, Requested 2542. Please try again in 10.799999999s. Need more tokens? Upgrade to Dev Tier today at https

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 11 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 12 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 13 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 14 | Convertir en nombre | freight | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 15 | Convertir en date | orderDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 16 | Convertir en date | requiredDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 17 | Convertir en date | shippedDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 18 | Signaler les valeurs manquantes | shippedDate | flagged | 21 valeur(s) manquante(s) (3 %) : laissées vides, imputation soumise à validation humaine | 0 |
| 27 | Ramener les valeurs extrêmes | freight | applied | 34 valeurs extrêmes : 34 au-dessus de 325.58 | corrigé avec l'accord de l'utilisateur | 34 |

## Table `products`

77 -> 77 lignes, 6 -> 6 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 6641, Requested 2101. Please try again in 5.564999999s. Need more tokens? Upgrade to Dev Tier today at https:

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 19 | Supprimer les espaces superflus | quantityPerUnit | applied | 1 valeur(s) avec espaces superflus | 1 |
| 20 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 21 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 22 | Convertir en nombre | discontinued | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 23 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 28 | Ramener les valeurs extrêmes | unitPrice | kept | 3 valeurs extrêmes : 3 au-dessus de 93.25 | conservé à la demande de l'utilisateur | 0 |

## Table `shippers`

3 -> 3 lignes, 2 -> 2 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 6577, Requested 1722. Please try again in 2.242499999s. Need more tokens? Upgrade to Dev Tier today at https:

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 24 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |

## À valider par un humain

- employees.reportsTo : 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine | LLM : Le flag ne modifie pas les données et signale utilement la valeur manquante du manager.
- orders.shippedDate : 21 valeur(s) manquante(s) (3 %) : laissées vides, imputation soumise à validation humaine
