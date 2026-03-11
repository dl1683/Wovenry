import json
import os

from google import genai
from core.models import Category


def generate_category_tags(title: str, content: str, description: str) -> list[str]:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return []

    valid_categories = list(Category.objects.values_list("name", flat=True))
    if not valid_categories:
        return []

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=(
            f"You are a categorization assistant. Given the following metaprompt, "
            f"select 1 to 3 categories from this EXACT list that best describe it:\n\n"
            f"{', '.join(valid_categories)}\n\n"
            f"Title: {title}\n"
            f"Content: {content[:2000]}\n"
            f"Description: {description[:500]}\n\n"
            f'Respond with ONLY a JSON array of 1-3 category names from the list above. '
            f'Example: ["Strategy", "Writing"]'
        ),
    )

    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        suggested = json.loads(text)
        return [c for c in suggested if c in valid_categories][:3]
    except (json.JSONDecodeError, AttributeError, IndexError):
        return []
