import base64
from openai import OpenAI

client = OpenAI()

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def generate_tests(url, screenshot_path, accessibility_tree):

    image_b64 = encode_image(screenshot_path)

    prompt = f"""
You are a senior QA automation engineer.

Analyze the provided website screenshot and accessibility tree.

WEBSITE URL: {url}

Accessibility Tree:
{accessibility_tree}

Your task:
1. Identify application type
2. Determine major user flows
3. Create Playwright Python tests

Rules:
- Use Playwright sync API
- Use get_by_role locators (NO CSS selectors)
- Include assertions
- Handle cookie popups
- Include negative test cases

Return ONLY Python code.
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"}
                    }
                ],
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content