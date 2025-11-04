import pandas as pd

# Check XLSX structure
df_raw = pd.read_excel('data/air+quality/AirQualityUCI.xlsx', nrows=10)

print("="*60)
print("XLSX FILE STRUCTURE")
print("="*60)
print(f"\nShape: {df_raw.shape}")
print(f"\nColumns: {df_raw.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df_raw.head())
print(f"\nData types:")
print(df_raw.dtypes)
print(f"\nDate column sample:")
print(df_raw['Date'].head())
print(f"\nTime column sample:")
print(df_raw['Time'].head())
