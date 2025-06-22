# clotributor/gemini_summarizer.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load & configure your Gemini API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("🔑 GOOGLE_API_KEY not set in .env")
genai.configure(api_key=api_key)

def summarize_issue(issue):
    """
    Uses Gemini to summarize an issue and suggest a beginner-friendly solution path.

    Args:
        issue (dict): Dictionary with 'title', 'link', 'metadata', and 'difficulty'.

    Returns:
        dict: Original issue dict with 'summary' and 'suggested_solution' added.
    """
    prompt = f"""
You are an experienced open-source contributor helping newcomers understand
and solve GitHub issues.

Please do the following for the issue below:
1. Summarize the problem in 2-3 concise sentences.
2. Suggest a simple, beginner-friendly plan to start solving it —
   including what parts of the codebase to look at or what skills are needed.

Format your answer like this:

Summary:
<your summary here>

Suggested Approach:
<your step-by-step suggestion here>

---

Title: {issue['title']}
Metadata: {issue['metadata']}
Link: {issue['link']}
"""

    try:
        # Use one of the models that support generateContent
        model    = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        content  = response.text.strip()

        # parse into summary & suggestion
        summary, suggestion = content, ""
        if "Suggested Approach:" in content:
            head, tail = content.split("Suggested Approach:", 1)
            summary    = head.replace("Summary:", "").strip()
            suggestion = tail.strip()

        return { **issue, "summary": summary, "suggested_solution": suggestion }

    except Exception as e:
        print(f"[Gemini Error] {e}")
        return { **issue, "summary": "N/A", "suggested_solution": "N/A" }
