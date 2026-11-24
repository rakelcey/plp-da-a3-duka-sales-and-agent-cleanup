# Duka Sales Exploration and Agent Network Clean-Up

This repository contains the data generation script, exploratory analysis and data-cleaning notebooks, reusable agent cleaning pipeline, and summary deliverables for **Assignment 3: Duka Sales Exploration and Agent Network Clean-Up**.

## Repository Structure

```text
plp-da-a3-duka-sales-and-agent-cleanup/
├── README.md
├── requirements.txt
├── generate_data.py
├── duka_sales_exploration.ipynb
├── cleaning_pipeline.py
├── agent_cleanup.ipynb
├── excel/
│   └── duka_branch_summary.xlsx
└── outputs/
    ├── premium_online_coast_capital.csv
    └── agent_transactions_clean.csv
```

> Note: Raw generated CSV files (`duka_sales.csv`, `agents.csv`, `agent_transactions.csv`) are generated locally/in-session and excluded from version control.

## Setup and Installation

```bash
pip install -r requirements.txt
```

## How to Regenerate Data and Outputs

1. **Generate synthetic datasets (`seed 2026` for Duka sales, `seed 44` for mobile money agent network):**
   ```bash
   python generate_data.py
   ```
2. **Run Duka Electronics half-year sales exploration (`duka_sales_exploration.ipynb`):**
   * Executes first-five-minutes inspection, feature engineering (`month`, `weekday`, `is_weekend`, `price_band`), branch/product/channel/weekday-weekend/month-over-month analyses, and exports `outputs/premium_online_coast_capital.csv` (102 rows) and `excel/duka_branch_summary.xlsx`.
3. **Run Mobile Money Agent Network clean-up (`agent_cleanup.ipynb`):**
   * Uses `clean_agent_data(txns, agents)` from `cleaning_pipeline.py` to audit and clean raw transactions, compute county summaries and weekly pivots, export `outputs/agent_transactions_clean.csv`, and document the six-dimension Data Quality Report.

## Duka Electronics Sales Executive Summary (Jan–Jun 2026)

* **Total Half-Year Performance:** Generated **KES 71,792,500** across **1,000** orders (`duka_sales.csv`, `seed 2026`).
* **Branch Rankings:** **Nairobi** leads with **KES 26,106,100** (376 orders), followed by **Mombasa** (**KES 14,003,700**, 186 orders), **Nakuru** (**KES 11,970,400**, 162 orders), **Kisumu** (**KES 10,868,100**, 159 orders), and **Eldoret** (**KES 8,844,200**, 117 orders).
* **Product Performance:** **Laptop** is the top revenue driver at **KES 41,535,000** (639 units), ahead of **Tablet** (**KES 19,348,000**, 691 units), **Phone** (**KES 8,880,000**, 592 units), **Headphones** (**KES 1,387,500**, 555 units), and **Charger** (**KES 642,000**, 535 units).
* **Sales Channels:** **In-store** generates **KES 40,969,200** (579 orders), **Online** generates **KES 22,786,100** (320 orders), and **Phone order** generates **KES 8,037,200** (101 orders). Filtering for **Premium** orders (`revenue >= 28,000`) placed **Online** in **Nairobi** and **Mombasa** yields **102** records in `outputs/premium_online_coast_capital.csv`.
* **Weekday vs. Weekend & Monthly Trend:** Weekdays generate **KES 51,856,200** across **723** orders compared to **KES 19,936,300** across **277** weekend orders. Monthly revenue peaks in **April 2026** at **KES 13,518,300** (up **+KES 1,121,500** month-over-month from **KES 12,396,800** in March) before easing to **KES 11,415,400** in May (**-KES 2,102,900**) and **KES 10,903,400** in June (**-KES 512,000**).

## Agent Network Cleaning Summary (Seed 44)

* **Row Counts (Before vs. After):** Started with **612** raw transaction rows (`600` base transactions plus `12` duplicated rows), removed **12** duplicate `txn_id` rows (keeping the first occurrence), and retained **600** cleaned transaction rows after merging with the 20-agent register (`agents.csv`).
* **Amount Imputation & Outliers:** Coerced `amount` to numeric, flagged **20** missing/non-numeric entries (`amount_imputed = True`) imputed using `txn_type` medians, and flagged **53** high-value outliers above the `1.5 * IQR` upper fence (`5,513.75`, with `Q1 = 1,105.00` and `Q3 = 2,868.50`).
* **Agent Join & Dates:** Standardized `txn_type` (`Deposit` / `Withdrawal`), retained **7** transactions with unknown agent ID `AG099` as `county = "Unknown"` via left join, and parsed `txn_date` cleanly without `format="mixed"` for weekly reporting.
