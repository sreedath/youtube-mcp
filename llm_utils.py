from openai import OpenAI

PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4.1-mini",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": "gemini-2.5-flash",
    },
}


def ask_llm(prompt, provider="openai", api_key=""):
    config = PROVIDERS[provider]
    client = OpenAI(api_key=api_key, base_url=config["base_url"])

    response = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content
