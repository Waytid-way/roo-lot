# Model Selection Report

## Comparison of Algorithms

The following regression algorithms were evaluated using GridSearchCV with 5-fold cross-validation:

| Model | Test R2 | Test MAE | Test RMSE | Best Params |
|-------|---------|----------|-----------|-------------|
| Lasso | 0.9923 | 43.63 | 58.41 | {'alpha': 0.1} |
| Ridge | 0.9923 | 43.61 | 58.45 | {'alpha': 0.1} |
| LinearRegression | 0.9923 | 43.67 | 58.45 | {} |
| ElasticNet | 0.9922 | 43.94 | 58.86 | {'alpha': 0.1, 'l1_ratio': 0.9} |
| RandomForest | 0.9728 | 85.73 | 109.59 | {'max_depth': 10, 'n_estimators': 100} |

*Note: Results are sorted by Test R2 Score.*

## Selected Model: Lasso Regression

**Justification:**
1. **Performance:** Lasso achieved the highest R2 score (0.9923) and lowest RMSE (58.41).
2. **Interpretability:** As a linear model, it provides clear feature coefficients, making it easy to explain to users which factors (AC usage, etc.) drive their bill.
3. **Simplicity:** It is much faster and lighter than ensemble methods like RandomForest, which is ideal for deployment on Streamlit Cloud.
4. **Regularization:** Lasso includes L1 regularization, which helps prevent overfitting and performs feature selection by shrinking less important coefficients towards zero.

## Performance Analysis on Test Set

- **R2 Score:** 0.9923 (The model explains 99.23% of the variance in electricity bills).
- **MAE:** 43.63 Baht (On average, the prediction is off by about 44 Baht).
- **RMSE:** 58.41 Baht (Root Mean Squared Error).

## Conclusion

The **Lasso Regression** model with `alpha=0.1` is recommended for production. It offers the best balance of accuracy, interpretability, and efficiency.
