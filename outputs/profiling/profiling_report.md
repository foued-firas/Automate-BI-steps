# Rapport de profilage — Agent 1

## metadata

- **run_id** : `prof_2026-10-03_133837`
- **generated_at** : 2026-10-03T13:38:37
- **source_dir** : `C:\Users\chihe\Desktop\5eme\ADSP\project_bi_ agents\Datasets\Import&Export\data`
- **spec_version** : 0.1
- **llm** : openai/gpt-oss-120b (ok (7/7 tables revues))

### files

| Fichier | Taille (octets) | Encodage | Séparateur | En-tête | Statut |
|---|---|---|---|---|---|
| categories.csv | 406 | ASCII | ',' | True | ok |
| customers.csv | 6758 | ISO-8859-1 | ',' | True | warning |
| employees.csv | 512 | ASCII | ',' | True | ok |
| order_details.csv | 42778 | ASCII | ',' | True | ok |
| orders.csv | 46283 | ASCII | ',' | True | ok |
| products.csv | 3531 | ISO-8859-1 | ',' | True | warning |
| shippers.csv | 79 | ASCII | ',' | True | ok |

## tables

### `categories` — 8 lignes × 3 colonnes

- Clés primaires candidates : [['categoryID'], ['categoryName'], ['description']]
- Lignes dupliquées : 0

| Colonne | Type détecté | Type attendu | Rôle | Manquants % | Distinctes | Min | Max | Exemples |
|---|---|---|---|---|---|---|---|---|
| categoryID | integer | integer | identifier | 0.0 | 8 | 1 | 8 | 1, 2, 3 |
| categoryName | string | string | text | 0.0 | 8 |  |  | Beverages, Condiments, Confections |
| description | string | string | text | 0.0 | 8 |  |  | Soft drinks, coffees, teas, beers, and ales, Sweet and savory sauces, relishes, spreads, and seasonings, Desserts, candies, and sweet breads |

### `customers` — 91 lignes × 6 colonnes

- Clés primaires candidates : [['customerID'], ['companyName'], ['contactName']]
- Lignes dupliquées : 0

| Colonne | Type détecté | Type attendu | Rôle | Manquants % | Distinctes | Min | Max | Exemples |
|---|---|---|---|---|---|---|---|---|
| customerID | string | string | identifier | 0.0 | 91 |  |  | ALFKI, ANATR, ANTON |
| companyName | string | string | text | 0.0 | 91 |  |  | Alfreds Futterkiste, Ana Trujillo Emparedados y helados, Antonio Moreno Taquería |
| contactName | string | string | text | 0.0 | 91 |  |  | Maria Anders, Ana Trujillo, Antonio Moreno |
| contactTitle | string | string | category | 0.0 | 12 |  |  | Sales Representative, Owner, Order Administrator |
| city | string | string | category | 0.0 | 69 |  |  | Berlin, Mexico City, London |
| country | string | string | category | 0.0 | 21 |  |  | Germany, Mexico, UK |

### `employees` — 9 lignes × 6 colonnes

- Clés primaires candidates : [['employeeID'], ['employeeName']]
- Lignes dupliquées : 0

| Colonne | Type détecté | Type attendu | Rôle | Manquants % | Distinctes | Min | Max | Exemples |
|---|---|---|---|---|---|---|---|---|
| employeeID | integer | integer | identifier | 0.0 | 9 | 1 | 9 | 1, 2, 3 |
| employeeName | string | string | text | 0.0 | 9 |  |  | Nancy Davolio, Andrew Fuller, Janet Leverling |
| title | string | string | category | 0.0 | 3 |  |  | Sales Representative, Vice President Sales, Sales Manager |
| city | string | string | category | 0.0 | 2 |  |  | New York, London |
| country | string | string | category | 0.0 | 2 |  |  | USA, UK |
| reportsTo | integer | integer | foreign_key | 11.11 | 3 | 2 | 8 | 8, 2, 5 |

### `order_details` — 2155 lignes × 5 colonnes

- Clés primaires candidates : [['orderID', 'productID']]
- Lignes dupliquées : 0

| Colonne | Type détecté | Type attendu | Rôle | Manquants % | Distinctes | Min | Max | Exemples |
|---|---|---|---|---|---|---|---|---|
| orderID | integer | integer | foreign_key | 0.0 | 830 | 10248 | 11077 | 10248, 10249, 10250 |
| productID | integer | integer | foreign_key | 0.0 | 77 | 1 | 77 | 11, 42, 72 |
| unitPrice | float | float | measure | 0.0 | 116 | 2.0 | 263.5 | 14, 9.8, 34.8 |
| quantity | integer | integer | measure | 0.0 | 55 | 1 | 130 | 12, 10, 5 |
| discount | float | float | measure | 0.0 | 11 | 0.0 | 0.25 | 0, 0.15, 0.05 |

