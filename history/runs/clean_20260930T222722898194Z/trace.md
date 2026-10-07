# Trace de nettoyage clean_20260930T222722898194Z

Statut : **WARN** · 25 correction(s) appliquée(s) · 0 refusée(s) par le LLM · 2 point(s) signalé(s)

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

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table « categories » : 8 lignes, 3 colonnes, chaque ligne représente une catégorie unique (grain = niveau catégorie). La colonne categoryID est la clé primaire, déjà sans doublons ni valeurs manquantes, et les valeurs sont des chaînes numériques simples. La qualité globale est bonne, mais les noms de colonnes et le type de la clé peuvent être optimisés pour l’ETL.

- Recommandation : Appliquer clean_column_names pour uniformiser les noms de colonnes
- Recommandation : Trim_whitespace et fix_encoding sur toutes les colonnes textuelles
- Recommandation : Vérifier l’unicité avec flag_duplicate_keys puis drop_duplicates si besoin
- Recommandation : Normaliser la clé avec normalize_keys si elle doit être jointe à d’autres tables

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 1 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Les IDs sont des nombres entiers sans zéros initiaux ni signification textuelle, la conversion en type numérique ne perd aucune information métier. | 0 |

## Table `customers`

91 -> 91 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table customers, grain probable = un client par ligne avec customerID comme clé primaire, toutes les colonnes sont des chaînes sans valeurs nulles, bonne distinctivité, aucune donnée numérique à convertir, risque faible de perte d'information.

- Recommandation : Appliquer clean_column_names pour uniformiser les noms de colonnes
- Recommandation : Normaliser les valeurs de pays avec normalize_country
- Recommandation : Vérifier les doublons de clés avec flag_duplicate_keys puis drop_duplicates si nécessaire
- Recommandation : Uniformiser les majuscules/minuscules avec fix_case si besoin

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 2 | Supprimer les espaces et caractères invisibles | companyName | applied | 1 valeur(s) avec espaces en trop, retours à la ligne ou caractères invisibles | LLM : Supprimer les espaces superflus ne modifie pas le contenu métier et corrige le seul cas détecté. | 1 |

## Table `employees`

9 -> 9 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table employees, 9 lignes, grain = un enregistrement par salarié, clé primaire probable employeeID, colonne reportsTo comme clé étrangère vers le manager. Les colonnes sont déjà propres, peu de valeurs manquantes (reportsTo = 1) et aucune valeur anormale. Risque principal : perte d'information si on convertit des identifiants contenant des zéros initiaux, mais ici les IDs sont simples.

- Recommandation : Après cast_numeric, définir employeeID comme clé primaire et reportsTo comme clé étrangère nullable.
- Recommandation : Vérifier l'unicité de employeeID et supprimer d'éventuels doublons.
- Recommandation : Standardiser les noms de pays (USA, UK) si besoin et appliquer trim_whitespace sur toutes les colonnes textuelles.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 3 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : employeeID ne comporte que des chiffres et aucun zéro initial, la conversion en numérique facilitera les jointures. | 0 |
| 4 | Convertir en nombre | reportsTo | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : reportsTo ne contient que des chiffres, la conversion en numérique est sûre pour les relations hiérarchiques. | 0 |
| 5 | Signaler les valeurs manquantes | reportsTo | flagged | 1 valeur(s) manquante(s) (11 %) : laissées vides | LLM : Le flag_missing signale correctement la valeur manquante sans altérer les données, utile pour le contrôle qualité. | 0 |

## Table `order_details`

2155 -> 2155 lignes, 5 -> 5 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 6131, Requested 2481. Please try again in 4.59s. Need more tokens? Upgrade to Dev Tier today at https://conso

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 6 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 7 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 8 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 9 | Convertir en nombre | quantity | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 10 | Convertir en nombre | discount | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |

## Table `orders`

830 -> 830 lignes, 8 -> 8 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 5828, Requested 2834. Please try again in 4.965s. Need more tokens? Upgrade to Dev Tier today at https://cons

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 11 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 12 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 13 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 14 | Convertir en nombre | freight | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 15 | Convertir en date | orderDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 16 | Convertir en date | requiredDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 17 | Convertir en date | shippedDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 18 | Signaler les valeurs manquantes | shippedDate | flagged | 21 valeur(s) manquante(s) (3 %) : laissées vides | 0 |
| 27 | Traiter les valeurs extrêmes | freight | applied | 1 valeur extrême : 1 en dessous de 0,12 (valeur habituelle : 41,36) | ramené dans la plage habituelle avec l'accord de l'utilisateur | 1 |

## Table `products`

77 -> 77 lignes, 6 -> 12 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 5522, Requested 2558. Please try again in 600ms. Need more tokens? Upgrade to Dev Tier today at https://conso

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 19 | Supprimer les espaces et caractères invisibles | productName | applied | 1 valeur(s) avec espaces en trop, retours à la ligne ou caractères invisibles | 1 |
| 20 | Supprimer les espaces et caractères invisibles | quantityPerUnit | applied | 1 valeur(s) avec espaces en trop, retours à la ligne ou caractères invisibles | 1 |
| 21 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 22 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 23 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 24 | Convertir en booléen | discontinued | applied | colonne oui/non codée 0 / 1 : conversion en booléen (1 = vrai) | 77 |
| 25 | Décomposer les conditionnements en colonnes | quantityPerUnit | applied | 77 conditionnements décomposés sur 77 en colonnes exploitables : nb_unites, taille_unite, unite_mesure, contenant, quantite_totale, unite_base (quantité totale convertie en g ou en ml) | 77 |

## Table `shippers`

3 -> 3 lignes, 2 -> 2 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table shippers, petite table de référence contenant 3 transporteurs, grain au niveau du transporteur, clé primaire shipperID sans valeurs manquantes ni doublons, qualité globale très bonne, risque limité de perte d'information lors de la conversion car aucun zéro initial ni format spécial.

- Recommandation : Appliquer clean_column_names pour uniformiser les noms de colonnes
- Recommandation : Utiliser trim_whitespace sur toutes les colonnes textuelles
- Recommandation : Exécuter flag_duplicate_keys puis drop_duplicates si besoin
- Recommandation : Vérifier que les colonnes companyName sont correctement capitalisées ou normalisées

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 26 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : shipperID ne comporte que des entiers simples, aucune information métier ne sera perdue en le convertissant en numérique, ce qui facilitera les jointures. | 0 |

## Points signalés (information, rien n'a été modifié)

- employees.reportsTo : 1 valeur(s) manquante(s) (11 %) : laissées vides | LLM : Le flag_missing signale correctement la valeur manquante sans altérer les données, utile pour le contrôle qualité.
- orders.shippedDate : 21 valeur(s) manquante(s) (3 %) : laissées vides
