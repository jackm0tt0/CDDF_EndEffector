import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle
import os



def FitCalibrationFunction(df_targets, df_results, filedir, mode = "polynomial"):
    if mode == "polynomial": FitPoly(df_targets, df_results, filedir)

def FitPoly(df_targets, df_results, filedir)->tuple[LinearRegression, np.ndarray]:
    """
    Fits polynomial representaion of targets to resultant data.
    Returns the model and ndarray representation of the targets used for prediction
    """

    # Step 1: Generate sample data

    np.random.seed(1)
    X = df_targets['pos_c']
    Y = df_targets['target_dist']
    Z = df_results["imy"]

    # Flatten the arrays for regression
    # X_flat = X.flatten()
    # Y_flat = Y.flatten()
    # Z_flat = Z.flatten()

    # Step 2: Perform polynomial regression
    degree = 2
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(np.vstack((X, Y)).T)
    print(X_poly)
    print("--------------------------------")
    model = LinearRegression()
    model.fit(X_poly, Z)

    # Create a grid for the fitted surface
    
    X_fit = np.linspace(min(X), max(X), 100)
    Y_fit = np.linspace(min(Y), max(Y), 100)
    X_fit, Y_fit = np.meshgrid(X_fit, Y_fit)
    X_poly_fit = poly.transform(np.vstack((X_fit.flatten(), Y_fit.flatten())).T)
    print(X_poly_fit)
    print(X_poly_fit.shape)
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

    plt.show(block = False)

    pickle.dump(model, open(filedir + "calibration_function.pkl", 'wb'))
    pickle.dump(poly, open(filedir + "data_fitter.pkl", 'wb'))


