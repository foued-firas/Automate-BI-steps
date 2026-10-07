# Trace de nettoyage clean_20261001T100846287596Z

Statut : **WARN** · 24 correction(s) appliquée(s) · 0 refusée(s) par le LLM · 2 point(s) signalé(s)

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

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table petite de 8 lignes décrivant des catégories produit, grain au niveau catégorie, clé primaire probable categoryID, aucune valeur manquante, pas de doublons, colonnes déjà propres.

- Recommandation : Appliquer clean_column_names sur toutes les colonnes
- Recommandation : trim_whitespace sur categoryName et description
- Recommandation : flag_duplicate_keys pour vérifier l'unicité future
- Recommandation : drop_empty_rows/columns (aucune ligne/colonne vide)
- Recommandation : imputer_missing non nécessaire ici

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 1 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : categoryID ne comporte que des chiffres sans zéros initiaux, le convertir en entier ne perd aucune information métier et facilite les jointures. | 0 |

## Table `customers`

91 -> 91 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table customers contient 91 lignes, chaque ligne représente un client unique (grain client). La clé primaire est customerID (distinct, sans null). Les colonnes sont bien typées en texte, sans valeurs manquantes, mais un léger problème d'espaces dans companyName. La qualité globale est bonne, risque de doublons ou d'incohérences de noms de pays faible.

- Recommandation : Appliquer clean_column_names pour uniformiser les noms de colonnes
- Recommandation : Normaliser les valeurs de country avec normalize_country
- Recommandation : Vérifier les doublons de clés avec flag_duplicate_keys puis drop_duplicates si nécessaire
- Recommandation : Uniformiser les variantes de city ou country avec merge_category_variants si besoin

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 2 | Supprimer les espaces et caractères invisibles | companyName | applied | 1 valeur(s) avec espaces en trop, retours à la ligne ou caractères invisibles | LLM : Supprimer les espaces superflus ne modifie pas le contenu métier et corrige le seul cas détecté. | 1 |

## Table `employees`

9 -> 9 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table employees (9 lignes) ressemble à une dimension employé avec un identifiant, un nom, un titre, ville, pays et le manager (reportsTo). Les colonnes sont déjà propres, peu de valeurs manquantes (reportsTo) et aucune donnée numérique stockée en texte. Risque principal : perte d'information si les IDs contiennent des zéros initiaux, ce qui n'est pas le cas ici.

- Recommandation : Appliquer clean_column_names pour uniformiser les noms (ex. employee_id, reports_to).
- Recommandation : Standardiser les pays avec normalize_country (USA→US, UK→GB).
- Recommandation : Vérifier l'unicité de employeeID et supprimer d'éventuels doublons avec drop_duplicates.
- Recommandation : Imputer ou laisser null les valeurs manquantes de reportsTo selon la logique métier.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 3 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : employeeID ne comporte pas de zéros initiaux, le convertir en nombre facilite les jointures sans perdre d'information métier. | 0 |
| 4 | Convertir en nombre | reportsTo | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : reportsTo est une clé étrangère numérique stockée en texte ; la conversion en nombre conserve la relation hiérarchique. | 0 |
| 5 | Signaler les valeurs manquantes | reportsTo | flagged | 1 valeur(s) manquante(s) (11 %) : laissées vides | LLM : flag_missing ne modifie pas les données et permet de repérer le manager manquant (ex. CEO). | 0 |

## Table `order_details`

2155 -> 2155 lignes, 5 -> 5 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : fait) : La table order_details est un fait détaillant chaque ligne de commande (grain: ligne de commande). Les colonnes orderID et productID sont des clés de jointure vers les dimensions Orders et Products. Toutes les colonnes sont de type texte mais contiennent uniquement des valeurs numériques, sans valeurs manquantes ni zéros initiaux. Le risque principal est de perdre le sens métier si l’on convertit des identifiants en texte, mais ici les IDs sont purement numériques, donc la conversion est sûre.

- Recommandation : Appliquer cast_numeric aux colonnes indiquées puis définir les types dans le modèle Power BI (int pour les IDs, decimal pour unitPrice, int pour quantity, decimal pour discount).
- Recommandation : Créer une clé primaire composite (orderID,productID) et vérifier l’unicité avec flag_duplicate_keys.
- Recommandation : Envisager round_money sur unitPrice si des décimales supplémentaires apparaissent.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 6 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : orderID ne comporte aucun zéro initial ni caractère spécial, le convertir en nombre facilite les jointures. | 0 |
| 7 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : productID est un identifiant numérique pur, la conversion en nombre ne détruit aucune information. | 0 |
| 8 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : unitPrice doit être numérique pour les calculs de montant, la conversion est appropriée. | 0 |
| 9 | Convertir en nombre | quantity | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : quantity représente un nombre d'unités, il faut le convertir en type numérique. | 0 |
| 10 | Convertir en nombre | discount | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : discount est déjà exprimé entre 0 et 1, le convertir en nombre permet les agrégations. | 0 |

## Table `orders`

830 -> 830 lignes, 8 -> 8 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 7316, Requested 3092. Please try again in 18.06s. Need more tokens? Upgrade to Dev Tier today at https://cons

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
| 27 | Traiter les valeurs extrêmes | freight | kept | 1 valeur extrême : 1 en dessous de 0,12 (valeur habituelle : 41,36) | conservé à la demande de l'utilisateur | 0 |

## Table `products`

77 -> 77 lignes, 6 -> 12 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 7046, Requested 2816. Please try again in 13.965s. Need more tokens? Upgrade to Dev Tier today at https://con

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

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 6660, Requested 2140. Please try again in 6s. Need more tokens? Upgrade to Dev Tier today at https://console.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 26 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |

## Points signalés (information, rien n'a été modifié)

- employees.reportsTo : 1 valeur(s) manquante(s) (11 %) : laissées vides | LLM : flag_missing ne modifie pas les données et permet de repérer le manager manquant (ex. CEO).
- orders.shippedDate : 21 valeur(s) manquante(s) (3 %) : laissées vides
