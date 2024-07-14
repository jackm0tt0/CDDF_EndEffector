"""
CDDF Paper Gun End Effector: Calibration Correction Function
Author: Jack Otto
"""
from flask import Flask
import ghhops_server as ghs

app = Flask(__name__)
hops: ghs.HopsFlask =ghs.Hops(app)

@hops.component(
    '/Calibration',
    description='Deploys Calibration Function as Correction Factor for Shooting Robot',
    inputs=[
        ghs.HopsPoint(
            'Position', 
            'P', 
            'The robot position to shoot from', 
            access=ghs.HopsParamAccess.ITEM
            ),
        ghs.HopsPoint(
            'Target', 
            'T', 
            'The target point to shoot at', 
            access=ghs.HopsParamAccess.ITEM
            ),
        ghs.HopsString(
            'FilePath', 
            'filepath', 
            'The place where the correction function is stored', 
            access=ghs.HopsParamAccess.ITEM
            ),
        ],

    outputs=[
        ghs.HopsPoint(
            'Frame', 
            'F', 
            'Target Frame', 
            ghs.HopsParamAccess.ITEM
            )
        ],
)
def applyCorrection(position: ghs.HopsPoint, target: ghs.HopsPoint, filepath: ghs.HopsString):
    print(position,target,filepath)
    return position


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