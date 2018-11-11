import sys

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2


def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'text_snippet': {'content': content, 'mime_type': 'text/plain' }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned

if __name__ == '__main__':
  content = sys.argv[1]
  project_id = sys.argv[2]
  model_id = sys.argv[3]

  res = get_prediction(content, project_id,  model_id)
  print (res)

  print ("**********************")

  print("Prediction results:")
  for result in res.payload:
      print("Predicted class name: {}".format(result.display_name))
      print("Predicted class score: {}".format(result.classification.score))

      if result.display_name == "harassment" and result.classification.score > 0.5 :
          print ("likely harassing message detected")

    
      
    

  
