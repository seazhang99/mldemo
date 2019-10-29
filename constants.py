apikey = "<Your API Key>"
allowed_extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
tmp_folder = "static/resources/tmp"
tmp_feature_zip_file = tmp_folder + "/temp.zip"
urls = {"lang-detect": "https://sandbox.api.sap.com/ml/api/v2alpha1/text/lang-detect/",
        "lang-translate": "https://sandbox.api.sap.com/mlfs/api/v2/text/translation",
        "face-detect": "https://sandbox.api.sap.com/ml/api/v2alpha1/image/face-detection",
        "image-classification": "https://sandbox.api.sap.com/mlfs/api/v2/image/classification",
        "image-feature-extract": "https://sandbox.api.sap.com/mlfs/api/v2/image/feature-extraction",
        "face-feature-extract": "https://sandbox.api.sap.com/ml/api/v2alpha1/image/face-feature-extraction",
        "similarity-scoring": "https://sandbox.api.sap.com/mlfs/api/v2/similarity-scoring",
        "ocr": "https://sandbox.api.sap.com/mlfs/api/v2/image/ocr",
        "scene-text-recognition": "https://sandbox.api.sap.com/mlfs/api/v2/image/scene-text-recognition"}
