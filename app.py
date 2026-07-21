"""
=========================================================
Tamil Nadu Private Omni Bus AI Chatbot (RAG)
Author : Sugumar R
Deployment : Railway
=========================================================
"""


import gradio as gr

from search_engine import ai_search

# ==========================================================
# Chatbot Function
# ==========================================================

def chatbot(message, history):
    """
    Main chatbot function.
    """

    if not message.strip():
        return "Please enter your bus search query."

    try:
        response = ai_search(message)
        return response

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ==========================================================
# Gradio Interface
# ==========================================================

demo = gr.ChatInterface(
    fn=chatbot,

    title="🚌 Tamil Nadu Private Omni Bus AI Chatbot (RAG)",

    description="""
Search private omni buses across Tamil Nadu using AI-powered semantic search.

Example Queries:
• Chennai to Madurai
• Luxury Sleeper Bus
• Volvo Bus under 1000
• AC Bus from Coimbatore to Chennai
""",

    examples=[
        "Chennai to Madurai",
        "Chennai to Salem",
        "Luxury Sleeper",
        "Volvo Bus",
        "Bus under 1000",
        "AC Bus",
        "GreenLine Travels",
        "Bus from Coimbatore to Chennai"
    ],

    theme="soft"
)

# ==========================================================
# Launch
# ==========================================================

if __name__ == "__main__":
    demo.queue()
    demo.launch()

