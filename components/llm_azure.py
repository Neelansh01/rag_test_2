"""Optional: generate a direct answer using Azure OpenAI (e.g. GPT-4o)."""
from typing import Optional

from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
)


def is_azure_configured(
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> bool:
    """Return True if Azure OpenAI can be used (key + endpoint set)."""
    key = api_key or AZURE_OPENAI_API_KEY
    url = endpoint or AZURE_OPENAI_ENDPOINT
    return bool(key and url)


def generate_with_azure(
    query: str,
    context: str,
    *,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    deployment: Optional[str] = None,
    api_version: Optional[str] = None,
) -> tuple[Optional[str], Optional[str]]:
    """
    Call Azure OpenAI chat completions to get a direct answer from the context.
    Returns (answer_text, error_message). If success, error_message is None.
    """
    key = api_key or AZURE_OPENAI_API_KEY
    url = (endpoint or AZURE_OPENAI_ENDPOINT or "").rstrip("/")
    deploy = deployment or AZURE_OPENAI_DEPLOYMENT
    version = api_version or AZURE_OPENAI_API_VERSION

    if not key or not url:
        return None, "Azure OpenAI not configured. Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT (or use Streamlit secrets)."

    try:
        from openai import AzureOpenAI
    except ImportError:
        return None, "Install the openai package: pip install openai"

    client = AzureOpenAI(
        api_key=key,
        api_version=version,
        azure_endpoint=url,
    )
    system = (
        "You are a helpful assistant. Answer the user's question using ONLY the provided context. "
        "If the context does not contain enough information, say so briefly. Keep the answer direct and concise."
    )
    user_content = f"Context:\n\n{context}\n\nQuestion: {query}"
    try:
        response = client.chat.completions.create(
            model=deploy,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
            max_tokens=1024,
        )
        text = response.choices[0].message.content if response.choices else None
        return (text or "", None)
    except Exception as e:
        return None, str(e)
