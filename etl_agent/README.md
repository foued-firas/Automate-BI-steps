# Agent ETL / Data Engineering (BI Flow, DSO3)

Aligné sur le rapport *BI Flow — Multi-Agent Automation of the Power BI Pipeline* (ch. 5 et 8).

## Place dans l'architecture

```
Data Profiler -> Quality & Cleaning -> [ETL / Data Eng.] -> Semantic & KPI -> BI Analyst -> Dashboard Generator -> BI Auditor / XAI
                                            ^  orchestrateur LangGraph : etl_node(state)
```

| | |
|---|---|
| Objectif | BO2 « Améliorer la qualité des données » via DSO3 « Transformation & ETL » |
| Remplace dans Power BI | Data modeling (schéma en étoile) |
| Entrée | tables nettoyées : `state["clean_data_dir"]` (par défaut `data/raw/`) |
| Sortie | `data/gold/*.csv`, `etl_contract.json`, `etl_lineage.json` |
| Test (rapport §6.1) | le script tourne sans erreur et les contrôles sont OK |
| Stack | Python, pandas ; nœud compatible LangGraph |

## Modèle en étoile produit

Le dataset fourni est de type Northwind (commandes B2B, clients dans 21 pays, 3 transporteurs), et non des déclarations douanières. Le modèle couvre donc BO3 (performance commerciale), BO4 (rentabilité client) et BO5 (logistique).

| Table | Grain | Lignes | Contenu clé |
|---|---|---|---|
| `fact_sales` | ligne de commande | 2 155 | quantité, prix, remise, montant brut / remise / net, fret réparti |
| `fact_orders` | commande | 830 | fret, nb lignes, montant net, délai d'expédition, retard, expédiée ou non |
| `dim_date` | jour (2013 à 2015) | 1 096 | année, trimestre, mois, semaine ISO, week-end |
| `dim_customer` | client | 92 | société, ville, pays |
| `dim_product` | produit | 78 | nom, prix catalogue, arrêté, catégorie (dénormalisée) |
| `dim_employee` | commercial | 10 | nom, titre, pays, manager |
| `dim_shipper` | transporteur | 4 | nom |

Chaque dimension a une clé de substitution `<dim>_key` et un membre « Inconnu » (clé -1).
Relations 1:* à filtrage simple ; `fact_orders.required_date_key` et `shipped_date_key` sont des relations inactives (à activer avec `USERELATIONSHIP` côté DAX).

## Règles appliquées

- Encodage : `customers.csv` et `products.csv` sont en Latin-1, réécrits en UTF-8 (ex. « Taquería »).
- `net_amount = unit_price × quantity × (1 − discount)`.
- Le fret (niveau commande) est réparti sur les lignes au prorata du montant net, pour la rentabilité par client ou produit.
- 21 commandes non expédiées : `shipped_date_key = -1`, `days_to_ship` et `delay_days` vides.
- `is_late = shippedDate > requiredDate` (37 commandes en retard).

## Contrôles qualité (bloquants si KO)

Unicité des clés, nombre de lignes conservé, intégrité référentielle faits vers dimensions, rapprochement du montant net et du fret avec la source, plages de remise et quantité. Dernier passage : **OK** (net 1 265 793,02 vs source 1 265 793,04, écart d'arrondi ; fret 64 942,69 = source).

## Interfaces avec les autres agents

- **Semantic & KPI** lit `etl_contract.json` (`tables`, `columns`, `relationships`) pour créer le modèle PBIP et les mesures DAX.
- **Dashboard Generator** lit les noms de colonnes du contrat.
- **BI Auditor / XAI** lit `etl_lineage.json` : source et règle de chaque colonne calculée.
- **Orchestrateur** lit `etl_status` (`OK`, `WARN`, `KO`) ; en cas de KO, les tables ne sont pas publiées.

## Utilisation

```bash
python etl_agent.py                        # data/raw -> data/gold
python etl_agent.py --input <dossier_nettoyé> --output <dossier_modèle>
```

```python
from etl_agent import etl_node
graph.add_node("etl", etl_node)   # LangGraph
```

## Chargement dans Power BI

`powerquery/load_gold.pq` contient une requête M par table ; il suffit de régler le paramètre `GoldFolder`.
