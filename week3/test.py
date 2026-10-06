import sys
import numpy as np
import pandas as pd
import plotnine
import statsmodels.formula.api as smf

from pathlib import Path

from plotnine import (
    ggplot,
    aes,
    after_stat,
    geom_density,
    geom_point,
    geom_histogram,
    geom_boxplot,
    geom_line,
    geom_ribbon,
    stat_smooth,
    stat_density_2d,
    facet_grid,
    facet_wrap,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    scale_fill_cmap,
    coord_fixed,
    coord_cartesian,
    theme,
    theme_gray,
    theme_minimal,
    element_rect,
    element_text,
)

from plotnine.data import penguins as penguins_raw

Path.cwd()
Path("SeoulBikeData.csv").exists()

print("Python:", sys.executable)
print("plotnine:", plotnine.__version__)

data_dir = Path(__file__).parent

bike = pd.read_csv(data_dir / "SeoulBikeData.csv", encoding="cp949")

bike2 = bike.copy()

print("PHẦN 1")
# Thống kê mô tả
print("Thống kê mô tả Rented Bike Count:")
print(bike2['Rented Bike Count'].describe())

plot_histogram = (
    ggplot(bike2, aes(x='Rented Bike Count')) +
    # Lớp 1: Vẽ histogram
    geom_histogram(
        aes(y='..density..'), # Đổi trục y sang mật độ để có thể vẽ đè đường cong lên
        bins=40, 
        fill='#4C72B0',       # Màu nền của cột
        color='black',        # Viền đen cho dễ nhìn
        alpha=0.7             # Độ trong suốt
    ) +
    # Lớp 2: Thêm đường cong mật độ (Density curve)
    geom_density(color='red', size=1) +
    # Lớp 3: Tinh chỉnh giao diện
    theme_minimal() +
    labs(
        title="Phân phối của lượng xe đạp được thuê (Rented Bike Count)",
        x="Số lượng xe đạp thuê (Chiếc)",
        y="Mật độ phân phối (Density)"
    ) +
    theme(
        plot_title=element_text(face='bold', size=14, hjust=0.5),
        axis_title=element_text(face='italic')
    )
)

# Hiển thị biểu đồ
#plot_histogram.draw(show = True)

print("PHẦN 2")

# Tạo biến rain_status
bike2['rain_status'] = np.where(bike2['Rainfall(mm)'] > 0, 'Rain', 'No Rain')
print(bike2.head())

print("PHẦN 3")
# Bảng tóm tắt
summary_2levels = bike2.groupby('rain_status')['Rented Bike Count'].agg(
    ['mean', 'median', 'std', 'min', 'max']
).reset_index()
print("Bảng tóm tắt theo rain_status:")
print(summary_2levels)

# Biểu đồ Boxplot
plot_compare_2 = (
    ggplot(bike2, aes(x='rain_status', y='Rented Bike Count', fill='rain_status')) +
    geom_boxplot(alpha=0.7) +
    theme_minimal() +
    labs(title="So sánh Rented Bike Count giữa Có mưa và Không mưa", x="Trạng thái mưa", y="Số lượng xe đạp thuê")
)
#plot_compare_2.draw(show = True)

print("PHẦN 4")
obs_counts = bike2['rain_status'].value_counts()
print("\nSố lượng quan sát trong từng nhóm:")
print(obs_counts)

print("PHẦN 5")
plot_condition = (
    ggplot(bike2, aes(x='rain_status', y='Rented Bike Count', fill='rain_status')) +
    geom_boxplot(alpha=0.7) +
    facet_wrap('~Seasons') + 
    theme_minimal() +
    labs(title="So sánh Rented Bike Count theo Trạng thái mưa (Tách theo mùa)", 
         x="Trạng thái mưa", y="Số lượng xe thuê")
)

# Ở mức gộp (aggregate), mưa làm giảm rõ rệt lượng thuê. 
# Khi điều kiện hóa theo mùa, bạn thường sẽ thấy mẫu hình này vẫn giữ nguyên 
# (nghĩa là đường trung vị của nhóm Rain luôn thấp hơn No Rain ở mọi mùa). 
# Tuy nhiên, mức độ chênh lệch có thể khác nhau 
# (ví dụ: mùa hè mưa nhiều nhưng nền nhiệt tốt nên lượng thuê khi mưa có thể vẫn cao hơn mùa đông không mưa). 
# Đây là lý do điều kiện hóa giúp tránh Nghịch lý Simpson.

plot_condition.draw(show = True)

#print(bike2)