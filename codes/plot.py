import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd

def plot_linegraph(x, y1, y2, xlabel, ylabel, title):
    fig = plt.figure(figsize=(5, 5))
    plt.plot(x, y1, color='red', marker='o', markersize=4, linewidth=1.5, label='TTv2')
    plt.plot(x, y2, color='green', marker='o', markersize=4, linewidth=1.5, label='TTv3')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(-1, 1)
    plt.xticks(np.arange(-1.0, 1.01, 0.5))
    plt.grid(True)
    plt.legend()
    return fig

def plot_distribution(x, y1, y2, xlabel, ylabel, title):
    data1 = pd.DataFrame(y1)
    data2 = pd.DataFrame(y2)
    num_features = len(x)
    positions = np.arange(num_features)

    fig, ax = plt.subplots(figsize=(12, 5))

    # te_2: 왼쪽으로
    vp1 = ax.violinplot(
        [data1.iloc[:, i].dropna() for i in range(num_features)],
        positions=positions - 0.2,
        widths=0.35,
        showmedians=True
    )

    # te_3: 오른쪽으로
    vp2 = ax.violinplot(
        [data2.iloc[:, i].dropna() for i in range(num_features)],
        positions=positions + 0.2,
        widths=0.35,
        showmedians=True
    )

    # 스타일 커스터마이징 함수
    def set_violin_style(vp, face_color, edge_color='black'):
        for b in vp['bodies']:
            b.set_facecolor(face_color)
            b.set_edgecolor(edge_color)
            b.set_linewidth(1.2)
            b.set_alpha(0.7)
        for partname in ['cbars', 'cmins', 'cmaxes', 'cmedians']:
            if partname in vp:
                vp[partname].set_edgecolor(edge_color)
                vp[partname].set_linewidth(1.0)

    # 스타일 적용
    set_violin_style(vp1, 'red')  # red
    set_violin_style(vp2, 'green')  # green

    # X축 라벨
    ax.set_xticks(positions)
    ax.set_xticklabels(x, fontsize=10)

    # 축 라벨과 타이틀
    ax.set_title("Target Error Distribution vs Offset (Violin Plot)", fontsize=16, pad=15)
    ax.set_ylabel("Target error (%)", fontsize=12)
    ax.set_xlabel("Offset", fontsize=12)
    ax.set_xlim(-0.5, num_features - 0.5)
    # 축 스타일 조정
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', labelsize=10)

    # 그리드 추가
    ax.yaxis.grid(True, linestyle='--')
    ax.xaxis.grid(False)

    # 범례 (선 스타일)
    ax.plot([], c='red', label='TTv2', linewidth=8)
    ax.plot([], c='green', label='TTv3', linewidth=8)
    ax.legend(fontsize=12).get_frame().set_edgecolor('none')

    plt.tight_layout()
    return fig