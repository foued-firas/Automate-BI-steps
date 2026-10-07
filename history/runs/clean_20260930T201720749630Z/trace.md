# Trace de nettoyage clean_20260930T201720749630Z

Statut : **WARN** · 21 correction(s) appliquée(s) · 1 refusée(s) par le LLM · 6 point(s) à valider

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

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table 'categories' contient 8 lignes, 3 colonnes, aucune valeur manquante, chaque ligne représente une catégorie unique ; grain probable au niveau de la catégorie, clé primaire probable = categoryID, qualité élevée, risque minimal de perte d'information métier lors de la conversion numérique car les IDs sont simples sans zéros initiaux

- Recommandation : Vérifier que les clés categoryID ne contiennent jamais de zéros initiaux avant de les convertir
- Recommandation : Ajouter un flag_duplicate_keys pour confirmer l'unicité des IDs
- Recommandation : Conserver categoryName et description tels quels, aucun nettoyage supplémentaire nécessaire

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 1 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Conversion en nombre de categoryID est sûre, les valeurs sont déjà numériques et ne comportent pas de zéros initiaux, ce qui facilite les jointures | 0 |

## Table `customers`

91 -> 91 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table customers, probablement une dimension client avec grain d'une ligne par client (customerID unique). Les colonnes sont toutes de type texte, aucune valeur manquante, distinctes, donc la qualité est élevée. Risques majeurs : perte d'information métier si on modifie le format des identifiants ou des codes, mais le nettoyage proposé est sans risque.

- Recommandation : Vérifier manuellement l'absence d'espaces internes pertinents dans les noms d'entreprise
- Recommandation : Appliquer éventuellement normalize_country sur la colonne country
- Recommandation : Utiliser flag_duplicate_keys pour confirmer l'unicité de customerID
- Recommandation : Contrôler l'encodage des caractères accentués avec fix_encoding si besoin

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 2 | Supprimer les espaces superflus | companyName | applied | 1 valeur(s) avec espaces superflus | LLM : Le trim des espaces superflus sur companyName ne supprime aucune donnée métier et améliore la cohérence des libellés. | 1 |

## Table `employees`

9 -> 9 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table employees semble être une dimension avec grain d'employé unique, clé probable employeeID (distinct=9, pas de null). Les colonnes sont majoritairement textuelles, mais employeeID et reportsTo contiennent uniquement des chiffres sans zéros initiaux. Une valeur manquante apparaît dans reportsTo (manager inconnu). Risque principal : la conversion numérique pourrait casser des jointures si d'autres tables utilisent des chaînes pour ces IDs.

- Recommandation : Vérifier la cohérence du type de données employeeID et reportsTo avec les tables de faits ou de hiérarchie avant de les convertir.
- Recommandation : Confirmer la politique d'imputation ou de gestion des valeurs manquantes de reportsTo (ex. manager top‑niveau).
- Recommandation : Exécuter le flag_duplicate_keys pour s'assurer qu'employeeID reste unique.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 3 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : employeeID ne comporte pas de zéros initiaux et est uniquement numérique, la conversion en nombre ne perd aucune information métier. | 0 |
| 4 | Convertir en nombre | reportsTo | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : reportsTo est également numérique et la conversion garde la valeur null, aucune perte d'information. | 0 |
| 5 | Signaler les valeurs manquantes | reportsTo | flagged | 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine | LLM : flag_missing est un outil de signalement qui ne modifie pas les données et aide à repérer les managers manquants. | 0 |

## Table `order_details`

