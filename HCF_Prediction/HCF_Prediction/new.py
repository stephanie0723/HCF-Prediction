import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
import torch.nn as nn

# 设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 读取数据
df = pd.read_excel(r"C:\Users\Administrator\Desktop\HCF.xlsx")

# 特征与标签
features = ['Brinell','YS','UTS','Elongation','C','P','S',
            'y1-fatigue limit 10^6','y2-b1(First Fatigue Strength Exponent)','y3-SRI(Stress Range Intercept, MPa)']

df_x = df[features].values.astype(np.float32)
df_y = df[['target']].values.astype(np.float32)

# 划分训练集
X_train, X_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=42)

# 整理训练集为DataFrame方便筛选
train_df = pd.DataFrame(X_train, columns=features)
train_df['target'] = y_train

# 获取正样本和负样本
X_for_generate = train_df.query("target == 1").iloc[:, :-1].values
X_non_default = train_df.query("target == 0").iloc[:, :-1].values

X_for_generate = torch.tensor(X_for_generate, dtype=torch.float32).to(device)
X_non_default = torch.tensor(X_non_default, dtype=torch.float32).to(device)

n_generate = X_non_default.shape[0] - X_for_generate.shape[0]

BATCH_SIZE = 256
LR_G = 0.0002
LR_D = 0.0002
N_IDEAS = 10  # 噪声向量长度

# 生成器网络
G = nn.Sequential(
    nn.Linear(N_IDEAS, 128),
    nn.ReLU(),
    nn.Linear(128, X_for_generate.shape[1])
).to(device)

# 判别器网络
D = nn.Sequential(
    nn.Linear(X_for_generate.shape[1], 128),
    nn.ReLU(),
    nn.Linear(128, 1),
    nn.Sigmoid()
).to(device)

# 优化器
opt_G = torch.optim.Adam(G.parameters(), lr=LR_G)
opt_D = torch.optim.Adam(D.parameters(), lr=LR_D)

# 损失函数（二分类交叉熵）
criterion = nn.BCELoss()

for step in range(10000):
    # === 训练判别器 ===
    D.zero_grad()
    # 采样真实样本
    idx = torch.randperm(X_for_generate.size(0))[:BATCH_SIZE]
    real_samples = X_for_generate[idx]
    real_labels = torch.ones((real_samples.size(0), 1), device=device)

    # 生成假样本
    noise = torch.randn(BATCH_SIZE, N_IDEAS, device=device)
    fake_samples = G(noise)
    fake_labels = torch.zeros((fake_samples.size(0), 1), device=device)

    # 判别器对真实样本的输出及损失
    output_real = D(real_samples)
    loss_real = criterion(output_real, real_labels)

    # 判别器对假样本的输出及损失
    output_fake = D(fake_samples.detach())
    loss_fake = criterion(output_fake, fake_labels)

    D_loss = loss_real + loss_fake
    D_loss.backward()
    opt_D.step()

    # === 训练生成器 ===
    G.zero_grad()
    noise = torch.randn(BATCH_SIZE, N_IDEAS, device=device)
    generated_samples = G(noise)
    output = D(generated_samples)
    # 生成器希望判别器判为真样本
    G_loss = criterion(output, torch.ones((BATCH_SIZE, 1), device=device))
    G_loss.backward()
    opt_G.step()

    if step % 500 == 0:
        print(f"Step {step:5d} | D_loss: {D_loss.item():.4f} | G_loss: {G_loss.item():.4f}")

# 生成假数据补充正样本
G.eval()
with torch.no_grad():
    noise = torch.randn(n_generate, N_IDEAS, device=device)
    fake_data = G(noise).cpu().numpy()

# 组合数据
X_default = pd.DataFrame(X_for_generate.cpu().numpy(), columns=features)
X_default['target'] = 1

X_fake = pd.DataFrame(fake_data, columns=features)
X_fake['target'] = 1

X_non_default_df = pd.DataFrame(X_non_default.cpu().numpy(), columns=features)
X_non_default_df['target'] = 0

train_data_gan = pd.concat([X_default, X_fake, X_non_default_df], ignore_index=True)

# 保存到Excel
train_data_gan.to_excel(r"C:\Users\Administrator\Desktop\Gan_data_improved2.xlsx", index=False)