### `orders` — 830 lignes × 8 colonnes

- Clés primaires candidates : [['orderID']]
- Lignes dupliquées : 0

| Colonne | Type détecté | Type attendu | Rôle | Manquants % | Distinctes | Min | Max | Exemples |
|---|---|---|---|---|---|---|---|---|
| orderID | integer | integer | identifier | 0.0 | 830 | 10248 | 11077 | 10248, 10249, 10250 |
| customerID | string | string | foreign_key | 0.0 | 89 |  |  | VINET, TOMSP, HANAR |
| employeeID | integer | integer | foreign_key | 0.0 | 9 | 1 | 9 | 5, 6, 4 |
| orderDate | date | date | date | 0.0 | 480 | 2013-07-04T00:00:00 | 2015-05-06T00:00:00 | 2013-07-04, 2013-07-05, 2013-07-08 |
| requiredDate | date | date | date | 0.0 | 454 | 2013-07-24T00:00:00 | 2015-06-11T00:00:00 | 2013-08-01, 2013-08-16, 2013-08-05 |
| shippedDate | date | date | date | 2.53 | 387 | 2013-07-10T00:00:00 | 2015-05-06T00:00:00 | 2013-07-16, 2013-07-10, 2013-07-12 |
| shipperID | integer | integer | foreign_key | 0.0 | 3 | 1 | 3 | 3, 1, 2 |
| freight | float | float | measure | 0.0 | 799 | 0.02 | 1007.64 | 32.38, 11.61, 65.83 |

### `products` — 77 lignes × 6 colonnes

- Clés primaires candidates : [['productID'], ['productName']]
- Lignes dupliquées : 0

| Colonne | Type détecté | Type attendu | Rôle | Manquants % | Distinctes | Min | Max | Exemples |
|---|---|---|---|---|---|---|---|---|
| productID | integer | integer | identifier | 0.0 | 77 | 1 | 77 | 1, 2, 3 |
| productName | string | string | text | 0.0 | 77 |  |  | Chai, Chang, Aniseed Syrup |
| quantityPerUnit | string | string | text | 0.0 | 70 |  |  | 10 boxes x 20 bags, 24 - 12 oz bottles, 12 - 550 ml bottles |
| unitPrice | float | float | measure | 0.0 | 62 | 2.5 | 263.5 | 18, 19, 10 |
| discontinued | integer | integer | flag | 0.0 | 2 | 0 | 1 | 0, 1 |
| categoryID | integer | integer | foreign_key | 0.0 | 8 | 1 | 8 | 1, 2, 7 |

### `shippers` — 3 lignes × 2 colonnes

- Clés primaires candidates : [['shipperID'], ['companyName']]
- Lignes dupliquées : 0

| Colonne | Type détecté | Type attendu | Rôle | Manquants % | Distinctes | Min | Max | Exemples |
|---|---|---|---|---|---|---|---|---|
| shipperID | integer | integer | identifier | 0.0 | 3 | 1 | 3 | 1, 2, 3 |
| companyName | string | string | text | 0.0 | 3 |  |  | Speedy Express, United Package, Federal Shipping |

## relationships

| ID | De | Vers | Cardinalité | Correspondance % | Orphelins | Méthode | Confiance |
|---|---|---|---|---|---|---|---|
| REL-001 | employees.reportsTo | employees.employeeID | many_to_one | 100.0 | 0 | value_overlap | 0.6 |
| REL-002 | order_details.orderID | orders.orderID | many_to_one | 100.0 | 0 | both | 0.95 |
| REL-003 | order_details.productID | products.productID | many_to_one | 100.0 | 0 | both | 0.95 |
| REL-004 | orders.customerID | customers.customerID | many_to_one | 100.0 | 0 | both | 0.95 |
| REL-005 | orders.employeeID | employees.employeeID | many_to_one | 100.0 | 0 | both | 0.95 |
| REL-006 | orders.shipperID | shippers.shipperID | many_to_one | 100.0 | 0 | both | 0.95 |
| REL-007 | products.categoryID | categories.categoryID | many_to_one | 100.0 | 0 | both | 0.95 |

## issues

