"""Agent ETL / Data Engineering de BI Flow (DSO3).

Rôle dans l'architecture : reçoit les tables nettoyées par l'agent Quality & Cleaning,
construit le modèle en étoile (faits + dimensions) et publie :
  - les tables du modèle dans data/gold/ (CSV UTF-8, lus par Power BI / PBIP) ;
  - etl_contract.json : schéma, clés, relations, contrôles (lu par l'agent Semantic & KPI
    et par le Dashboard Generator) ;
  - etl_lineage.json : origine et règle de chaque colonne produite (lu par l'agent BI Auditor / XAI).

Utilisable seul (python etl_agent.py) ou comme nœud LangGraph : etl_node(state) -> dict.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "data" / "raw"
DEFAULT_OUTPUT = ROOT / "data" / "gold"
UNKNOWN_KEY = -1  # membre « Inconnu » de chaque dimension

SOURCES = ["categories", "customers", "employees", "order_details", "orders", "products", "shippers"]


# --------------------------------------------------------------------------- extraction
def read_source(path: Path) -> pd.DataFrame:
    """Lit un CSV en UTF-8, et bascule en Latin-1 si le fichier n'est pas en UTF-8."""
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")


def extract(input_dir: Path) -> dict[str, pd.DataFrame]:
    missing = [s for s in SOURCES if not (input_dir / f"{s}.csv").exists()]
    if missing:
        raise FileNotFoundError(f"Tables manquantes dans {input_dir}: {missing}")
    return {s: read_source(input_dir / f"{s}.csv") for s in SOURCES}


# --------------------------------------------------------------------------- dimensions
def with_surrogate_key(df: pd.DataFrame, key: str, unknown: dict) -> pd.DataFrame:
    df = df.reset_index(drop=True)
    df.insert(0, key, range(1, len(df) + 1))
    unknown_row = pd.DataFrame([{key: UNKNOWN_KEY, **unknown}])
    return pd.concat([unknown_row, df], ignore_index=True)


def build_dim_date(orders: pd.DataFrame) -> pd.DataFrame:
    dates = pd.concat([orders[c] for c in ["order_date", "required_date", "shipped_date"]]).dropna()
    start = pd.Timestamp(dates.min().year, 1, 1)
    end = pd.Timestamp(dates.max().year, 12, 31)
    d = pd.DataFrame({"date": pd.date_range(start, end, freq="D")})
    d.insert(0, "date_key", d["date"].dt.strftime("%Y%m%d").astype(int))
    d["year"] = d["date"].dt.year
    d["quarter"] = "T" + d["date"].dt.quarter.astype(str)
    d["month_number"] = d["date"].dt.month
    d["month_name"] = d["date"].dt.strftime("%B")
    d["year_month"] = d["date"].dt.strftime("%Y-%m")
    d["week_iso"] = d["date"].dt.isocalendar().week.astype(int)
    d["day_of_week"] = d["date"].dt.dayofweek + 1
    d["is_weekend"] = d["day_of_week"] >= 6
    d["date"] = d["date"].dt.date
    unknown = {"date_key": UNKNOWN_KEY, "date": None, "year": 0, "quarter": "Inconnu", "month_number": 0,
               "month_name": "Inconnu", "year_month": "Inconnu", "week_iso": 0, "day_of_week": 0, "is_weekend": False}
    return pd.concat([pd.DataFrame([unknown]), d], ignore_index=True)


