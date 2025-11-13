import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
output_dir = 'diagnosis_figures'
os.makedirs(output_dir, exist_ok=True)

# Load data
try:
    df = pd.read_excel('data/air+quality/AirQualityUCI.xlsx')
    print("Data source: AirQualityUCI.xlsx")
except:
    df = pd.read_csv('data/air+quality/AirQualityUCI.csv', sep=';', decimal=',')
    print("Data source: AirQualityUCI.csv")

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Merge temporal fields
# Handle both CSV (string) and XLSX (datetime + time string) formats
if df['Date'].dtype == 'object':
    # CSV format: both are strings
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'],
                                    format='%d/%m/%Y %H.%M.%S',
                                    errors='coerce')
else:
    # XLSX format: Date is datetime, Time needs conversion to string
    df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

df = df.dropna(subset=['DateTime'])
df = df.set_index('DateTime').sort_index()
df = df.drop(['Date', 'Time'], axis=1)

# Replace -200 with NaN
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    df[col] = df[col].replace(-200.0, np.nan)

print("\n" + "=" * 70)
print("MISSING VALUE DIAGNOSIS REPORT")
print("=" * 70)

# ============================================
# 1. OVERALL MISSING STATISTICS
# ============================================
print("\n[1] OVERALL MISSING VALUE STATISTICS")
print("-" * 70)

pollutants = ['CO(GT)', 'NMHC(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
sensors = ['PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S3(NOx)', 'PT08.S4(NO2)', 'PT08.S5(O3)']
meteo = ['T', 'RH', 'AH']
all_features = pollutants + sensors + meteo

missing_stats = pd.DataFrame({
    'Missing_Count': df[all_features].isnull().sum(),
    'Missing_Pct': (df[all_features].isnull().sum() / len(df) * 100).round(2),
    'Present_Count': df[all_features].notnull().sum()
})
missing_stats = missing_stats.sort_values('Missing_Pct', ascending=False)
print(missing_stats)

# ============================================
# 2. TEMPORAL PATTERN OF MISSING VALUES
# ============================================
print("\n[2] TEMPORAL DISTRIBUTION OF MISSING VALUES")
print("-" * 70)

# Check if missing values are concentrated in specific time periods
df['Year'] = df.index.year
df['Month'] = df.index.month
df['Hour'] = df.index.hour

for feature in pollutants:
    monthly_missing = df.groupby(['Year', 'Month'])[feature].apply(lambda x: x.isnull().sum())
    if monthly_missing.sum() > 0:
        print(f"\n{feature} - Missing by Month:")
        print(monthly_missing[monthly_missing > 0].head(10))

# ============================================
# 3. CONSECUTIVE MISSING PATTERNS
# ============================================
print("\n[3] CONSECUTIVE MISSING VALUE ANALYSIS")
print("-" * 70)


def find_consecutive_gaps(series):
    """Find consecutive missing value gaps"""
    is_missing = series.isnull()
    gaps = []
    gap_start = None

    for idx, missing in enumerate(is_missing):
        if missing and gap_start is None:
            gap_start = idx
        elif not missing and gap_start is not None:
            gaps.append(idx - gap_start)
            gap_start = None

    if gap_start is not None:
        gaps.append(len(is_missing) - gap_start)

    return gaps


for feature in pollutants:
    gaps = find_consecutive_gaps(df[feature])
    if gaps:
        gaps = np.array(gaps)
        print(f"\n{feature}:")
        print(f"  Total gaps: {len(gaps)}")
        print(f"  Max consecutive missing: {gaps.max()} hours")
        print(f"  Mean gap length: {gaps.mean():.1f} hours")
        print(f"  Median gap length: {np.median(gaps):.1f} hours")
        print(f"  Gaps > 24 hours: {(gaps > 24).sum()}")
        print(f"  Gaps > 168 hours (1 week): {(gaps > 168).sum()}")

# ============================================
# 4. CORRELATION OF MISSING VALUES
# ============================================
print("\n[4] CO-OCCURRENCE OF MISSING VALUES")
print("-" * 70)

# Check if features are missing together
missing_matrix = df[all_features].isnull().astype(int)
missing_corr = missing_matrix.corr()

print("\nFeatures with highly correlated missing patterns (|r| > 0.8):")
high_corr_pairs = []
for i in range(len(missing_corr.columns)):
    for j in range(i + 1, len(missing_corr.columns)):
        if abs(missing_corr.iloc[i, j]) > 0.8:
            high_corr_pairs.append((
                missing_corr.columns[i],
                missing_corr.columns[j],
                missing_corr.iloc[i, j]
            ))

for feat1, feat2, corr in high_corr_pairs:
    print(f"  {feat1} <-> {feat2}: {corr:.3f}")

# ============================================
# 5. MISSING VALUE VISUALIZATION
# ============================================
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
fig.suptitle('Missing Value Pattern Analysis', fontsize=16, y=0.995)

# Timeline of missing values
for feature in pollutants:
    missing_indicator = df[feature].isnull().astype(int)
    axes[0].plot(df.index, missing_indicator.cumsum(),
                 label=feature.split('(')[0], linewidth=2, alpha=0.7)
axes[0].set_ylabel('Cumulative Missing Count')
axes[0].set_title('Cumulative Missing Values Over Time')
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

# Heatmap of missing values over time (sample)
sample_size = min(2000, len(df))
sample_df = df[all_features].iloc[:sample_size]
missing_heatmap = sample_df.isnull().astype(int).T
axes[1].imshow(missing_heatmap, cmap='RdYlGn_r', aspect='auto', interpolation='nearest')
axes[1].set_yticks(range(len(all_features)))
axes[1].set_yticklabels([f.split('(')[0] for f in all_features], fontsize=8)
axes[1].set_xlabel('Time Index (first 2000 observations)')
axes[1].set_title('Missing Value Heatmap (Red = Missing)')

# Missing value correlation heatmap
sns.heatmap(missing_corr, annot=False, cmap='coolwarm', center=0,
            vmin=-1, vmax=1, ax=axes[2], cbar_kws={'label': 'Correlation'})
axes[2].set_title('Co-occurrence Pattern of Missing Values')
axes[2].set_xticklabels([f.split('(')[0] for f in all_features], rotation=45, ha='right', fontsize=8)
axes[2].set_yticklabels([f.split('(')[0] for f in all_features], rotation=0, fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'missing_pattern_analysis.png'),
            dpi=300, bbox_inches='tight')
