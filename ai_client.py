from openai import OpenAI


class AiClient:
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(
            api_key=api_key
        )

    def get_response(self, message: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return completion.choices[0].message.content
