from pathlib import Path
import numpy as np
import pandas as pd


def generate_duka_sales(seed: int = 2026, n_rows: int = 1000) -> pd.DataFrame:
  """Generate synthetic Duka Electronics half-year sales data."""
  rng = np.random.default_rng(seed)
  products = {
      "Phone": 15000,
      "Laptop": 65000,
      "Headphones": 2500,
      "Tablet": 28000,
      "Charger": 1200,
  }

  df = pd.DataFrame({
      "order_id": range(1001, 1001 + n_rows),
      "order_date": pd.to_datetime("2026-01-01")
      + pd.to_timedelta(rng.integers(0, 180, n_rows), unit="D"),
      "branch": rng.choice(
          ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"],
          n_rows,
          p=[0.40, 0.20, 0.15, 0.15, 0.10],
      ),
      "product": rng.choice(list(products.keys()), n_rows),
      "quantity": rng.integers(1, 6, n_rows),
      "channel": rng.choice(
          ["In-store", "Online", "Phone order"], n_rows, p=[0.55, 0.35, 0.10]
      ),
  })
  df["unit_price"] = df["product"].map(products)
  df["revenue"] = df["quantity"] * df["unit_price"]
  return df


def generate_agent_data(
    seed: int = 44, n_txns: int = 600
) -> tuple[pd.DataFrame, pd.DataFrame]:
  """Generate synthetic mobile money agent register and raw transactions with injected issues."""
  rng = np.random.default_rng(seed)

  agents = pd.DataFrame({
      "agent_id": [f"AG{i:03d}" for i in range(1, 21)],
      "county": rng.choice(
          ["Nairobi", "Kiambu", "Nakuru", "Mombasa", "Kisumu"], 20
      ),
      "onboarded": pd.date_range("2024-01-01", periods=20, freq="MS").strftime(
          "%Y-%m-%d"
      ),
  })

  txns = pd.DataFrame({
      "txn_id": [f"TX{i:05d}" for i in range(1, n_txns + 1)],
      "agent_id": rng.choice(agents["agent_id"], n_txns),
      "txn_type": rng.choice(
          ["Deposit", "withdrawal", "DEPOSIT ", "Withdrawal", "deposit"], n_txns
      ),
      "amount": rng.lognormal(7.5, 0.8, n_txns).round(0).astype(str),
      "txn_date": (
          pd.to_datetime("2026-03-01")
          + pd.to_timedelta(rng.integers(0, 60, n_txns), unit="D")
      ).strftime("%Y-%m-%d"),
  })

  # Inject missing values, string 'N/A', high value, and slash-delimited dates
  idx = rng.choice(n_txns, 30, replace=False)
  txns.loc[idx[:15], "amount"] = np.nan
  txns.loc[idx[15:20], "amount"] = "N/A"
  txns.loc[idx[20:25], "amount"] = "250000"
  txns.loc[idx[25:], "txn_date"] = txns.loc[idx[25:], "txn_date"].str.replace(
      "-", "/"
  )

  # Inject duplicate transactions and unknown agent IDs
  txns = pd.concat([txns, txns.sample(12, random_state=1)], ignore_index=True)
  txns.loc[rng.choice(len(txns), 8, replace=False), "agent_id"] = "AG099"

  return agents, txns


def main() -> None:
  Path("outputs").mkdir(exist_ok=True)
  Path("excel").mkdir(exist_ok=True)

  duka_sales = generate_duka_sales(seed=2026, n_rows=1000)
  agents, agent_txns = generate_agent_data(seed=44, n_txns=600)

  duka_sales.to_csv("duka_sales.csv", index=False)
  agents.to_csv("agents.csv", index=False)
  agent_txns.to_csv("agent_transactions.csv", index=False)
  print("Generated duka_sales.csv, agents.csv, and agent_transactions.csv.")


if __name__ == "__main__":
  main()