def build_dimensions(src: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    customers = src["customers"].rename(columns={
        "customerID": "customer_id", "companyName": "company_name", "contactName": "contact_name",
        "contactTitle": "contact_title"})
    dim_customer = with_surrogate_key(customers, "customer_key", {
        "customer_id": "N/A", "company_name": "Inconnu", "contact_name": "Inconnu",
        "contact_title": "Inconnu", "city": "Inconnu", "country": "Inconnu"})

    products = src["products"].merge(src["categories"], on="categoryID", how="left")
    products = products.rename(columns={
        "productID": "product_id", "productName": "product_name", "quantityPerUnit": "quantity_per_unit",
        "unitPrice": "list_unit_price", "categoryID": "category_id", "categoryName": "category_name",
        "description": "category_description"})
    products["discontinued"] = products["discontinued"].astype(bool)
    products = products[["product_id", "product_name", "quantity_per_unit", "list_unit_price",
                         "discontinued", "category_id", "category_name", "category_description"]]
    dim_product = with_surrogate_key(products, "product_key", {
        "product_id": UNKNOWN_KEY, "product_name": "Inconnu", "quantity_per_unit": "",
        "list_unit_price": 0.0, "discontinued": False, "category_id": UNKNOWN_KEY,
        "category_name": "Inconnu", "category_description": ""})

    emp = src["employees"].rename(columns={
        "employeeID": "employee_id", "employeeName": "employee_name", "reportsTo": "manager_id"})
    names = emp.set_index("employee_id")["employee_name"]
    emp["manager_name"] = emp["manager_id"].map(names).fillna("(aucun)")
    emp["manager_id"] = emp["manager_id"].astype("Int64")
    dim_employee = with_surrogate_key(emp, "employee_key", {
        "employee_id": UNKNOWN_KEY, "employee_name": "Inconnu", "title": "Inconnu", "city": "Inconnu",
        "country": "Inconnu", "manager_id": pd.NA, "manager_name": "(aucun)"})

    shippers = src["shippers"].rename(columns={"shipperID": "shipper_id", "companyName": "shipper_name"})
    dim_shipper = with_surrogate_key(shippers, "shipper_key", {"shipper_id": UNKNOWN_KEY, "shipper_name": "Inconnu"})

    return {"dim_customer": dim_customer, "dim_product": dim_product,
            "dim_employee": dim_employee, "dim_shipper": dim_shipper}


# --------------------------------------------------------------------------- faits
def lookup(values: pd.Series, dim: pd.DataFrame, natural: str, key: str) -> pd.Series:
    mapping = dim[dim[key] != UNKNOWN_KEY].set_index(natural)[key]
    return values.map(mapping).fillna(UNKNOWN_KEY).astype(int)


def date_key(s: pd.Series) -> pd.Series:
    return s.dt.strftime("%Y%m%d").fillna(str(UNKNOWN_KEY)).astype(int)


def build_facts(src: dict[str, pd.DataFrame], dims: dict[str, pd.DataFrame]):
    orders = src["orders"].rename(columns={
        "orderID": "order_id", "customerID": "customer_id", "employeeID": "employee_id",
        "orderDate": "order_date", "requiredDate": "required_date", "shippedDate": "shipped_date",
        "shipperID": "shipper_id"})
    for c in ["order_date", "required_date", "shipped_date"]:
        orders[c] = pd.to_datetime(orders[c], errors="coerce")

    orders["customer_key"] = lookup(orders["customer_id"], dims["dim_customer"], "customer_id", "customer_key")
    orders["employee_key"] = lookup(orders["employee_id"], dims["dim_employee"], "employee_id", "employee_key")
    orders["shipper_key"] = lookup(orders["shipper_id"], dims["dim_shipper"], "shipper_id", "shipper_key")

    lines = src["order_details"].rename(columns={
        "orderID": "order_id", "productID": "product_id", "unitPrice": "unit_price"})
    lines["gross_amount"] = (lines["unit_price"] * lines["quantity"]).round(2)
    lines["discount_amount"] = (lines["gross_amount"] * lines["discount"]).round(2)
    lines["net_amount"] = (lines["gross_amount"] - lines["discount_amount"]).round(2)

    order_net = lines.groupby("order_id")["net_amount"].transform("sum")
    lines = lines.merge(orders, on="order_id", how="left")
    # Le fret est au niveau commande : il est réparti sur les lignes au prorata du montant net.
    share = (lines["net_amount"] / order_net).where(order_net > 0, 1 / lines.groupby("order_id")["order_id"].transform("size"))
    lines["freight_allocated"] = (lines["freight"] * share).round(4)
    lines["product_key"] = lookup(lines["product_id"], dims["dim_product"], "product_id", "product_key")
    lines["order_date_key"] = date_key(lines["order_date"])

    fact_sales = lines[["order_id", "product_id", "order_date_key", "customer_key", "product_key",
                        "employee_key", "shipper_key", "unit_price", "quantity", "discount",
                        "gross_amount", "discount_amount", "net_amount", "freight_allocated"]].copy()
    fact_sales.insert(0, "sales_line_key", range(1, len(fact_sales) + 1))

    agg = src["order_details"].assign(
        net=lambda d: d["unitPrice"] * d["quantity"] * (1 - d["discount"])
    ).groupby("orderID").agg(line_count=("productID", "size"), total_quantity=("quantity", "sum"),
                             order_net_amount=("net", "sum")).reset_index().rename(columns={"orderID": "order_id"})
    fo = orders.merge(agg, on="order_id", how="left")
    fo["order_net_amount"] = fo["order_net_amount"].round(2)
    fo["order_date_key"] = date_key(fo["order_date"])
    fo["required_date_key"] = date_key(fo["required_date"])
    fo["shipped_date_key"] = date_key(fo["shipped_date"])
    fo["is_shipped"] = fo["shipped_date"].notna()
    fo["days_to_ship"] = (fo["shipped_date"] - fo["order_date"]).dt.days.astype("Int64")
    fo["delay_days"] = (fo["shipped_date"] - fo["required_date"]).dt.days.astype("Int64")
    fo["is_late"] = (fo["delay_days"] > 0).fillna(False).astype(bool)
    fact_orders = fo[["order_id", "order_date_key", "required_date_key", "shipped_date_key",
                      "customer_key", "employee_key", "shipper_key", "freight", "line_count",
                      "total_quantity", "order_net_amount", "is_shipped", "days_to_ship",
                      "delay_days", "is_late"]]

    return {"fact_sales": fact_sales, "fact_orders": fact_orders}, orders


# --------------------------------------------------------------------------- contrôles
def run_checks(src, tables) -> list[dict]:
    checks = []

    def add(name, ok, detail, level="KO"):
        checks.append({"check": name, "status": "OK" if ok else level, "detail": detail})

    pks = {"dim_customer": "customer_key", "dim_product": "product_key", "dim_employee": "employee_key",
           "dim_shipper": "shipper_key", "dim_date": "date_key", "fact_sales": "sales_line_key",
           "fact_orders": "order_id"}
    for t, k in pks.items():
        dup = int(tables[t][k].duplicated().sum())
        add(f"pk_unique:{t}.{k}", dup == 0, f"{dup} doublon(s)")

    fs, fo, dd = tables["fact_sales"], tables["fact_orders"], tables["dim_date"]
    add("rows:fact_sales = order_details", len(fs) == len(src["order_details"]),
        f"{len(fs)} vs {len(src['order_details'])}")
    add("rows:fact_orders = orders", len(fo) == len(src["orders"]), f"{len(fo)} vs {len(src['orders'])}")

    for t, cols in {"fact_sales": ["customer_key", "product_key", "employee_key", "shipper_key"],
                    "fact_orders": ["customer_key", "employee_key", "shipper_key"]}.items():
        for c in cols:
            n = int((tables[t][c] == UNKNOWN_KEY).sum())
            add(f"fk_resolved:{t}.{c}", n == 0, f"{n} ligne(s) rattachée(s) au membre Inconnu", level="WARN")

    for t, c in [("fact_sales", "order_date_key"), ("fact_orders", "order_date_key"),
                 ("fact_orders", "required_date_key")]:
        n = int((~tables[t][c].isin(dd["date_key"])).sum())
        add(f"fk_date:{t}.{c}", n == 0, f"{n} date(s) hors dim_date")
    n = int((~fo["shipped_date_key"].isin(dd["date_key"])).sum())
    add("fk_date:fact_orders.shipped_date_key", n == 0,
        f"{n} date(s) hors dim_date ; {int((fo['shipped_date_key'] == UNKNOWN_KEY).sum())} commande(s) non expédiée(s) -> -1")

    od = src["order_details"]
    raw_net = round(float((od["unitPrice"] * od["quantity"] * (1 - od["discount"])).sum()), 2)
    add("reconcile:net_amount", abs(fs["net_amount"].sum() - raw_net) < 1.0,
        f"gold {fs['net_amount'].sum():.2f} vs source {raw_net:.2f}")
    add("reconcile:freight", abs(fs["freight_allocated"].sum() - src["orders"]["freight"].sum()) < 0.5,
        f"alloué {fs['freight_allocated'].sum():.2f} vs source {src['orders']['freight'].sum():.2f}")
    n = int((~fs["discount"].between(0, 1)).sum())
    add("range:discount in [0,1]", n == 0, f"{n} remise(s) hors [0,1]")
    n = int((fs["quantity"] <= 0).sum())
    add("range:quantity > 0", n == 0, f"{n} quantité(s) <= 0")
    return checks


# --------------------------------------------------------------------------- contrat et traçabilité
RELATIONSHIPS = [
    ("dim_date.date_key", "fact_sales.order_date_key", True),
    ("dim_customer.customer_key", "fact_sales.customer_key", True),
    ("dim_product.product_key", "fact_sales.product_key", True),
    ("dim_employee.employee_key", "fact_sales.employee_key", True),
    ("dim_shipper.shipper_key", "fact_sales.shipper_key", True),
    ("dim_date.date_key", "fact_orders.order_date_key", True),
    ("dim_date.date_key", "fact_orders.required_date_key", False),
    ("dim_date.date_key", "fact_orders.shipped_date_key", False),
    ("dim_customer.customer_key", "fact_orders.customer_key", True),
    ("dim_employee.employee_key", "fact_orders.employee_key", True),
    ("dim_shipper.shipper_key", "fact_orders.shipper_key", True),
]

LINEAGE = {
    "fact_sales.gross_amount": ("order_details.unitPrice, order_details.quantity", "unit_price * quantity"),
    "fact_sales.discount_amount": ("order_details.discount", "gross_amount * discount"),
    "fact_sales.net_amount": ("order_details.*", "gross_amount - discount_amount"),
    "fact_sales.freight_allocated": ("orders.freight", "freight de la commande réparti au prorata du net_amount de chaque ligne"),
    "fact_sales.order_date_key": ("orders.orderDate", "jointure orders.orderID, format AAAAMMJJ"),
    "fact_orders.days_to_ship": ("orders.orderDate, orders.shippedDate", "shippedDate - orderDate en jours, vide si non expédiée"),
    "fact_orders.delay_days": ("orders.requiredDate, orders.shippedDate", "shippedDate - requiredDate en jours, > 0 = retard"),
    "fact_orders.is_late": ("orders.requiredDate, orders.shippedDate", "delay_days > 0"),
    "fact_orders.shipped_date_key": ("orders.shippedDate", "AAAAMMJJ, -1 si non expédiée"),
    "fact_orders.order_net_amount": ("order_details.*", "somme des montants nets des lignes"),
    "fact_orders.line_count": ("order_details.productID", "nombre de lignes par commande"),
    "dim_product.category_name": ("categories.categoryName", "jointure products.categoryID"),
    "dim_employee.manager_name": ("employees.employeeName", "auto-jointure sur reportsTo"),
    "*.<dim>_key": ("aucune", "clé de substitution 1..n, -1 = membre Inconnu"),
    "dim_date": ("orders.orderDate/requiredDate/shippedDate", "calendrier continu sur les années couvertes"),
    "encodage": ("customers.csv, products.csv", "lus en Latin-1, écrits en UTF-8 (accents corrigés)"),
}


def rel(path: Path) -> str:
    """Chemin relatif au projet si possible, sinon absolu."""
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(Path(path).resolve())


def pbi_type(dtype) -> str:
    if pd.api.types.is_bool_dtype(dtype):
        return "boolean"
    if pd.api.types.is_integer_dtype(dtype):
        return "int64"
    if pd.api.types.is_float_dtype(dtype):
        return "decimal"
    return "string"


def build_contract(tables, checks, output_dir: Path, run_id: str) -> dict:
    status = "KO" if any(c["status"] == "KO" for c in checks) else ("WARN" if any(c["status"] == "WARN" for c in checks) else "OK")
    return {
        "agent": "etl",
        "version": "1.0",
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "quality_status": status,
        "unknown_member_key": UNKNOWN_KEY,
        "tables": [{
            "name": name,
            "role": "fact" if name.startswith("fact_") else "dimension",
            "path": rel(output_dir / f"{name}.csv"),
            "rows": int(len(df)),
            "columns": [{"name": c, "type": "date" if c == "date" else pbi_type(df[c].dtype)} for c in df.columns],
        } for name, df in tables.items()],
        "relationships": [{"from": a, "to": b, "cardinality": "1:*", "cross_filter": "single", "active": act}
                          for a, b, act in RELATIONSHIPS],
        "checks": checks,
    }


# --------------------------------------------------------------------------- orchestration
def run(input_dir: Path = DEFAULT_INPUT, output_dir: Path = DEFAULT_OUTPUT) -> dict:
    run_id = datetime.now(timezone.utc).strftime("etl_%Y%m%dT%H%M%SZ")
    src = extract(input_dir)
    dims = build_dimensions(src)
    facts, orders = build_facts(src, dims)
    tables = {"dim_date": build_dim_date(orders), **dims, **facts}
    checks = run_checks(src, tables)
    contract = build_contract(tables, checks, output_dir, run_id)

    output_dir.mkdir(parents=True, exist_ok=True)
    if contract["quality_status"] == "KO":
        (output_dir / "etl_contract.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8")
        raise RuntimeError("Contrôles ETL en échec : tables non publiées (voir etl_contract.json)")

    for name, df in tables.items():
        df.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8")
    (output_dir / "etl_contract.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8")
    lineage = {"run_id": run_id, "sources": {s: f"{rel(input_dir)}/{s}.csv" for s in SOURCES},
               "columns": {k: {"source": v[0], "rule": v[1]} for k, v in LINEAGE.items()}}
    (output_dir / "etl_lineage.json").write_text(json.dumps(lineage, indent=2, ensure_ascii=False), encoding="utf-8")
    return contract


def etl_node(state: dict) -> dict:
    """Nœud LangGraph : lit state['clean_data_dir'] (sortie de l'agent Cleaning) et ajoute le contrat ETL."""
    input_dir = Path(state.get("clean_data_dir", DEFAULT_INPUT))
    output_dir = Path(state.get("model_dir", DEFAULT_OUTPUT))
    try:
        contract = run(input_dir, output_dir)
        return {"etl_contract": contract, "model_dir": str(output_dir), "etl_status": contract["quality_status"]}
    except Exception as exc:  # l'orchestrateur décide : relance, validation humaine ou arrêt
        return {"etl_status": "KO", "etl_error": str(exc)}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Agent ETL BI Flow : construit le modèle en étoile")
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    a = p.parse_args()
    c = run(a.input.resolve(), a.output.resolve())
    print(f"Statut qualité : {c['quality_status']}")
    for t in c["tables"]:
        print(f"  {t['name']:<14} {t['rows']:>6} lignes")
    for chk in c["checks"]:
        if chk["status"] != "OK":
            print(f"  [{chk['status']}] {chk['check']} : {chk['detail']}")
