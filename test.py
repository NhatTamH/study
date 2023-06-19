import numpy as np

theta = np.array([-0.34, -0.34, -0.34, 0.04])
np.save('weight.npy', theta)

def predict(x, W, b):
    return x * W + b

def gradient (y_hat, y, x):
    dw = 2 * x * (y_hat-y)
    db = 2* (y_hat-y)
    
    return dw, db

def update_weight(w, b, lr, dw, db):
    w_new = w - lr * dw
    b_new = b - lr * db
    
    return w_new, b_new
print (theta)
