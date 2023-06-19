import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt 

theta = np.array([-0.34, -0.34, -0.34, 0.04])
np.save('weight.npy', theta)

loaded_theta = np.load('weight.npy')
# print(loaded_theta)

data = np.genfromtxt('Real_estate.csv', delimiter=',')
data = data[1:]
data_size = data.shape[0]
# print(data_size)

X = data[:, 0:-1]
y = data[:, -1]
# print(X)
# filename = 'output.csv'

# Ghi dữ liệu vào tệp CSV
# import csv
# with open(filename, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(X)


scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)
# print(X_scaled)

# forward 
def predict(x, theta):
  x = np.array(x)
  return x.dot(theta)


# compute gradient 
def gradient(y_hat, y, x):
  dtheta = 2 * x * (y_hat-y)

  return dtheta

# update weights 
def update_weight(theta, lr, dthetas, m):
  theta_new = theta - (lr*dthetas)/m

  return theta_new

data_concat = np.c_[X_scaled, np.ones((data_size, 1))]
# print(data_concat)


# khởi tạo trọng số 
theta1 = np.array([-0.34, -0.34, -0.34, 0.04])
# theta = np.array([-0.34, -0.34, -0.34, 1, 1, 1, 1, 0.04])

theta = np.insert(theta1, -1, [1, 1, 1, 1])
# print(theta)

lr = 0.01 
epochs = 100 # số lần lặp data
m = 2 # mini-batch size 
min_loss = float('inf')

list_loss = []
for epoch in range(epochs):
  for j in range(0, data_size, m):
    sum_loss = 0
    dthetas = 0
    for i in range(j, j+m):
      # lấy 1 sample (1 điểm dữ liệu)
      x_i = data_concat[i]
      y_i = y[i]

      # dự đoán y_hat
      y_hat = predict(x_i, theta)
      
      # tính toán độ lỗi 
      loss = (y_hat-y_i)*(y_hat-y_i)
      sum_loss += loss

      # tính đạo hàm 
      dtheta = gradient(y_hat, y_i, x_i)
      dthetas += dtheta

      # Lưu trọng số theta nếu có lỗi nhỏ nhất mới được tìm thấy
      if loss < min_loss:
          min_loss = loss
          np.savetxt('best_theta.txt', theta)
      
    # cập nhật trọng số 
    theta = update_weight(theta, lr, dthetas, m)
    list_loss.append(sum_loss/m) 
  
  # print("[INFO] Epoch {}: theta: {}".format(epoch, theta))
  
plt.plot(list_loss)
plt.xlabel('iter')
plt.ylabel('loss')
plt.show()

best_theta = np.loadtxt('best_theta.txt')
for sample in theta:
   x = sample
   y_hat = predict(x,best_theta)
   print(y_hat)