import os
import requests

def build_prompt(title, description, severity, status, reporter_info=""):
    return f'''you are a senior software engineer reviewing a bug report.
Analyze it and give a structured review.

Bug Title: {title}
Severity: {severity}
Status: {status}
Description: {description}
Additional Info: {reporter_info or 'None'}

Respond in this formate:
Root Cause: (what likely caused this bug)
Severity AsAssessment: (is the severity label correct? why?)
Suggested Fix: (clear step-by-step fix)
Prevention Tip: (how to avoid this in future) '''

def review_bug(title, description, severity, status, reporter_info=""):
    try:
        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            return {"success": False, "review": "Api_key is not set."}

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a senior software engineer who reviews bug reports and gives clear, actionable feedback."
                    },
                    {
                        "role": "user",
                        "content": build_prompt(title, description, severity, status, reporter_info)
                    }
                ],
                "max_tokens": 1024,
                "temperature": 0.7
            },
            timeout=30
        )
        data = response.json()

        if response.status_code != 200:
            error_msg = data.get("errors", {}).get("message", "Unknown error")
            return {"success": False, "review": f"Groq error: {error_msg}"}

        review_text = data["choices"][0]["message"]["content"]
        return {
            "success": True,
            "review": review_text
            }
    except requests.exceptions.Timeout:
        return {"success": False, "review": "Request timed out. Please try again later."}
    except Exception as e:
        return {"success": False, "review": f" Groq_error: {str(e)}"}