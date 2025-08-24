import pandas as pd

# ID file Google Sheets kamu
sheet_id = "1JDe9Ldrk8IMJZjzhUVDXBA5B-ZptkoI1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

df = pd.read_csv(url)
st = "\n".join(df.columns.tolist())
print("Kolom di sheet kamu:\n" + st)
