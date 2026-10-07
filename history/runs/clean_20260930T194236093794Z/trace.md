# Trace de nettoyage clean_20260930T194236093794Z

Statut : **WARN** · 22 correction(s) appliquée(s) · 0 refusée(s) par le LLM · 6 point(s) à valider

Planificateur : rules

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

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 1 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |

## Table `customers`

91 -> 91 lignes, 6 -> 6 colonnes

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 2 | Supprimer les espaces superflus | companyName | applied | 1 valeur(s) avec espaces superflus | 1 |

## Table `employees`

9 -> 9 lignes, 6 -> 6 colonnes

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 3 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 4 | Convertir en nombre | reportsTo | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 5 | Signaler les valeurs manquantes | reportsTo | flagged | 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine | 0 |

## Table `order_details`

2155 -> 2155 lignes, 5 -> 5 colonnes

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 6 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 7 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 8 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 9 | Convertir en nombre | quantity | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 10 | Convertir en nombre | discount | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 11 | Signaler les valeurs extrêmes | unitPrice | flagged | 60 valeur(s) extrême(s) hors [-48.00 ; 92.00] (écart interquartile x3) : signalées, non modifiées | 0 |
| 12 | Signaler les valeurs extrêmes | quantity | flagged | 24 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées | 0 |

## Table `orders`

830 -> 830 lignes, 8 -> 8 colonnes

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

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 28 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |

## À valider par un humain

- employees.reportsTo : 1 valeur(s) manquante(s) (11 %) : laissées vides, imputation soumise à validation humaine
- order_details.unitPrice : 60 valeur(s) extrême(s) hors [-48.00 ; 92.00] (écart interquartile x3) : signalées, non modifiées
- order_details.quantity : 24 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées
- orders.freight : 34 valeur(s) extrême(s) hors [-220.77 ; 325.58] (écart interquartile x3) : signalées, non modifiées
- orders.shippedDate : 21 valeur(s) manquante(s) (3 %) : laissées vides, imputation soumise à validation humaine
- products.unitPrice : 3 valeur(s) extrême(s) hors [-46.75 ; 93.25] (écart interquartile x3) : signalées, non modifiées
