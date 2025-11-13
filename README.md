# COMP9417 Air Quality Forecasting Project

## Project Structure

```
COMP9417_Project/
├── README.md
├── proj_Main.ipynb                         # Main end-to-end project notebook
├── proj_Requirements.pdf                   # Project specification (given by course)
│
├── data_orig/                              # Original data & missing-value diagnosis
│   ├── data/
│   │   └── air+quality/                    # Raw UCI Air Quality dataset (.csv/.xlsx)
│   ├── check_xlsx.py                       # Utility script for checking raw Excel
│   ├── diagnosis_figures/                  # Missing-value visualisations
│   │   └── missing_pattern_analysis.png
│   └── missing_value_diagnosis.py          # Missing-value diagnosis pipeline
│
├── output_Preprocessing_TemporalDataSplitting/   # Preprocessing & temporal split
│   ├── train_2004.csv
│   ├── test_2005.csv
│   ├── preprocessed_data_normalized.csv
│   ├── preprocessed_data_unnormalized.csv
│   ├── scaler.pkl
│   └── preprocessing_summary.png
│
├── output_AnomalyDetection/                # Anomaly detection outputs
│   ├── train_2004_anomaly_flag.csv
│   ├── train_2004_cleaned.csv
│   ├── train_2004_removed_anomalies.csv
│   ├── anomaly_detection_detailed_results.csv
│   ├── anomaly_summary_statistics.csv
│   └── anomaly_analysis_train_2004.png
│
├── output_FeatureEngineering/              # Feature-engineered train/test sets
│   ├── train_2004_fe_daily_[orig/cleaned].csv
│   ├── train_2004_fe_hourly_[orig/cleaned].csv
│   ├── train_2004_fe_merge_[orig/cleaned].csv
│   ├── test_2005_fe_daily.csv
│   ├── test_2005_fe_hourly.csv
│   ├── test_2005_fe_merge.csv
│   └── fe_train_test_summary.csv
│
├── output_EDA/                             # Exploratory data analysis figures
│   ├── temporal_patterns.png
│   ├── correlation_heatmap.png
│   └── pollutant_distributions.png
│
├── results_cls/                            # Classification experiments (RQ1–RQ4)
│   ├── analysis/                           # Aggregated metrics by research question
│   │   ├── rq1_model_comparison.csv
│   │   ├── rq2_anomaly_effect.csv
│   │   ├── rq3_fe_effect.csv
│   │   └── rq4_horizon_effect.csv
│   │
│   ├── figs/                               # Confusion matrices & summary plots
│   │   ├── cm_LogReg_FE-daily_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_LogReg_FE-hourly_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_LogReg_FE-merge_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_RF_FE-daily_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_RF_FE-hourly_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_RF_FE-merge_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_XGB_FE-daily_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_XGB_FE-hourly_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_XGB_FE-merge_[orig/cleaned]_[h1/h6/h12/h24].png
│   │   ├── cm_naive_[h1/h6/h12/h24].png
│   │   ├── rq1_model_comparison.png
│   │   ├── rq2_cleaning_uplift_by_fe.png
│   │   ├── rq3_fe_effect_heatmap.png
│   │   └── rq4_perf_vs_horizon.png
│   │   # (Individual confusion-matrix images are grouped with [...] above)
│   │
│   └── summary_full_run_20251113_161730.csv    # Full metrics log for final run
│
└── exp_pipeline_md/
    └── cls_pipeline.md                     # Text description of classification pipeline
```
