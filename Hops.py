"""
CDDF Paper Gun End Effector: Calibration Correction Function
Author: Jack Otto
"""
from flask import Flask
import ghhops_server as ghs
import pickle
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

app = Flask(__name__)
hops: ghs.HopsFlask =ghs.Hops(app)

@hops.component(
    '/Calibration',
    description='Deploys Calibration Function as Correction Factor for Shooting Robot',
    inputs=[
        ghs.HopsNumber(
            "pos_x",
            "pos_x",
            "position x",
            access=ghs.HopsParamAccess.ITEM
        ),
        ghs.HopsNumber(
            "pos_y",
            "pos_y",
            "position y",
            access=ghs.HopsParamAccess.ITEM
        ),
        ghs.HopsNumber(
            "pos_z",
            "pos_z",
            "position z",
            access=ghs.HopsParamAccess.ITEM
        ),
        ghs.HopsNumber(
            "target_x",
            "target_x",
            "target x",
            access=ghs.HopsParamAccess.ITEM
        ),
        ghs.HopsNumber(
            "target_y",
            "target_y",
            "target y",
            access=ghs.HopsParamAccess.ITEM
        ),
        ghs.HopsNumber(
            "target_z",
            "target_z",
            "target z",
            access=ghs.HopsParamAccess.ITEM
        ),        
        ghs.HopsString(
            'FilePath', 
            'filepath', 
            'The place where the correction function is stored', 
            access=ghs.HopsParamAccess.ITEM
            )
        ],

    outputs=[
        ghs.HopsString(
            'Debug', 
            'Debug', 
            'Debug', 
            access=ghs.HopsParamAccess.ITEM
            )
        ],
)
def applyCorrection(px,py,pz,tx,ty,tz, filepath: ghs.HopsString):
    print(px,py,filepath)
    loaded_model = pickle.load(open(filepath + "calibration_function.pkl", 'rb'))
    loaded_fitter = pickle.load(open(filepath + "data_fitter.pkl", 'rb'))

    features = np.vstack((px, tz)).T
    params = loaded_fitter.fit_transform(features)

    objectives = loaded_model.predict(params)
    objective = float(objectives[0])
    return "This does not work"



# @hops.component(    
#     "/surrogate",
#     description="Uses a trained Surrogate Model to predict in grasshopper",
#     inputs=[
#         ghs.HopsNumber("Features", "F", "The features to predict", access=ghs.HopsParamAccess.LIST),
#         ghs.HopsString("FeatureNames", "FN", "The list of feature names in the same order as the features",
#                        access=ghs.HopsParamAccess.LIST),
#         ghs.HopsString("ModelName", "M", "The model to use for prediction", access=ghs.HopsParamAccess.ITEM),
#         ],
#     outputs=[
#         ghs.HopsNumber("Labels", "L", "The predicted labels")
#         ],
# )
# def predict(features: float, feature_names: str, model_name: str):
#     # load scaler and get feature order
#     scaler_filename = "sk_transformer.pkl"
#     sc = pickle.load(open(filePath + scaler_filename, 'rb'))
#     feature_order = sc.feature_names_in_

#     feature_dict = {}
#     for j, name in enumerate(feature_names):
#         if name not in feature_dict.keys():
#             feature_dict[name] = []
#         feature_dict[name].append(features[j])
#     feature_df = pd.DataFrame(feature_dict)
#     feature_df = feature_df[feature_order]

#     std_params_data = pd.DataFrame(sc.transform(feature_df))
#     std_params_data.columns = feature_order

#     loaded_model = pickle.load(open(filePath + (model_name + '.pkl'), 'rb'))

#     objectives = loaded_model.predict(std_params_data)
#     objective = float(objectives[0])
#     return objective


if __name__ == "__main__":
    app.run(debug=True)