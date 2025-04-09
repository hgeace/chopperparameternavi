import streamlit as st
import os
from PIL import Image
import base64
import matplotlib.pyplot as plt
import numpy as np
import h5py
from plot import plot_linegraph, plot_distribution
st.set_page_config(layout="wide")
# ---------------------------
# 파라미터 후보 리스트 정의
# ---------------------------
learning_rate_list = [0.01, 0.025, 0.05]
transfer_rate_list2 = [0.01, 0.025, 0.05]  # Algo2용 tr2
transfer_rate_list3 = [0.05, 0.1, 0.3]     # Algo3용 tr3
alpha_list = [0.001, 0.005, 0.01]           # 예시에 맞춰 오름차순 정렬
offset_list = [-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
chopper_period_list = [5000, 10000, 15000]
target_value = 0.8  # target_list = [0.8] 만 있으므로 고정

# ---------------------------
# Streamlit 사이드바에서 사용자 선택
st.sidebar.subheader("Device")
selected_alpha = st.sidebar.selectbox("Alpha", alpha_list)
st.sidebar.image(f'./plot_img/alpha_{selected_alpha}_deviceplot.png', use_container_width =True)

st.sidebar.markdown("---")  
st.sidebar.subheader("TTv2")
selected_lr2 = st.sidebar.selectbox("Learning Rate of tt2", learning_rate_list, key="learning_rate_2")
selected_tr2 = st.sidebar.selectbox("Transfer Rate of tt2", transfer_rate_list2)

st.sidebar.markdown("---")
st.sidebar.subheader("TTv3")
selected_lr3 = st.sidebar.selectbox("Learning Rate of tt3", learning_rate_list, key="learning_rate_3")
selected_tr3 = st.sidebar.selectbox("Transfer Rate of tt3", transfer_rate_list3)
selected_cp = st.sidebar.selectbox("Chopper Period", chopper_period_list)
# ---------------------------

# ---------------------------
# 에러 plot 영역
MSE_2_means=[]
MSE_3_means=[]
te_2_means=[]
te_3_means=[]
te_2 = []
te_3 = []

with h5py.File(f"./data/{target_value}_{selected_alpha}_{selected_lr2}_{selected_tr2}_2.h5", 'r') as h5f:
    for grp_key in offset_list:
        grp = h5f[str(grp_key)]
        MSE_2_means.append(grp.attrs['MSE_mean'])
        te_2_means.append(grp.attrs['te_mean'])
        te_2.append(grp['te_list'][:])
with h5py.File(f"./data/{target_value}_{selected_alpha}_{selected_lr3}_{selected_tr3}_{selected_cp}.h5", 'r') as h5f:
    for grp_key in offset_list:
        grp = h5f[str(grp_key)]
        MSE_3_means.append(grp.attrs['MSE_mean'])
        te_3_means.append(grp.attrs['te_mean'])
        te_3.append(grp['te_list'][:])
        
fig_MSE = plot_linegraph(offset_list, MSE_2_means, MSE_3_means, 'Offset', 'MSE', 'MSE vs Offset')
fig_te = plot_linegraph(offset_list, te_2_means, te_3_means, 'Offset', 'Target error(%)', 'Target error vs Offset')
fig_teabs = plot_linegraph(offset_list, np.abs(te_2_means), np.abs(te_3_means), 'Offset', 'Target error(%)', 'Target error vs Offset (abs)')
# fig_te_dist = plot_distribution(offset_list, te_2, te_3, "_",  "_",  "_")
# 꼴을 보니까 뭔가 df로 잘못 변환되고있거나 데이터를 잘못 불러오고있는듯.
# 지금은 시간이 없으니까 이따가 할것.

st.title(f"TTv2 vs TTv3 : alpha = {selected_alpha}")
col1, col2, col3 = st.columns(3)
with col1:
    st.pyplot(fig_MSE, use_container_width=True)
with col2:
    st.pyplot(fig_te, use_container_width=True)
with col3:
    st.pyplot(fig_teabs, use_container_width=True)
# with st.expander("Target Error distribution"):
#     st.write("여기에 내용이 들어갑니다.")
#     st.pyplot(fig_te_dist, use_container_width=True)
# ---------------------------

# ---------------------------
# 이미지영역 함수 정의
def get_image_base64(file_path): #이미지 파일을 Base64 인코딩하는 함수
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return encoded
    return None
st.markdown( # CSS로 가로 스크롤 컨테이너 구성
    """<style>
    .scroll-container { display: flex; flex-wrap: nowrap; overflow-x: auto; padding-bottom: 1rem;}
    .scroll-item {flex: 0 0 auto;margin-right: 1rem;}
    </style>""",    unsafe_allow_html=True)
# ---------------------------

st.subheader(f"ttv2, learning rate: {selected_lr2}, transfer rate: {selected_tr2}")

# ---------------------------
# 이미지영역
img_width = 300  # 이미지 표시 폭 (px)
combined_container = '<div class="scroll-container">'
for offset in offset_list:
    combined_container += '<div class="scroll-item" style="text-align: center;">'
    # Algo2 이미지
    file_path_2 = f"./plot_img/{target_value}_{selected_alpha}_{selected_lr2}_{selected_tr2}_2_{offset}.png"# get_algo2_filepath(selected_lr2, selected_tr2, selected_alpha, offset, target_value)
    img_b64_2 = get_image_base64(file_path_2)
    if img_b64_2:
        combined_container += f'<small>offset={offset}</small><br><img src="data:image/png;base64,{img_b64_2}" width="{img_width}">'
    else:
        combined_container += f'<div style="width:{img_width}px;">Algo2<br>offset={offset}<br>[파일 없음]</div>'
    combined_container += '<br>'  # Algo2와 Algo3 사이에 여백
    # Algo3 이미지plot_img/{target}_{alpha}_{lr}_{tr3}_{cp}_{offset}
    file_path_3 = f"./plot_img/{target_value}_{selected_alpha}_{selected_lr3}_{selected_tr3}_{selected_cp}_{offset}.png" #get_algo3_filepath(selected_lr3, selected_tr3, selected_alpha, selected_cp, offset, target_value)
    img_b64_3 = get_image_base64(file_path_3)
    if img_b64_3:
        combined_container += f'<img src="data:image/png;base64,{img_b64_3}" width="{img_width}"><br><small>offset={offset}</small>'
    else:
        combined_container += f'<div style="width:{img_width}px;">Algo3<br>offset={offset}<br>[파일 없음]</div>'
    combined_container += '</div>'
combined_container += '</div>'
# ---------------------------

st.markdown(combined_container, unsafe_allow_html=True)
st.subheader(f"ttv3, learning rate: {selected_lr3}, transfer rate: {selected_tr3}, chopper period: {selected_cp}")