| ID | Sévérité | Table | Colonne | Type | Lignes (%) | Description | Exemples | Action suggérée | Attendu | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| ISS-001 | 🟡 medium | customers |  | encoding_error | 30 (32.97 %) | Le fichier est encodé en ISO-8859-1 : lu en UTF-8, les caractères accentués sont remplacés par '�'. | ["Antonio Moreno Taquer�a", "Berglunds snabbk�p", "Lule�"] | reencode | non | rule |
| ISS-002 | 🟡 medium | products |  | encoding_error | 15 (19.48 %) | Le fichier est encodé en ISO-8859-1 : lu en UTF-8, les caractères accentués sont remplacés par '�'. | ["Gustaf's Knackebr�d", "Tunnbr�d", "NuNuCa�Nu�-Nougat-Creme"] | reencode | non | rule |
| ISS-003 | 🔵 low | customers | companyName | typo_suspected | 1 (1.1 %) | 'Blondesddsl père et fils' semble erronée : Le nom contient une séquence de caractères improbable "ddsl" qui ressemble à une faute de frappe. | ["Blondesddsl père et fils"] | investigate | non | llm |
| ISS-004 | 🔵 low | order_details | quantity | outlier | 87 (4.04 %) | 87 valeur(s) aberrante(s) dans quantity (hors de [-20.0, 60.0]). | [130, 120, 110] | flag_only | non | rule |
| ISS-005 | 🔵 low | order_details | unitPrice | outlier | 98 (4.55 %) | 98 valeur(s) aberrante(s) dans unitPrice (hors de [-18.0, 62.0]). | [263.5, 210.8, 123.79] | flag_only | non | rule |
| ISS-006 | 🔵 low | orders | freight | outlier | 67 (8.07 %) | 67 valeur(s) aberrante(s) dans freight (hors de [-103.695, 208.505]). | [1007.64, 890.78, 830.75] | flag_only | non | rule |
| ISS-007 | 🔵 low | products | quantityPerUnit | typo_suspected | 1 (1.3 %) | '50 bags x 30 sausgs.' semble erronée : Typo in word 'sausgs.'; likely should be 'sausages' | ["50 bags x 30 sausgs.", "50 bags x 30 sausages."] | correct_value | non | llm |
| ISS-008 | 🔵 low | products | unitPrice | outlier | 4 (5.19 %) | 4 valeur(s) aberrante(s) dans unitPrice (hors de [-16.75, 63.25]). | [263.5, 123.79, 97.0] | flag_only | non | rule |
| ISS-009 | ⚪ info | employees | reportsTo | missing_values | 1 (11.11 %) | 1 valeur(s) manquante(s) (11.11 %) dans reportsTo. | [] | keep_as_null | oui | rule |
| ISS-010 | ⚪ info | orders | shippedDate | missing_values | 21 (2.53 %) | 21 valeur(s) manquante(s) (2.53 %) dans shippedDate. | [] | keep_as_null | oui | rule |

## summary

Le diagnostic montre que l’ensemble des 7 tables (3 173 lignes) atteint un score global de 96,3 % et est déclaré prêt pour le nettoyage. Les tables « categories », « employees » et « shippers » affichent un score parfait de 100 %, tandis que « customers », « order_details », « orders » et « products » restent très satisfaisantes (entre 91 % et 98 %). Les seules anomalies de gravité moyenne concernent des erreurs d’encodage ISO‑8859‑1 lues en UTF‑8, qui remplacent les caractères accentués par « � » dans les tables « customers » et « products » ; ce sont les points prioritaires à corriger. Les six problèmes de faible sévérité (valeurs aberrantes, fautes de frappe suspectées et valeurs manquantes) sont secondaires et pourront être traités après la résolution des encodages. Aucun problème critique ou élevé n’a été détecté, ce qui indique que la majorité des données est déjà saine. En résumé, concentrez‑vous d’abord sur la normalisation des encodages, puis passez aux ajustements mineurs d’anomalies.

- Tables : **7** — lignes : **3173**
- Problèmes détectés : **10** 🔴 critical : 0 · 🟠 high : 0 · 🟡 medium : 2 · 🔵 low : 6 · ⚪ info : 2
- Score global de qualité : **96.3 / 100**
- Prêt pour le nettoyage : **oui**

| Table | Score qualité |
|---|---|
| categories | 100.0 |
| customers | 93.0 |
| employees | 100.0 |
| order_details | 96.0 |
| orders | 98.0 |
| products | 91.0 |
| shippers | 100.0 |

## artifacts

- **json_report** : `C:\Users\chihe\Desktop\5eme\ADSP\project_bi_ agents\outputs\profiling\profiling_report.json`
- **markdown_report** : `C:\Users\chihe\Desktop\5eme\ADSP\project_bi_ agents\outputs\profiling\profiling_report.md`
