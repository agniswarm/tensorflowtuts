# Demings Regression https://en.wikipedia.org/wiki/Deming_regression

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
sess = tf.Session()
iris = datasets.load_iris()

# Petal Width
x_vals = np.array([x[3] for x in iris['data']])
# Sepal Length
y_vals = np.array([x[0] for x in iris['data']])

batch_size = 50
learning_rate = 0.1

x_data = tf.placeholder(shape=[None, 1], dtype=tf.float32)
y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)
A = tf.Variable(tf.random_normal(shape=[1, 1]))
b = tf.Variable(tf.random_normal(shape=[1, 1]))
model_output = tf.add(tf.matmul(x_data, A), b)

# Loss Function

numerator = tf.abs(tf.subtract(y_target, tf.add(tf.multiply(x_data, A), b)))
denominator = tf.sqrt(tf.add(tf.square(A), 1))
loss = tf.reduce_mean(tf.truediv(numerator, denominator))

init = tf.global_variables_initializer()
sess.run(init)

loss = tf.reduce_mean(tf.square(y_target-model_output))
my_opt = tf.train.GradientDescentOptimizer(learning_rate)
train_step = my_opt.minimize(loss)
loss_vec = []

for i in range(100):
    rand_index = np.random.choice(len(x_vals), batch_size)
    rand_x = np.transpose([x_vals[rand_index]])
    rand_y = np.transpose([y_vals[rand_index]])
    sess.run(train_step, feed_dict={x_data: rand_x, y_target: rand_y})
    temp_loss = sess.run(loss, feed_dict={x_data: rand_x, y_target: rand_y})
    loss_vec.append(temp_loss)
    if((i+1) % 500 == 0):
        print(
            f"Step # {i+1} A = {sess.run(A)} + b = {sess.run(b)} Loss = {temp_loss}")

[[slope]] = sess.run(A)
[[y_intercept]] = sess.run(b)

best_fit = []
for i in x_vals:
    best_fit.append(slope*i+y_intercept)
plt.plot(x_vals, y_vals, 'o', label="Data Points")
plt.plot(x_vals, best_fit, 'b-', label="Best Fit line", linewidth=3)
plt.legend(loc="upper left")
plt.title("Sepal Length vs Petal Width Deming's Regression")
plt.xlabel("Sepal Length")
plt.ylabel("Petal Width")
plt.show()

plt.plot(loss_vec, 'k-')
plt.title('L2 loss per generation')
plt.xlabel("Generation")
plt.ylabel("Loss")
plt.show()