2155 -> 2155 lignes, 5 -> 5 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : fait) : La table order_details représente probablement le grain ligne de commande (détail d'une commande) avec les colonnes orderID, productID, unitPrice, quantity et discount. Les colonnes sont actuellement de type texte mais contiennent uniquement des valeurs numériques, sans zéros initiaux apparents. Aucun null n'est présent, le nombre de lignes (2155) et de distincts indique une granularité fine. Le risque principal serait de perdre des informations d'identifiant si des zéros initiaux existaient, ce qui n'est pas le cas ici. Les flags d'anomalies sont utiles pour la validation métier.

- Recommandation : Vérifier auprès du propriétaire métier que les seuils d'outliers (unitPrice, quantity) sont pertinents.
- Recommandation : Confirmer que la conversion de orderID et productID en numérique n'affecte pas d'éventuelles jointures externes basées sur des chaînes.
- Recommandation : S'assurer que les valeurs négatives ou nulles n'apparaissent pas après conversion (ex. discount).

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 6 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Conversion sûre en nombre, aucun zéro initial détecté. | 0 |
| 7 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Conversion sûre en nombre, les IDs sont purement numériques. | 0 |
| 8 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : unitPrice doit être numérique pour les calculs de prix. | 0 |
| 9 | Convertir en nombre | quantity | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : quantity doit être numérique pour les agrégations. | 0 |
| 10 | Convertir en nombre | discount | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : discount est un taux numérique, conversion appropriée. | 0 |
| 11 | Signaler les valeurs extrêmes | unitPrice | flagged | 60 valeur(s) extrême(s) hors [-48.00 ; 92.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers conservé, aucune modification des données. | 0 |
| 12 | Signaler les valeurs extrêmes | quantity | flagged | 24 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers conservé, aucune modification des données. | 0 |

## Table `orders`

830 -> 830 lignes, 8 -> 8 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : fait) : La table orders semble être une table de faits au grain commande (une ligne par orderID), avec orderID comme clé primaire et des clés étrangères vers client, employé et transporteur. Les colonnes sont toutes en texte alors que plusieurs sont naturellement numériques ou dates, et il y a quelques valeurs manquantes sur shippedDate. Le risque principal est de casser les jointures si les clés sont converties différemment que dans les tables de dimensions.

- Recommandation : Valider manuellement la décision de garder orderID en texte ou le convertir en nombre pour assurer la cohérence avec les tables de dimensions.
- Recommandation : Imputer ou traiter les 21 valeurs manquantes de shippedDate après validation métier.
- Recommandation : Vérifier que les conversions numériques d'employeeID et shipperID correspondent aux types utilisés dans les tables de dimensions associées.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 13 | Convertir en nombre | orderID | rejected | 100 % des valeurs sont numériques : conversion en nombre | LLM : Convertir orderID en nombre pourrait rompre les jointures si les autres tables conservent cet identifiant en texte. | 0 |
| 14 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : employeeID est purement numérique et aucune perte d'information n'est attendue. | 0 |
| 15 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : shipperID ne comporte que des chiffres, la conversion en nombre est sûre. | 0 |
| 16 | Convertir en nombre | freight | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : freight représente des montants décimaux, la conversion en type numérique est appropriée. | 0 |
| 17 | Convertir en date | orderDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | LLM : orderDate est déjà au format ISO, la conversion en type date ne change rien au sens. | 0 |
| 18 | Convertir en date | requiredDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | LLM : requiredDate est également au format ISO, conversion en date recommandée. | 0 |
| 19 | Convertir en date | shippedDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | LLM : shippedDate contient des dates valides et des nulls, la conversion en date conserve les manquants. | 0 |
| 20 | Signaler les valeurs extrêmes | freight | flagged | 34 valeur(s) extrême(s) hors [-220.77 ; 325.58] (écart interquartile x3) : signalées, non modifiées | LLM : Le flag outliers sur freight ne modifie pas les données et aide à repérer des valeurs anormales. | 0 |
| 21 | Signaler les valeurs manquantes | shippedDate | flagged | 21 valeur(s) manquante(s) (3 %) : laissées vides, imputation soumise à validation humaine | LLM : Le flag missing sur shippedDate signale les 21 valeurs nulles sans les altérer. | 0 |

## Table `products`

77 -> 77 lignes, 6 -> 6 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 7465, Requested 2345. Please try again in 13.575s. Need more tokens? Upgrade to Dev Tier today at https://con

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 22 | Supprimer les espaces superflus | quantityPerUnit | applied | 1 valeur(s) avec espaces superflus | 1 |
| 23 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 24 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 25 | Convertir en nombre | discontinued | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 26 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 27 | Signaler les valeurs extrêmes | unitPrice | flagged | 3 valeur(s) extrême(s) hors [-46.75 ; 93.25] (écart interquartile x3) : signalées, non modifiées | 0 |

## Table `shippers`

3 -> 3 lignes, 2 -> 2 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 7380, Requested 1792. Please try again in 8.79s. Need more tokens? Upgrade to Dev Tier today at https://conso

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 28 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |

## À valider par un humain

- employees.reportsTo : 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine | LLM : flag_missing est un outil de signalement qui ne modifie pas les données et aide à repérer les managers manquants.
- order_details.unitPrice : 60 valeur(s) extrême(s) hors [-48.00 ; 92.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers conservé, aucune modification des données.
- order_details.quantity : 24 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers conservé, aucune modification des données.
- orders.freight : 34 valeur(s) extrême(s) hors [-220.77 ; 325.58] (écart interquartile x3) : signalées, non modifiées | LLM : Le flag outliers sur freight ne modifie pas les données et aide à repérer des valeurs anormales.
- orders.shippedDate : 21 valeur(s) manquante(s) (3 %) : laissées vides, imputation soumise à validation humaine | LLM : Le flag missing sur shippedDate signale les 21 valeurs nulles sans les altérer.
- products.unitPrice : 3 valeur(s) extrême(s) hors [-46.75 ; 93.25] (écart interquartile x3) : signalées, non modifiées
