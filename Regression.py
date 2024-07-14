import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd

def FitCalibrationFunction(df_targets, df_results, mode = "polynomial"):
    if mode == "polynomial": FitPoly(df_targets,df_results)

def FitPoly(df_targets, df_results)->tuple[LinearRegression, np.ndarray]:
    """
    Fits polynomial representaion of targets to resultant data.
    Returns the model and ndarray representation of the targets used for prediction
    """

    # Data from targets to include
    labels = ['distance', 'pitch']
    # Step 1: Generate sample data

    features = [df_targets[l] for l in labels]
    print(features)
    np.random.seed(1)
    X = df_targets['x']
    Y = df_targets['y']
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

# # Create a grid for the fitted surface
# X_fit = np.linspace(0, 10, 100)
# Y_fit = np.linspace(0, 10, 100)
# X_fit, Y_fit = np.meshgrid(X_fit, Y_fit)
# X_poly_fit = poly.transform(np.vstack((X_fit.flatten(), Y_fit.flatten())).T)
# Z_fit = model.predict(X_poly_fit).reshape(X_fit.shape)

# # Step 3: Plot the results
# fig = plt.figure(figsize=(12, 6))

# # Original data points
# ax = fig.add_subplot(121, projection='3d')
# ax.scatter(X, Y, Z, label='Data points', color='blue')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('Original Data Points')

# # Fitted polynomial surface
# ax = fig.add_subplot(122, projection='3d')
# ax.plot_surface(X_fit, Y_fit, Z_fit, color='red', alpha=0.5, label='Fitted polynomial')
# ax.scatter(X, Y, Z, color='blue')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('Fitted Polynomial Surface')

# plt.show()


target_df = pd.DataFrame(columns= ['x', 'y', 'z', 'distance', 'power', 'pitch', 'yaw'])
result_df = pd.DataFrame(columns= ['x','y'])


