 ##TODO(developer): Uncomment and set the following variables
project_id = 'aiot-fit-xlab'
compute_region = 'us-central1'
model_id = 'TCN7656632053749434671'
# file_path = '/local/path/to/file'

from google.cloud import automl_v1beta1 as automl

automl_client = automl.AutoMlClient()

# Create client for prediction service.
prediction_client = automl.PredictionServiceClient()

# Get the full path of the model.
model_full_id = automl_client.model_path(
    project_id, compute_region, model_id
)

# Read the file content for prediction.
##with open(file_path, "rb") as content_file:
##    snippet = content_file.read()


snippet = "suck my cock"

# Set the payload by giving the content and type of the file.
payload = {"text_snippet": {"content": snippet, "mime_type": "text/plain"}}

# params is additional domain-specific parameters.
# currently there is no additional parameters supported.
params = {}
response = prediction_client.predict(model_full_id, payload, params)
print("Prediction results:")
for result in response.payload:
    print("Predicted class name: {}".format(result.display_name))
    print("Predicted class score: {}".format(result.classification.score))
