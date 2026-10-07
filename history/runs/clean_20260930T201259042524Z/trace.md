# Trace de nettoyage clean_20260930T201259042524Z

Statut : **WARN** · 20 correction(s) appliquée(s) · 2 refusée(s) par le LLM · 6 point(s) à valider

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

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table 'categories' semble être une dimension de référence avec 8 lignes, chaque ligne représente une catégorie unique ; la clé probable est categoryID, aucune valeur manquante ni doublon apparent ; les colonnes sont de type texte, les descriptions sont courtes ; le risque principal serait de perdre d'éventuels zéros initiaux si la clé était alphanumérique.

- Recommandation : Vérifier que categoryID ne comporte jamais de zéros initiaux ou de préfixes alphanumériques avant de le convertir définitivement en numérique
- Recommandation : Confirmer qu'aucune catégorie n'est dupliquée et que la clé reste unique après conversion
- Recommandation : Documenter le changement de type dans le dictionnaire de données

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 1 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Les valeurs de categoryID sont toutes numériques sans zéro initial, la conversion en nombre ne détruit aucune information métier. | 0 |

## Table `customers`

91 -> 91 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table customers, grain au niveau client avec customerID comme clé primaire, toutes les colonnes sont de type texte et aucune valeur manquante ni doublon apparent ; la qualité est globalement bonne mais un léger problème d'espaces superflus a été détecté. Risque de perte d'information très faible car le nettoyage ne modifie que les espaces en début ou fin de chaîne.

- Recommandation : Vérifier après le trim qu'aucun libellé de companyName n'est devenu identique à un autre (doublon éventuel).
- Recommandation : Exécuter les drapeaux flag_duplicate_keys et flag_missing pour confirmer l'absence de clés dupliquées ou de valeurs manquantes.
- Recommandation : Envisager d'appliquer normalize_country sur la colonne country pour harmoniser les libellés.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 2 | Supprimer les espaces superflus | companyName | applied | 1 valeur(s) avec espaces superflus | LLM : Supprimer les espaces superflus sur companyName est sans risque et améliore la cohérence des libellés. | 1 |

## Table `employees`

9 -> 9 lignes, 6 -> 6 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table employees semble être une dimension avec grain au niveau de chaque salarié, clé probable employeeID, 9 lignes sans doublons apparents, quelques valeurs manquantes dans reportsTo (manager). Les colonnes sont de type texte mais contiennent des identifiants numériques, aucune donnée sensible à perdre. Risques principaux : perte de zéros initiaux sur employeeID ou reportsTo, mais les échantillons ne montrent pas de tels cas.

- Recommandation : Vérifier manuellement qu'aucun employeeID ne possède de zéros initiaux avant la conversion.
- Recommandation : Confirmer que la colonne reportsTo doit être numérique et que les valeurs nulles correspondent bien à des top‑level managers.
- Recommandation : Exécuter un contrôle d'unicité sur employeeID (flag_duplicate_keys) et envisager de le faire flagger.
- Recommandation : Standardiser les valeurs de country (outil normalize_country) et nettoyer les espaces éventuels (trim_whitespace) si besoin.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 3 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Conversion en nombre de employeeID est sûre car les valeurs sont purement numériques et ne comportent pas de zéros initiaux. | 0 |
| 4 | Convertir en nombre | reportsTo | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : Conversion en nombre de reportsTo est appropriée pour un champ de clé étrangère numérique, la valeur null sera conservée. | 0 |
| 5 | Signaler les valeurs manquantes | reportsTo | flagged | 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine | LLM : Le flag_missing ne modifie pas les données et permet de repérer les managers manquants, ce qui est pertinent. | 0 |

## Table `order_details`

2155 -> 2155 lignes, 5 -> 5 colonnes

**Analyse LLM** (openai/gpt-oss-120b, rôle : fait) : La table order_details représente le grain ligne de commande (une ligne par produit commandé), avec orderID et productID comme clés potentielles, unitPrice, quantity et discount comme mesures. Les colonnes sont toutes de type texte alors que les valeurs sont numériques, ce qui indique un problème de typage mais aucune valeur manquante n’est détectée. Le risque principal est de convertir les identifiants en nombre si d’autres tables les conservent en texte, ce qui pourrait casser les jointures. Les valeurs numériques semblent correctes, mais des outliers sont signalés pour unitPrice et quantity, ce qui mérite une vérification métier.

