import streamlit as st
import os
from PIL import Image
import base64
import matplotlib.pyplot as plt
import numpy as np
import h5py
st.set_page_config(layout="wide")
# ---------------------------
# 1) 파라미터 후보 리스트 정의
# ---------------------------
learning_rate_list = [0.01, 0.025, 0.05]
transfer_rate_list2 = [0.01, 0.025, 0.05]  # Algo2용 tr2
transfer_rate_list3 = [0.05, 0.1, 0.3]     # Algo3용 tr3
alpha_list = [0.001, 0.005, 0.01]           # 예시에 맞춰 오름차순 정렬
offset_list = [-0.9, -0.6, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.6, 0.9]
chopper_period_list = [5000, 10000, 15000]
target_value = 0.8  # target_list = [0.8] 만 있으므로 고정

# ---------------------------
# 2) Streamlit 사이드바에서 사용자 선택
# ---------------------------
st.sidebar.subheader("Device")
selected_alpha = st.sidebar.selectbox("Alpha", alpha_list)
st.sidebar.image(f'plot_img\\alpha_{selected_alpha}\\deviceplot.png', use_container_width =True)

st.sidebar.markdown("---")  
st.sidebar.subheader("TTv2")
selected_lr2 = st.sidebar.selectbox("Learning Rate of tt2", learning_rate_list, key="learning_rate_2")
selected_tr2 = st.sidebar.selectbox("transfer_rate2", transfer_rate_list2)

st.sidebar.markdown("---")
st.sidebar.subheader("TTv3")
selected_lr3 = st.sidebar.selectbox("Learning Rate of tt3", learning_rate_list, key="learning_rate_3")
selected_tr3 = st.sidebar.selectbox("transfer_rate3", transfer_rate_list3)
selected_cp = st.sidebar.selectbox("Chopper Period", chopper_period_list)

# ---------------------------   
# 3) 디렉토리 / 파일명 생성 함수
# ---------------------------
def get_algo2_filepath(lr, tr2, alpha, offset, target=0.8):
    alpha_str = str(alpha)
    lr_str = str(lr)
    tr2_str = str(tr2)
    offset_str = str(offset)
    target_str = str(target)
    directory = os.path.join("plot_img", f"alpha_{alpha_str}")
    filename = f"{lr_str}_{tr2_str}_{alpha_str}_2_{offset_str}_{target_str}.png"
    return os.path.join(directory, filename)

def get_algo3_filepath(lr, tr3, alpha, cp, offset, target=0.8):
    alpha_str = str(alpha)
    lr_str = str(lr)
    tr3_str = str(tr3)
    cp_str = str(cp)
    offset_str = str(offset)
    target_str = str(target)
    directory = os.path.join("plot_img", f"alpha_{alpha_str}")
    filename = f"{lr_str}_{tr3_str}_{alpha_str}_{cp_str}_{offset_str}_{target_str}.png"
    return os.path.join(directory, filename)



MSE_2_means=[]
MSE_3_means=[]
te_2_means=[]
te_3_means=[]
with h5py.File(f"./data/{target_value}_{selected_alpha}_{selected_lr2}_{selected_tr2}_2.h5", 'r') as h5f:
    for grp_key in offset_list:
        grp = h5f[str(grp_key)]
        MSE_2_means.append(grp.attrs['MSE_mean'])
        te_2_means.append(grp.attrs['te_mean'])
with h5py.File(f"./data/{target_value}_{selected_alpha}_{selected_lr3}_{selected_tr3}_{selected_cp}.h5", 'r') as h5f:
    for grp_key in offset_list:
        grp = h5f[str(grp_key)]
        MSE_3_means.append(grp.attrs['MSE_mean'])
        te_3_means.append(grp.attrs['te_mean'])
fig1 = plt.figure(figsize=(5, 5))
plt.plot(offset_list, MSE_2_means, color='red', marker='o', markersize=4, linewidth=1.5, label='TTv2')
plt.plot(offset_list, MSE_3_means, color='green', marker='o', markersize=4, linewidth=1.5, label='TTv3')
plt.xlabel('Offset')
plt.ylabel('MSE')
plt.title('MSE')
plt.xlim(-1, 1)
plt.xticks(np.arange(-1.0, 1.01, 0.5))
plt.grid(True)
plt.legend()

fig2 = plt.figure(figsize=(5, 5))
plt.plot(offset_list, te_2_means, color='red', marker='o', markersize=4, linewidth=1.5, label='TTv2')
plt.plot(offset_list, te_3_means, color='green', marker='o', markersize=4, linewidth=1.5, label='TTv3')
plt.xlabel('Offset')
plt.ylabel('Target error(%)')
plt.title('Target error vs Offset')
plt.xlim(-1, 1)
plt.xticks(np.arange(-1.0, 1.01, 0.5))
plt.grid(True)
plt.legend()

st.title(f"TTv2 vs TTv3 : alpha = {selected_alpha}")
col1, col2,_ = st.columns(3)
with col1:
    st.pyplot(fig1, use_container_width=True)
with col2:
    st.pyplot(fig2, use_container_width=True)
# ---------------------------
# 4) 이미지 파일을 Base64 인코딩하는 함수
# ---------------------------
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return encoded
    return None

# ---------------------------
# 5) CSS로 가로 스크롤 컨테이너 구성
# ---------------------------
st.markdown(
    """<style>
    .scroll-container { display: flex; flex-wrap: nowrap; overflow-x: auto; padding-bottom: 1rem;}
    .scroll-item {flex: 0 0 auto;margin-right: 1rem;}
    </style>""",    unsafe_allow_html=True)

# ---------------------------
# 6) 화면 구성 (Algo2 / Algo3 영역)
# ---------------------------
img_width = 300  # 이미지 표시 폭 (px)

st.subheader(f"ttv2, learning rate: {selected_lr2}, transfer rate: {selected_tr2}")
combined_container = '<div class="scroll-container">'
for offset in offset_list:
    combined_container += '<div class="scroll-item" style="text-align: center;">'
    
    # Algo2 이미지
    file_path_2 = get_algo2_filepath(selected_lr2, selected_tr2, selected_alpha, offset, target_value)
    img_b64_2 = get_image_base64(file_path_2)
    if img_b64_2:
        combined_container += f'<small>offset={offset}</small><br><img src="data:image/png;base64,{img_b64_2}" width="{img_width}">'
    else:
        combined_container += f'<div style="width:{img_width}px;">Algo2<br>offset={offset}<br>[파일 없음]</div>'
    
    combined_container += '<br>'  # Algo2와 Algo3 사이에 여백
    # Algo3 이미지
    file_path_3 = get_algo3_filepath(selected_lr3, selected_tr3, selected_alpha, selected_cp, offset, target_value)
    img_b64_3 = get_image_base64(file_path_3)
    if img_b64_3:
        combined_container += f'<img src="data:image/png;base64,{img_b64_3}" width="{img_width}"><br><small>offset={offset}</small>'
    else:
        combined_container += f'<div style="width:{img_width}px;">Algo3<br>offset={offset}<br>[파일 없음]</div>'
    
    combined_container += '</div>'
combined_container += '</div>'

st.markdown(combined_container, unsafe_allow_html=True)
st.subheader(f"ttv3, learning rate: {selected_lr3}, transfer rate: {selected_tr3}, chopper period: {selected_cp}")
