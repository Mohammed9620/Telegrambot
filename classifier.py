import os
from google import genai

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
_MODEL = "gemini-3.1-flash-lite"

_PROMPT = (
    "You are filtering a message from Telegram job-posting groups. "
    "The message may describe one or several job openings.\n\n"
    "Answer yes ONLY if the message describes a job whose main duties are "
    "software development, IT/technical support, data/AI/machine learning, "
    "cybersecurity, network or cloud engineering, or hardware/electronics "
    "engineering.\n\n"
    "Answer no for sales, customer service, call centers, marketing, "
    "accounting, retail, hospitality, security guards, non-technical "
    "teaching, or any other role that is not a core technology job — even "
    "if the ad mentions phones, computers, or the internet.\n\n"
    "If the message lists several jobs and at least one of them is a "
    "genuine tech role as defined above, answer yes.\n\n"
    "Reply with exactly one word: yes or no.\n\n"
    "Message:\n{text}"
)


def is_tech_related(text: str) -> bool:
    response = _client.models.generate_content(
        model=_MODEL,
        contents=_PROMPT.format(text=text),
    )
    answer = (response.text or "").strip().lower()
    return answer.startswith("yes")
