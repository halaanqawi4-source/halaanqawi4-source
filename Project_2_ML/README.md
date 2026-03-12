# Project 2 — House Price Prediction

A complete machine learning pipeline built with Python and scikit-learn.

## What it does
Predicts house prices based on area, number of rooms, age, distance to city centre, and other features. Two models are trained and compared — Linear Regression as a baseline, and Random Forest as the main model.

## Files
| File | Description |
|------|-------------|
| `House_Price_Prediction_ML.ipynb` | Full notebook — run this |

## How to run
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
jupyter notebook House_Price_Prediction_ML.ipynb
```

## Pipeline steps
1. Dataset generation (800 synthetic houses with realistic features)
2. Exploratory data analysis — scatter plots, correlation matrix
3. Feature scaling with `StandardScaler`
4. Model training — Linear Regression + Random Forest
5. Evaluation — MAE, RMSE, R² score
6. Visualisation — actual vs. predicted, feature importance

## Results

| Model | R² Score | MAE |
|-------|----------|-----|
| Linear Regression | ~0.88 | ~$20,000 |
| Random Forest | ~0.94 | ~$13,000 |

**Strongest predictor:** `area_sqm`

## Tools
Python · pandas · numpy · matplotlib · seaborn · scikit-learn
