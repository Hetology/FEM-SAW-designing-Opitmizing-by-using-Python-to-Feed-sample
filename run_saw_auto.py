import os
import subprocess
import glob
import time
import numpy as np
import pandas as pd
from scipy.stats import qmc
from scipy.signal import find_peaks, peak_widths
from tqdm import tqdm

# ==========================================
# 1. CẤU HÌNH (TỐI GIẢN)
# ==========================================
NUM_SAMPLES = 200
WORK_DIR = os.getcwd()
OUTPUT_CSV = "SAW_AI_Dataset_auto_save.csv"
ANSYS_EXE_PATH = r"C:\Program Files\ANSYS Inc\v150\ansys\bin\winx64\ansys150.exe"
MACRO_FILE = "SAW_main.txt"

# Không gian thiết kế 
bounds_lower = [21, 8, 4000, 100, 340, 62.5]
bounds_upper = [29, 12, 6000, 400, 1340, 81.5]

sampler = qmc.LatinHypercube(d=6, seed=42)
sample_points = sampler.random(n=NUM_SAMPLES)
scaled_samples = qmc.scale(sample_points, bounds_lower, bounds_upper)

if not os.path.exists(OUTPUT_CSV):
    pd.DataFrame(columns=["Case_ID", "numIDT", "d1_um", "D_um", "h1_um", "h3_nm", "E3_GPa", "f0_MHz", "A0", "BW3dB_MHz"]).to_csv(OUTPUT_CSV, index=False)

# ==========================================
# 2. HÀM FFT
# ==========================================
def extract_features_from_vout(filepath):
    try:
        data = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.split()
                # Chỉ lấy những dòng có đúng 2 cột và cột đầu là số (thời gian)
                if len(parts) == 2:
                    try:
                        t_val = float(parts[0])
                        v_val = float(parts[1])
                        data.append([t_val, v_val])
                    except ValueError:
                        continue
        
        if not data: return None, None, None
        
        df = pd.DataFrame(data, columns=["Time", "Volt"])
        t, v = df["Time"].values, df["Volt"].values
        dt = t[1] - t[0]
        N = len(v)
        yf = np.fft.fft(v)
        xf = np.fft.fftfreq(N, dt)[:N//2]
        amp = 2.0/N * np.abs(yf[0:N//2])
        
        valid_idx = np.where((xf >= 60e6) & (xf <= 160e6))[0]
        if len(valid_idx) == 0: return None, None, None
        
        xf_v, amp_v = xf[valid_idx], amp[valid_idx]
        max_idx = np.argmax(amp_v)
        f0, A0 = xf_v[max_idx], amp_v[max_idx]
        
        # Tính Bandwidth 3dB
        widths = peak_widths(amp_v, [max_idx], rel_height=0.293)
        bw = widths[0][0] * (xf_v[1] - xf_v[0])
        
        return f0 / 1e6, A0, bw / 1e6  
    except Exception:
        return None, None, None
# ==========================================
# 3. CHẠY VÒNG LẶP 
# ==========================================
print("\nBẮT ĐẦU CHẠY MÔ PHỎNG :")

with tqdm(total=NUM_SAMPLES, desc="Tiến độ tổng", unit="case") as pbar:
    for i, sample in enumerate(scaled_samples):
        start_time = time.time()
        
        # Diệt các tiến trình cũ để giải phóng file log
        os.system("taskkill /f /im ansys150.exe /t >nul 2>&1")

        # Ghi parameters.txt
        with open("parameters.txt", "w") as f:
            f.write(f"*SET,numIDT,{int(sample[0])}\n*SET,d1,{sample[1]}e-6\n*SET,D,{sample[2]}e-6\n")
            f.write(f"*SET,h1,{sample[3]}e-6\n*SET,h3,{sample[4]}e-9\n*SET,E3,{sample[5]}e9\n")
            f.write("*SET,rho3,6582\n*SET,nu3,0.30\n*SET,L1,2000e-6\n*SET,L2,2000e-6\n")

        pbar.write(f"\n[{i+1}/{NUM_SAMPLES}] Đang chạy...")

        # LỆNH GỌI ANSYS
        ansys_cmd = [ANSYS_EXE_PATH, "-b", "-np", "6", "-i", MACRO_FILE, "-o", "ansys_log.txt"]
        
        subprocess.run(ansys_cmd, cwd=WORK_DIR)

        # Trích xuất kết quả
        vout_path = os.path.join(WORK_DIR, "Vout.txt")
        if os.path.exists(vout_path):
            f0, A0, bw = extract_features_from_vout(vout_path)
            if f0:
                row = [[f"Case_{i+1}", int(sample[0]), sample[1], sample[2], sample[3], sample[4], sample[5], f0, A0, bw]]
                pd.DataFrame(row).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
                pbar.write(f" -> OK! | f0={f0:.2f}MHz")
                os.remove(vout_path)
            
            # Đổi tên file kết quả để lưu trữ 
            if os.path.exists("file.rst"):
                try: os.rename("file.rst", f"SAW_{i+1}.rst")
                except: pass
        else:
            pbar.write(" -> Thất bại! Không thấy Vout.txt")

        pbar.update(1)
