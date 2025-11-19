# Air Pollution Forecasting — COMP9417 Group Project

## 1. Overview
This repository contains the full end-to-end pipeline for short‑term air‑pollution forecasting using the UCI Air Quality dataset (2004–2005).  
The project includes:
- Preprocessing & temporal train/test split  
- Consensus-based anomaly detection  
- Hourly / daily / merged feature engineering  
- Regression & classification forecasting experiments (four horizons: 1, 6, 12, 24 hours)  
- Complete outputs for reproducibility

All experiments are implemented in modular Jupyter notebooks.

---

## 2. Project Structure

```
.
├── README.md
├── requirements.txt                     # Python dependencies
│
├── notebooks/                           # Main executable pipeline notebooks
│   ├── 1_EDA.ipynb
│   ├── 2_Preprocessing_TemporalDataSplitting.ipynb
│   ├── 3_AnomalyDetection.ipynb
│   ├── 4_FeatureEngineering.ipynb
│   ├── 5_Regression_Model.ipynb
│   └── 6_Classification_Model.ipynb
│
├── data_orig/                           # Raw UCI dataset + initial diagnosis
│   ├── data/air+quality/
│   │   ├── AirQualityUCI.csv
│   │   └── AirQualityUCI.xlsx
│   └── check_xlsx.py
│
├── output_Preprocessing_TemporalDataSplitting/
│   ├── train_2004.csv
│   ├── test_2005.csv
│   ├── preprocessed_data.csv
│   └── Preprocessing_Summary.png
│
├── output_AnomalyDetection/
│   ├── train_2004_anomaly_flag.csv
│   ├── train_2004_cleaned.csv
│   ├── train_2004_removed.csv
│   ├── Anomaly_Detail.csv
│   ├── Anomaly_Summary.csv
│   └── Anomaly_Analysis.png
│
├── output_FeatureEngineering/           # Hourly/Daily/Merged features
│   ├── fe_train_test_summary.csv
│   ├── test/
│   │   ├── test_2005_fe_daily.csv
│   │   ├── test_2005_fe_hourly.csv
│   │   └── test_2005_fe_merge.csv
│   └── train/
│       ├── orig/
│       └── cleaned/
│
├── results_cls/                         # Classification experiments
│   ├── analysis/
│   ├── figs/
│   └── summary_full_run_*.csv
│
└── results_reg/                         # Regression experiments
    ├── analysis/
    ├── figs/
    └── summary_full_run_*.csv
```

---

## 3. Installation

### 3.1 Create environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 4. Running the Pipeline

Run the notebooks in the following order:

### **Step 1 – EDA**
`notebooks/1_EDA.ipynb`  
Produces temporal plots, pollutant distributions, correlations.

### **Step 2 – Preprocessing & temporal split**
`notebooks/2_Preprocessing_TemporalDataSplitting.ipynb`  
Outputs:
- `train_2004.csv`
- `test_2005.csv`
- `preprocessed_data.csv`
- `Preprocessing_Summary.png`

### **Step 3 – Anomaly detection**
`notebooks/3_AnomalyDetection.ipynb`  
Outputs:
- Cleaned training set  
- Anomaly flags  
- Anomaly analysis figure  

### **Step 4 – Feature engineering**
`notebooks/4_FeatureEngineering.ipynb`  
Generates hourly, daily, merged features (orig & cleaned).

### **Step 5 – Regression models**
`notebooks/5_Regression_Model.ipynb`  
Outputs:
- RMSE performance summary  
- Model comparison plots  
- Time‑series and residual plots  

### **Step 6 – Classification models**
`notebooks/6_Classification_Model.ipynb`  
Outputs:
- Accuracy / F1 / Recall summary  
- Confusion matrices for all models × FE types × horizons  

---

## 5. Output Locations

### **Preprocessing**
`output_Preprocessing_TemporalDataSplitting/`

### **Anomaly detection**
`output_AnomalyDetection/`

### **Feature engineering**
`output_FeatureEngineering/`  
- `train/orig/`  
- `train/cleaned/`  
- `test/`

### **Classification results**
`results_cls/analysis/` – CSV metrics  
`results_cls/figs/` – CM + RQ1–RQ4 plots  

### **Regression results**
`results_reg/analysis/` – CSV metrics  
`results_reg/figs/` – RMSE/RQ plots + residuals + time-series

---

## 6. Requirements

A minimal environment compatible with all notebooks is provided in `requirements.txt`:

```
numpy
pandas
matplotlib
scikit-learn
xgboost
seaborn
```

---

## 7. Notes
- All splits are strictly chronological (no leakage between 2004/2005).
- Anomaly detection is applied **only** to training data.
- Both regression and classification tasks follow identical experimental setups.

---

## 8. License
This project is for educational use in **UNSW COMP9417**.
