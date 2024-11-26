import os
import base64

def getresponse(image, client):
    completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "extract the vendor name, line items, and total amount as a json output and only extract these details and do not extract any other data. Do not put any explaination, only output the raw json output. Do not prefix with any text such as json or put any quotations around the values. Format the JSON like this: {vendorName: string, lineItems: Array<{name: string, value: number}>, totalAmount: number}" 
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image}"
                    }
                }
            ]}
        ],
        model="gpt-4o",
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