- Recommandation : Valider avec le propriétaire métier que les colonnes orderID et productID peuvent être converties en entier avant de les transformer.
- Recommandation : Vérifier que les tables de faits ou de dimensions connexes utilisent le même type (texte ou entier) pour les clés orderID et productID.
- Recommandation : Examiner les valeurs outliers signalées pour unitPrice et quantity afin de décider d’un éventuel nettoyage ou d’une exclusion.
- Recommandation : Envisager d’ajouter une contrainte d’unicité sur (orderID,productID) pour détecter d’éventuels doublons de lignes.

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 6 | Convertir en nombre | orderID | rejected | 100 % des valeurs sont numériques : conversion en nombre | LLM : Conversion de orderID en nombre pourrait rompre les jointures si les tables liées utilisent encore du texte. | 0 |
| 7 | Convertir en nombre | productID | rejected | 100 % des valeurs sont numériques : conversion en nombre | LLM : Conversion de productID en nombre présente le même risque de rupture de jointure. | 0 |
| 8 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : unitPrice doit être numérique pour les calculs de montant. | 0 |
| 9 | Convertir en nombre | quantity | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : quantity doit être numérique pour les agrégations. | 0 |
| 10 | Convertir en nombre | discount | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : discount doit être numérique pour appliquer les réductions. | 0 |
| 11 | Signaler les valeurs extrêmes | unitPrice | flagged | 60 valeur(s) extrême(s) hors [-48.00 ; 92.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers sur unitPrice est pertinent pour détecter des prix anormaux. | 0 |
| 12 | Signaler les valeurs extrêmes | quantity | flagged | 24 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers sur quantity est pertinent pour repérer des quantités inhabituelles. | 0 |

## Table `orders`

830 -> 830 lignes, 8 -> 8 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 6572, Requested 2726. Please try again in 9.735s. Need more tokens? Upgrade to Dev Tier today at https://cons

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 13 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 14 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 15 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 16 | Convertir en nombre | freight | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 17 | Convertir en date | orderDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 18 | Convertir en date | requiredDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 19 | Convertir en date | shippedDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 20 | Signaler les valeurs extrêmes | freight | flagged | 34 valeur(s) extrême(s) hors [-220.77 ; 325.58] (écart interquartile x3) : signalées, non modifiées | 0 |
| 21 | Signaler les valeurs manquantes | shippedDate | flagged | 21 valeur(s) manquante(s) (3 %) : laissées vides, imputation soumise à validation humaine | 0 |

## Table `products`

77 -> 77 lignes, 6 -> 6 colonnes

> LLM (openai/gpt-oss-120b) indisponible pour cette table, règles utilisées : Groq HTTP 429 : {"error":{"message":"Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01knan9xctf86rxcxc43emy5a5` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Used 6233, Requested 2593. Please try again in 6.194999999s. Need more tokens? Upgrade to Dev Tier today at https:

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

**Analyse LLM** (openai/gpt-oss-120b, rôle : dimension) : Table shippers de 3 lignes, 2 colonnes, aucune valeur manquante, clé probable shipperID, petite dimension de référence, données déjà propres, risque limité de perte d'information

- Recommandation : Vérifier que les clés shipperID sont utilisées comme texte ailleurs (ex. jointures) avant de convertir
- Recommandation : Confirmer qu'aucune valeur future ne contiendra de zéros initiaux qui seraient perdus après cast

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 28 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | LLM : shipperID ne comporte aucun zéro initial et toutes les valeurs sont numériques, la conversion en nombre ne détruit aucune information métier | 0 |

## À valider par un humain

- employees.reportsTo : 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine | LLM : Le flag_missing ne modifie pas les données et permet de repérer les managers manquants, ce qui est pertinent.
- order_details.unitPrice : 60 valeur(s) extrême(s) hors [-48.00 ; 92.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers sur unitPrice est pertinent pour détecter des prix anormaux.
- order_details.quantity : 24 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées | LLM : Flag d'outliers sur quantity est pertinent pour repérer des quantités inhabituelles.
- orders.freight : 34 valeur(s) extrême(s) hors [-220.77 ; 325.58] (écart interquartile x3) : signalées, non modifiées
- orders.shippedDate : 21 valeur(s) manquante(s) (3 %) : laissées vides, imputation soumise à validation humaine
- products.unitPrice : 3 valeur(s) extrême(s) hors [-46.75 ; 93.25] (écart interquartile x3) : signalées, non modifiées
