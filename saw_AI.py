import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.optimize import minimize

# Cấu hình dữ liệu mới (6 Features)
DATA_FILE = SAW_AI_Dataset_auto_save.csv
FEATURES = [numIDT, d1_um, D_um, h1_um, h3_nm, E3_GPa]
TARGETS = [f0_MHz, A0, BW3dB_MHz]

# Giới hạn vật lý để AI không tìm ra các thông số phi thực tế
BOUNDS = [
    (21, 29),    # numIDT
    (8, 12),     # d1_um
    (4000, 6000),# D_um
    (100, 400),  # h1_um
    (340, 1340), # h3_nm
    (62.5, 81.5) # E3_GPa
]

class SAW_Expert_System
    def __init__(self)
        self.models = {}
        self.best_model_name = {t None for t in TARGETS}

    def train(self, df)
        X = df[FEATURES].values
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        
        results = []
        for target in TARGETS
            y = df[target].values
            
            # Định nghĩa 3 ứng viên
            candidates = {
                Ridge_Poly2 Pipeline([
                    (poly, PolynomialFeatures(degree=2)),
                    (scaler, StandardScaler()),
                    (model, Ridge(alpha=1.0))
                ]),
                RandomForest RandomForestRegressor(n_estimators=200, random_state=42)
            }
            
            best_r2 = -np.inf
            for name, model in candidates.items()
                # Cross-validation để đánh giá
                y_pred = cross_val_predict(model, X, y, cv=kf)
                r2 = r2_score(y, y_pred)
                mae = mean_absolute_error(y, y_pred)
                results.append({Target target, Model name, R2 r2, MAE mae})
                
                # Lưu model tốt nhất để dùng cho Inverse Design
                if r2  best_r2
                    best_r2 = r2
                    self.best_model_name[target] = name
                    model.fit(X, y) # Train trên toàn bộ data
                    self.models[target] = model
                    
        return pd.DataFrame(results)

    def inverse_design(self, target_f0, target_bw=None)
        
        Tìm thông số thiết kế (X) để đạt được f0 mong muốn
        
        def objective(x)
            x = x.reshape(1, -1)
            pred_f0 = self.models[f0_MHz].predict(x)[0]
            score = (pred_f0 - target_f0)2
            if target_bw
                pred_bw = self.models[BW3dB_MHz].predict(x)[0]
                score += (pred_bw - target_bw)2
            return score

        # Điểm bắt đầu (giữa dải)
        x0 = [25, 10, 5000, 200, 800, 72]
        res = minimize(objective, x0, bounds=BOUNDS, method='L-BFGS-B')
        
        return dict(zip(FEATURES, res.x)), res.fun

# ==========================================
# CHƯƠNG TRÌNH CHÍNH
# ==========================================
if __name__ == __main__
    if not Path(DATA_FILE).exists()
        print(fLỗi Không tìm thấy file {DATA_FILE}. Hãy chạy mô phỏng ANSYS trước!)
    else
        df = pd.read_csv(DATA_FILE)
        expert = SAW_Expert_System()
        
        print(--- Đang huấn luyện Forward Models (5-Fold CV) ---)
        metrics = expert.train(df)
        print(metrics.to_string(index=False))
        
        print(n--- Chức năng Inverse Design (Thiết kế ngược) ---)
        target_val = 105.5 # Ví dụ fen muốn thiết kế sensor chạy ở 105.5 MHz
        design, error = expert.inverse_design(target_val)
        
        print(fMục tiêu {target_val} MHz)
        print(Thông số AI đề xuất)
        for k, v in design.items()
            print(f  {k} {v.4f})
        print(fSai số dự đoán {np.sqrt(error).4f} MHz)