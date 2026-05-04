import joblib
import numpy as np
import random
from scipy.optimize import minimize

# Cấu hình (Phải khớp hoàn toàn với FEATURES lúc train)
FEATURES = ["numIDT", "d1_um", "D_um", "h1_um", "h3_nm", "E3_GPa"]
TARGETS = ["f0_MHz", "A0", "BW3dB_MHz"]
BOUNDS = [(21, 29), (8, 12), (4000, 6000), (100, 400), (340, 1340), (62.5, 81.5)]

class InverseDesigner:
    def __init__(self):
        self.models = {}
        for t in TARGETS:
            try:
                # Lưu ý: Nếu fen đã thêm biến vật lý h/lambda vào file train, 
                # thì phải cập nhật FEATURES và logic tiền xử lý ở đây nhé!
                self.models[t] = joblib.load(f"trained_models/best_model_{t}.pkl")
            except FileNotFoundError:
                print(f"Lỗi: Thiếu model cho {t}")
        print("--- Hệ thống sẵn sàng  ---")

    def solve(self, t_f0, t_a0, t_bw, weights=(1.0, 1.2, 0.05), n_trials=10):
        """
        n_trials: Số lần thử xuất phát tại các điểm ngẫu nhiên khác nhau.
        Giúp AI không bị kẹt tại x0 ban đầu.
        """
        w_f, w_a, w_b = weights
        best_overall_res = None
        min_overall_loss = np.inf

        def objective(x):
            x_in = x.reshape(1, -1)
            p_f0 = self.models["f0_MHz"].predict(x_in)[0]
            p_a0 = self.models["A0"].predict(x_in)[0]
            p_bw = self.models["BW3dB_MHz"].predict(x_in)[0]
            
            # Loss function chuẩn hóa
            err_f = w_f * ((p_f0 - t_f0) / t_f0) ** 2
            err_a = w_a * ((p_a0 - t_a0) / t_a0) ** 2
            err_b = w_b * ((p_bw - t_bw) / t_bw) ** 2
            
            return err_f + err_a + err_b

        print(f"Đang thử {n_trials} kịch bản...")

        for i in range(n_trials):
            # Tạo điểm khởi đầu ngẫu nhiên trong khoảng BOUNDS
            x_random = [random.uniform(b[0], b[1]) for b in BOUNDS]
            
            # Sử dụng SLSQP để tối ưu hóa linh hoạt hơn L-BFGS-B
            res = minimize(objective, x_random, bounds=BOUNDS, method='SLSQP')
            
            if res.success and res.fun < min_overall_loss:
                min_overall_loss = res.fun
                best_overall_res = res

        if best_overall_res is None:
            return None, None

        return dict(zip(FEATURES, best_overall_res.x)), np.sqrt(min_overall_loss)

if __name__ == "__main__":
    designer = InverseDesigner()
    
    f_req = float(input("Nhập f0 mong muốn (MHz): "))
    a_req = float(input("Nhập A0 mong muốn: "))
    bw_req = float(input("Nhập BW mong muốn (MHz): "))
    
    # Chạy tối ưu hóa đa điểm khởi đầu
    design, error = designer.solve(f_req, a_req, bw_req)
    
    if design:
        print("\n" + "="*40)
        print("KẾT QUẢ THIẾT KẾ TỐI ƯU (Đã thoát bẫy x0)")
        print(f"Sai số tổng hợp: {error:.8f}")
        print("-"*40)
        for k, v in design.items():
            print(f"  {k:10}: {v:.4f}")
        print("="*40)
        print("Lưu ý: Hãy nạp bộ số này vào ANSYS để kiểm chứng thực tế!")
    else:
        print("Không tìm thấy lời giải phù hợp.")