print(f"\n[SAVED] {output_dir}/missing_pattern_analysis.png")

# ============================================
# 6. FEATURE AVAILABILITY ANALYSIS
# ============================================
print("\n[6] FEATURE AVAILABILITY FOR MODELING")
print("-" * 70)

# Calculate how many complete cases we have
complete_cases = df[all_features].notnull().all(axis=1).sum()
print(
    f"\nComplete cases (no missing in any feature): {complete_cases} / {len(df)} ({complete_cases / len(df) * 100:.1f}%)")

# Check availability for each pollutant individually
print("\nAvailability by pollutant (with all sensors and meteo):")
for pollutant in pollutants:
    features_needed = [pollutant] + sensors + meteo
    available = df[features_needed].notnull().all(axis=1).sum()
    print(f"  {pollutant}: {available} / {len(df)} ({available / len(df) * 100:.1f}%)")

# ============================================
# 7. INTERPOLATION FEASIBILITY
# ============================================
print("\n[7] INTERPOLATION FEASIBILITY ASSESSMENT")
print("-" * 70)

for feature in pollutants:
    series = df[feature]
    total_missing = series.isnull().sum()

    if total_missing > 0:
        # Check if data is suitable for linear interpolation
        gaps = find_consecutive_gaps(series)
        short_gaps = sum(1 for g in gaps if g <= 3)  # gaps <= 3 hours
        medium_gaps = sum(1 for g in gaps if 3 < g <= 24)
        long_gaps = sum(1 for g in gaps if g > 24)

        print(f"\n{feature}:")
        print(f"  Short gaps (≤3h): {short_gaps} - EXCELLENT for linear interpolation")
        print(f"  Medium gaps (4-24h): {medium_gaps} - GOOD for time-based interpolation")
        print(f"  Long gaps (>24h): {long_gaps} - REQUIRES forward fill or deletion")

        # Calculate data density
        density = (len(series) - total_missing) / len(series)
        print(f"  Data density: {density * 100:.1f}%")

        if density > 0.95:
            print(f"  ✓ RECOMMENDATION: Linear/Time interpolation suitable")
        elif density > 0.80:
            print(f"  ⚠ RECOMMENDATION: Combine interpolation + forward fill")
        else:
            print(f"  ✗ RECOMMENDATION: Consider dropping feature or extensive imputation")

# ============================================
# SUMMARY AND RECOMMENDATIONS
# ============================================
print("\n" + "=" * 70)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 70)
print(f"\nDiagnosis complete. Check '{output_dir}/' for visualizations.")