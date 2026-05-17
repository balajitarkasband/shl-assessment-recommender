from app.retriever import search_assessments
from app.llm import generate_response
from app.prompts import SYSTEM_PROMPT


def is_vague_query(text):
    vague_words = [
        "assessment",
        "test",
        "hiring",
        "need assessment"
    ]

    return len(text.split()) < 4 or text.lower() in vague_words


def is_comparison_query(text):
    compare_words = ["difference", "compare", "vs"]

    return any(word in text.lower() for word in compare_words)


def is_off_topic(text):
    banned = [
        "legal advice",
        "politics",
        "weather"
    ]

    return any(word in text.lower() for word in banned)


def handle_chat(messages):
    latest_user_message = messages[-1].content

    if is_off_topic(latest_user_message):
        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    if is_vague_query(latest_user_message):
        return {
            "reply": "Sure — what role are you hiring for and what skills are important?",
            "recommendations": [],
            "end_of_conversation": False
        }

    retrieved = search_assessments(latest_user_message, top_k=5)

    context = "\n".join([
        f"{item['name']} - {item['description']}"
        for item in retrieved
    ])

    prompt = f"""
{SYSTEM_PROMPT}

Conversation:
{messages}

Catalog Context:
{context}

User Query:
{latest_user_message}

Generate recommendation response.
"""

    reply = "Here are recommended SHL assessments for the role."

    recommendations = []

    for item in retrieved:
        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item.get("test_type", "Unknown")
        })

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": True
    }