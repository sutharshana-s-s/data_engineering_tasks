# Data Engineering Tasks

## Task 1: Revenue Tracker

Maps monthly revenue data from source Excel to output template by month abbreviation.
- **Tech**: Python, openpyxl, pandas

Consolidates multi-month MIS files (Apr/May/Jun) into single output with revenue per project.
- **Tech**: Python, openpyxl, pandas

## Task 2: CLI Data Processing Tool
Interactive CLI for data operations: `ingest` (metadata), `validate` (quality checks), `transform` (clean & export).
- **Tech**: Python, argparse, pandas

## Task 3: Book Data Ingestion Pipeline
Reads multi-file JSON book data, adds page metadata, transforms for analysis.
- **Tech**: Python, JSON processing

## Task 4: E-Commerce Data Processing
PySpark pipeline for 21 Shein CSVs: dynamic loading, standardization, price/discount transforms, schema-aligned merging, deduplication.
- **Tech**: PySpark, Databricks

## Task 5: SQL/T-SQL Practice
Queries covering joins, aggregations, subqueries, window functions, date operations on programmer/studies/software schema.
- **Tech**: SQL Server

## Task 6: SuperStore Sales Analytics
End-to-end analysis of orders: schema inference, null/duplicate checks, sales metrics, regional trends, visualizations.
- **Tech**: PySpark, Plotly, Delta Lake

## Task 7: Weather Data Platform 
Full-stack weather analytics with medallion architecture and dashboard.

**Pipeline**: APIs (Open-Meteo + NASA Power) → Bronze (raw JSON) → Silver (typed tables) → Gold (aggregations)
- Coverage: 10 cities, 2020-2024

**Dashboard**: Streamlit app with filters, KPIs, gauges, trend charts, regional comparisons
- Deployed on Databricks Apps

**Tech**: PySpark, Streamlit, Plotly, REST APIs