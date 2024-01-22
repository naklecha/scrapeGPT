# This file is a derivative of the project found at https://github.com/ishan0102/vimGPT

import base64
import os
from io import BytesIO

import openai
import instructor
from dotenv import load_dotenv
from pydantic import BaseModel
from PIL import Image
from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
IMG_RES = 1080

# Enables `response_model`
client = instructor.patch(OpenAI(), mode=instructor.function_calls.Mode.MD_JSON)


# Function to encode the image
def encode_and_resize(image):
    W, H = image.size
    image = image.resize((IMG_RES, int(IMG_RES * H / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

class action_details(BaseModel):
    description: str
    text: str


def get_actions(screenshot):
    encoded_screenshot = encode_and_resize(screenshot)
    example_json = '''
        {
            'description': 'describe the image in detail',
            'text': 'place every text in the image here'
        }
    '''
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=action_details,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""You are a web navigator describe the image with as much detail as possible. 
                                The outputted JSON MUST look like:
                                {example_json}
                        """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_screenshot}",
                        },
                    },
                ],
            }
        ],
        max_tokens=4096,
    )

    print(response)
    return response

if __name__ == "__main__":
    image = Image.open("./screenshots/screenshot_d8af2023-c738-4209-bbd3-4716bd5cef15.png")
    actions = get_actions(image)


