// Requêtes Power Query M générées par l'agent ETL (une par table).
// Créer d'abord un paramètre texte GoldFolder = chemin du dossier data\gold\ (terminé par \).

// ---- dim_date
dim_date = let
    Source = Csv.Document(File.Contents(GoldFolder & "dim_date.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"date_key", Int64.Type}, {"date", type date}, {"year", Int64.Type}, {"quarter", type text}, {"month_number", Int64.Type}, {"month_name", type text}, {"year_month", type text}, {"week_iso", Int64.Type}, {"day_of_week", Int64.Type}, {"is_weekend", type logical}}, "en-US")
in
    Types;

// ---- dim_customer
dim_customer = let
    Source = Csv.Document(File.Contents(GoldFolder & "dim_customer.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"customer_key", Int64.Type}, {"customer_id", type text}, {"company_name", type text}, {"contact_name", type text}, {"contact_title", type text}, {"city", type text}, {"country", type text}}, "en-US")
in
    Types;

// ---- dim_product
dim_product = let
    Source = Csv.Document(File.Contents(GoldFolder & "dim_product.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"product_key", Int64.Type}, {"product_id", Int64.Type}, {"product_name", type text}, {"quantity_per_unit", type text}, {"list_unit_price", type number}, {"discontinued", type logical}, {"category_id", Int64.Type}, {"category_name", type text}, {"category_description", type text}}, "en-US")
in
    Types;

// ---- dim_employee
dim_employee = let
    Source = Csv.Document(File.Contents(GoldFolder & "dim_employee.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"employee_key", Int64.Type}, {"employee_id", Int64.Type}, {"employee_name", type text}, {"title", type text}, {"city", type text}, {"country", type text}, {"manager_id", type text}, {"manager_name", type text}}, "en-US")
in
    Types;

// ---- dim_shipper
dim_shipper = let
    Source = Csv.Document(File.Contents(GoldFolder & "dim_shipper.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"shipper_key", Int64.Type}, {"shipper_id", Int64.Type}, {"shipper_name", type text}}, "en-US")
in
    Types;

// ---- fact_sales
fact_sales = let
    Source = Csv.Document(File.Contents(GoldFolder & "fact_sales.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"sales_line_key", Int64.Type}, {"order_id", Int64.Type}, {"product_id", Int64.Type}, {"order_date_key", Int64.Type}, {"customer_key", Int64.Type}, {"product_key", Int64.Type}, {"employee_key", Int64.Type}, {"shipper_key", Int64.Type}, {"unit_price", type number}, {"quantity", Int64.Type}, {"discount", type number}, {"gross_amount", type number}, {"discount_amount", type number}, {"net_amount", type number}, {"freight_allocated", type number}}, "en-US")
in
    Types;

// ---- fact_orders
fact_orders = let
    Source = Csv.Document(File.Contents(GoldFolder & "fact_orders.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"order_id", Int64.Type}, {"order_date_key", Int64.Type}, {"required_date_key", Int64.Type}, {"shipped_date_key", Int64.Type}, {"customer_key", Int64.Type}, {"employee_key", Int64.Type}, {"shipper_key", Int64.Type}, {"freight", type number}, {"line_count", Int64.Type}, {"total_quantity", Int64.Type}, {"order_net_amount", type number}, {"is_shipped", type logical}, {"days_to_ship", Int64.Type}, {"delay_days", Int64.Type}, {"is_late", type logical}}, "en-US")
in
    Types;
