# Trace de nettoyage clean_20260930T193301409967Z

Statut : **WARN** · 28 correction(s) appliquée(s) · 9 point(s) à valider

## Fichiers lus

- `clients_sale.csv` (cp1252, séparateur ';') : tables ['clients_sale'] · sha256 18b33967ec6c…
- `ventes_sale.xlsx` (Excel) : tables ['ventes_sale_commandes', 'ventes_sale_lignes', 'ventes_sale_produits'] · sha256 cc72b5e9dc27…

## Table `clients_sale`

94 -> 91 lignes, 6 -> 6 colonnes

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 1 | Uniformiser les valeurs manquantes | contactTitle | applied | 1 marqueur(s) de valeur manquante ['n/a'] remplacés par une vraie valeur vide | 1 |
| 2 | Uniformiser les valeurs manquantes | city | applied | 1 marqueur(s) de valeur manquante ['null'] remplacés par une vraie valeur vide | 1 |
| 3 | Supprimer les lignes vides | (table) | applied | 1 ligne(s) entièrement vide(s) | 1 |
| 4 | Supprimer les espaces superflus | companyName | applied | 14 valeur(s) avec espaces superflus | 14 |
| 5 | Corriger l'encodage des accents | contactName | applied | 1 valeur(s) avec accents mal encodés (ex. 'Ã©' au lieu de 'é') | 1 |
| 6 | Standardiser les pays | country | applied | 22 nom(s) de pays standardisé(s) (ex. 'United States' -> 'USA') | 22 |
| 7 | Supprimer les doublons exacts | (table) | applied | 2 ligne(s) en double exact (2 %) | 2 |
| 8 | Signaler les valeurs manquantes | contactTitle | flagged | 1 valeur(s) manquante(s) (1 %) : laissées vides, imputation soumise à validation humaine | 0 |
| 9 | Signaler les valeurs manquantes | city | flagged | 1 valeur(s) manquante(s) (1 %) : laissées vides, imputation soumise à validation humaine | 0 |

## Table `ventes_sale_commandes`

120 -> 120 lignes, 8 -> 8 colonnes

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 10 | Uniformiser les valeurs manquantes | shippedDate | applied | 2 marqueur(s) de valeur manquante ['-', 'n/a'] remplacés par une vraie valeur vide | 2 |
| 11 | Uniformiser les valeurs manquantes | freight | applied | 1 marqueur(s) de valeur manquante ['inconnu'] remplacés par une vraie valeur vide | 1 |
| 12 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 13 | Convertir en nombre | employeeID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 14 | Convertir en nombre | shipperID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 15 | Convertir en nombre | freight | applied | 100 % des valeurs sont numériques : conversion en nombre (119 au format texte, ex. virgule décimale ou symbole monétaire) | 119 |
| 16 | Convertir en date | orderDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ (30 dans un autre format, lecture jour/mois) | 30 |
| 17 | Convertir en date | requiredDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 18 | Convertir en date | shippedDate | applied | 100 % des valeurs sont des dates : conversion au format AAAA-MM-JJ | 0 |
| 19 | Signaler les valeurs extrêmes | freight | flagged | 1 valeur(s) extrême(s) hors [-201.76 ; 292.73] (écart interquartile x3) : signalées, non modifiées | 0 |
| 20 | Signaler les valeurs manquantes | shippedDate | flagged | 2 valeur(s) manquante(s) (2 %) : laissées vides, imputation soumise à validation humaine | 0 |
| 21 | Signaler les valeurs manquantes | freight | flagged | 1 valeur(s) manquante(s) (1 %) : laissées vides, imputation soumise à validation humaine | 0 |

## Table `ventes_sale_lignes`

322 -> 320 lignes, 5 -> 5 colonnes

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 22 | Supprimer les espaces superflus | unitPrice | applied | 1 valeur(s) avec espaces superflus | 1 |
| 23 | Convertir en nombre | orderID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 24 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 25 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre (1 au format texte, ex. virgule décimale ou symbole monétaire) | 1 |
| 26 | Convertir en nombre | quantity | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 27 | Convertir en nombre | discount | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 28 | Supprimer les doublons exacts | (table) | applied | 2 ligne(s) en double exact (1 %) | 2 |
| 29 | Signaler les valeurs négatives | quantity | flagged | 1 valeur(s) négative(s) dans une colonne qui devrait être positive : à vérifier | 0 |
| 30 | Signaler les valeurs extrêmes | unitPrice | flagged | 9 valeur(s) extrême(s) hors [-41.00 ; 79.40] (écart interquartile x3) : signalées, non modifiées | 0 |
| 31 | Signaler les valeurs extrêmes | quantity | flagged | 1 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées | 0 |

## Table `ventes_sale_produits`

77 -> 77 lignes, 6 -> 6 colonnes

| # | Outil | Colonne | Statut | Pourquoi | Valeurs modifiées |
|---|---|---|---|---|---|
| 32 | Supprimer les espaces superflus | quantityPerUnit | applied | 1 valeur(s) avec espaces superflus | 1 |
| 33 | Convertir en nombre | productID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 34 | Convertir en nombre | unitPrice | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 35 | Convertir en nombre | categoryID | applied | 100 % des valeurs sont numériques : conversion en nombre | 0 |
| 36 | Convertir en booléen | discontinued | applied | valeurs oui/non hétérogènes ['non', 'oui'] : conversion en booléen | 77 |
| 37 | Signaler les valeurs extrêmes | unitPrice | flagged | 4 valeur(s) extrême(s) hors [-46.00 ; 94.00] (écart interquartile x3) : signalées, non modifiées | 0 |

## À valider par un humain

- clients_sale.contactTitle : 1 valeur(s) manquante(s) (1 %) : laissées vides, imputation soumise à validation humaine
- clients_sale.city : 1 valeur(s) manquante(s) (1 %) : laissées vides, imputation soumise à validation humaine
- ventes_sale_commandes.freight : 1 valeur(s) extrême(s) hors [-201.76 ; 292.73] (écart interquartile x3) : signalées, non modifiées
- ventes_sale_commandes.shippedDate : 2 valeur(s) manquante(s) (2 %) : laissées vides, imputation soumise à validation humaine
- ventes_sale_commandes.freight : 1 valeur(s) manquante(s) (1 %) : laissées vides, imputation soumise à validation humaine
- ventes_sale_lignes.quantity : 1 valeur(s) négative(s) dans une colonne qui devrait être positive : à vérifier
- ventes_sale_lignes.unitPrice : 9 valeur(s) extrême(s) hors [-41.00 ; 79.40] (écart interquartile x3) : signalées, non modifiées
- ventes_sale_lignes.quantity : 1 valeur(s) extrême(s) hors [-50.00 ; 90.00] (écart interquartile x3) : signalées, non modifiées
- ventes_sale_produits.unitPrice : 4 valeur(s) extrême(s) hors [-46.00 ; 94.00] (écart interquartile x3) : signalées, non modifiées
