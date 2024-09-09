from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import numpy as np
from io import BytesIO
from PIL import Image
import os
# Your client credentials

class image_downloader():
    def __init__(self):
        client_id = 'sh-7355d8ee-729c-4091-abc6-1f5956727522'
        client_secret = 'JBPKsGOvn6SVjDEVoJZvRL28MFvOoyTB'


        # Create a session
        client = BackendApplicationClient(client_id=client_id)
        self.oauth = OAuth2Session(client=client)

        # Get token for the session
        token = self.oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                                client_secret=client_secret, include_client_id=True)



        def sentinelhub_compliance_hook(response):
            response.raise_for_status()
            return response

        self.oauth.register_compliance_hook("access_token_response", sentinelhub_compliance_hook)

    def download_image(self,  bbox, time_range, width=512, height=512):
        

        # check if image is already downloaded
        if os.path.exists('images/'+str(bbox)+str(time_range[0])+'_'+str(time_range[1])+str(width)+str(height)+'.png'):
            img = Image.open('images/'+str(bbox)+str(time_range[0])+'_'+str(time_range[1])+str(width)+str(height)+'.png')
            img = np.array(img)
            img = np.asarray(img, dtype=np.float32)/255.0
            return img
        else:
            evalscript = """
            //VERSION=3
            function setup() {
            return {
                input: ["B02", "B03", "B04"],
                output: {
                bands: 3,
                sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
                },
            }
            }

            function evaluatePixel(sample) {
            return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
            }
            """

            request = {
                "input": {
                    "bounds": {
                        "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                        "bbox": bbox,
                    },
                    "data": [
                        {
                            "type": "sentinel-2-l2a",
                            "dataFilter": {
                                "timeRange": {
                                    "from": time_range[0],
                                    "to": time_range[1],
                                }
                            },
                        }
                    ],
                },
                "output": {
                    "width": width,
                    "height": height,
                },
                "evalscript": evalscript,
            }

            url = "https://sh.dataspace.copernicus.eu/api/v1/process"
            response = self.oauth.post(url, json=request)
            # Save the raw response content to a file
            image_data = BytesIO(response.content)
            # Load the image using PIL
            img = Image.open(image_data)
            img.save('images/'+str(bbox)+str(time_range[0])+'_'+str(time_range[1])+str(width)+str(height)+'.png')

            img = np.array(img)
            img = np.asarray(img, dtype=np.float32)/255.0

            return img
