import pandas as pd


def clean_agent_data(
    txns: pd.DataFrame, agents: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:
  """Clean raw agent transactions and enrich with agent county details."""
  df = txns.copy()
  before_rows = len(df)

  # 1. Remove duplicate txn_id rows (keep first)
  dup_mask = df.duplicated(subset=["txn_id"], keep="first")
  duplicates_removed = int(dup_mask.sum())
  df = df[~dup_mask].copy()

  # 2. Standardise txn_type to 'Deposit' or 'Withdrawal'
  df["txn_type"] = df["txn_type"].astype(str).str.strip().str.title()

  # 3. Convert amount to numeric, flag imputed values, and impute by txn_type median
  raw_numeric = pd.to_numeric(df["amount"], errors="coerce")
  df["amount_imputed"] = raw_numeric.isna()
  amount_imputed_count = int(df["amount_imputed"].sum())
  df["amount"] = raw_numeric

  type_medians = df.groupby("txn_type")["amount"].median()
  overall_median = float(df["amount"].median())
  df["amount"] = (
      df["amount"]
      .fillna(df["txn_type"].map(type_medians))
      .fillna(overall_median)
  )

  # 4. Parse txn_date into datetime64[ns]
  df["txn_date"] = pd.to_datetime(
      df["txn_date"], format="mixed", errors="coerce"
  )

  # 5. Flag outliers using 1.5 * IQR
  q1 = float(df["amount"].quantile(0.25))
  q3 = float(df["amount"].quantile(0.75))
  iqr = q3 - q1
  lower_fence = q1 - 1.5 * iqr
  upper_fence = q3 + 1.5 * iqr
  df["is_outlier"] = (df["amount"] < lower_fence) | (df["amount"] > upper_fence)

  # 6. Merge with agents on agent_id
  unknown_agent_txns = int((~df["agent_id"].isin(agents["agent_id"])).sum())
  clean_df = df.merge(
      agents[["agent_id", "county"]].drop_duplicates(subset=["agent_id"]),
      on="agent_id",
      how="left",
  )
  clean_df["county"] = clean_df["county"].fillna("Unknown")

  log = {
      "rows_before": before_rows,
      "duplicates_removed": duplicates_removed,
      "rows_after": len(clean_df),
      "amount_imputed_count": amount_imputed_count,
      "iqr_q1": round(q1, 2),
      "iqr_q3": round(q3, 2),
      "iqr_upper_fence": round(upper_fence, 2),
      "outliers_flagged": int(df["is_outlier"].sum()),
      "rows_at_250000": int((df["amount"] == 250000).sum()),
      "unknown_agent_txns": unknown_agent_txns,
  }
  return clean_df, log
