import pandas as pd

# ID dari Google Sheet
sheet_id = "1JDe9Ldrk8IMJZjzhUVDXBA5B-ZptkoI1"

# Link CSV export
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Baca ke DataFrame
df = pd.read_csv(url)

st.write(df.head())  # tampilkan preview data
