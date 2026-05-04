import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor

# Cấu hình hệ thống
DATA_FILE = "SAW_AI_Dataset_auto_save.csv"
FEATURES = ["numIDT", "d1_um", "D_um", "h1_um", "h3_nm", "E3_GPa"]
TARGETS = ["f0_MHz", "A0", "BW3dB_MHz"]
MODEL_PATH = Path("trained_models")
MODEL_PATH.mkdir(exist_ok=True)

def train_best_surrogates():
    if not Path(DATA_FILE).exists():
        print(f"Lỗi: Không tìm thấy file {DATA_FILE}")
        return

    df = pd.read_csv(DATA_FILE)
    X = df[FEATURES].values
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    report = []

    for target in TARGETS:
        y = df[target].values
        print(f"\n>>> Đang tối ưu hóa mô hình cho: {target}")

        # Danh sách ứng viên tinh gọn (Bỏ NeuralNet/SVR do hiệu quả thấp trên 200 mẫu)
        candidates = {
            "RandomForest": RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42),
            "XGBoost": XGBRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=1000),
            "Ridge_Poly2": Pipeline([
                ("poly", PolynomialFeatures(degree=2)),
                ("scaler", StandardScaler()),
                ("model", Ridge(alpha=1.0))
            ])
        }

        best_r2 = -np.inf
        best_model = None
        best_name = ""

        for name, model in candidates.items():
            # Đánh giá bằng Cross-Validation 5-Fold
            y_pred = cross_val_predict(model, X, y, cv=kf)
            r2 = r2_score(y, y_pred)
            mae = mean_absolute_error(y, y_pred)
            
            print(f"  - {name:15} | R2: {r2:7.4f} | MAE: {mae:.6f}")

            if r2 > best_r2:
                best_r2 = r2
                best_model = model
                best_name = name

        # Huấn luyện mô hình tốt nhất trên toàn bộ Dataset và lưu lại
        print(f"  => CHỌN: {best_name} (R2={best_r2:.4f})")
        best_model.fit(X, y)
        joblib.dump(best_model, MODEL_PATH / f"best_model_{target}.pkl")
        report.append({"Target": target, "Model": best_name, "R2": best_r2})

    print("\n" + "="*30)
    print("BÁO CÁO TỔNG KẾT SURROGATE")
    print(pd.DataFrame(report).to_string(index=False))
    print("="*30)

if __name__ == "__main__":
    train_best_surrogates()