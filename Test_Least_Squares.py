import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Step 1: Generate sample data
np.random.seed(1)
X = np.linspace(0, 10, 10)
Y = np.linspace(0, 10, 10)
X, Y = np.meshgrid(X, Y)
Z = 2 * X**2 + 3 * Y + 5 + np.random.randn(*X.shape) * 10  # Polynomial function with noise

# Flatten the arrays for regression
X_flat = X.flatten()
Y_flat = Y.flatten()
Z_flat = Z.flatten()

# Step 2: Perform polynomial regression
degree = 2
poly = PolynomialFeatures(degree)
X_poly = poly.fit_transform(np.vstack((X_flat, Y_flat)).T)
model = LinearRegression()
model.fit(X_poly, Z_flat)

# Create a grid for the fitted surface
X_fit = np.linspace(0, 10, 100)
Y_fit = np.linspace(0, 10, 100)
X_fit, Y_fit = np.meshgrid(X_fit, Y_fit)
X_poly_fit = poly.transform(np.vstack((X_fit.flatten(), Y_fit.flatten())).T)
Z_fit = model.predict(X_poly_fit).reshape(X_fit.shape)

# Step 3: Plot the results
fig = plt.figure(figsize=(12, 6))

# Original data points
ax = fig.add_subplot(121, projection='3d')
ax.scatter(X, Y, Z, label='Data points', color='blue')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Original Data Points')

# Fitted polynomial surface
ax = fig.add_subplot(122, projection='3d')
ax.plot_surface(X_fit, Y_fit, Z_fit, color='red', alpha=0.5, label='Fitted polynomial')
ax.scatter(X, Y, Z, color='blue')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Fitted Polynomial Surface')

plt.show()


###################################################

# import numpy as np
# import matplotlib.pyplot as plt

# # Step 1: Generate sample data
# np.random.seed(0)
# x = np.linspace(0, 10, 50)
# y = 2 * x**2 + 3 * x + 5 + np.random.randn(50) * 10  # Quadratic function with noise

# # Step 2: Perform polynomial regression (degree 2)
# degree = 5
# coefficients = np.polyfit(x, y, degree)

# # Generate polynomial function from coefficients
# polynomial = np.poly1d(coefficients)

# # Step 3: Plot the results
# plt.scatter(x, y, label='Data points', color='blue')
# x_fit = np.linspace(0, 10, 100)
# y_fit = polynomial(x_fit)
# plt.plot(x_fit, y_fit, label='Fitted polynomial', color='red')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.title(f'Polynomial Regression (Degree {degree})')
# plt.show()