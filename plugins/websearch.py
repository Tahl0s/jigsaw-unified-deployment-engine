import requests
from bs4 import BeautifulSoup

class JudePlugin:
    name = "websearch"
    description = "Searches the web using DuckDuckGo and returns the top results."
    trigger_keywords = ["search", "lookup", "google", "find", "look up", "look for", "web"]
    auto_run = True
    min_score = 80

    def run(self, user_input: str, context: dict = {}) -> str:
        # Extract query from user input
        for keyword in self.trigger_keywords:
            if keyword in user_input.lower():
                query = user_input.lower().split(keyword, 1)[-1].strip()
                break
        else:
            return "What would you like me to search for?"

        if not query:
            return "I didn't catch what you want me to search for. Can you rephrase?"

        url = "https://html.duckduckgo.com/html/"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.post(url, data={"q": query}, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", class_="result__a", limit=3)

            if not results:
                return "No results found, sorry."

            reply = f"🔍 Top results for: **{query}**\n\n"
            for i, result in enumerate(results, 1):
                title = result.get_text(strip=True)
                link = result["href"]
                reply += f"{i}. [{title}]({link})\n"
            return reply

        except Exception as e:
            return f"Web search failed: {e}"
