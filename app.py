from ai_client import AiClient
from search_client import SearchClient
import debugpy
from flask import request, Flask, Response, render_template, render_template_string
from typing import Tuple, Dict, Any
import markdown
from dotenv import load_dotenv
import os

PROMPT = '''
You are a tool used to help researchers search for answers and summarize the results. Make sure that you give your response in markdown format.

Here is the query:
{query}
    
Summarize the following search results
{results}

Summary:
'''

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

ai_api_client = AiClient(api_key=api_key)
search_client = SearchClient()


def setup_debugging() -> None:
    debugpy.listen(("0.0.0.0", 5678))
    print("Debugger is active on port 5678")
    app.run(debug=True)


@app.route('/')
def search_page() -> str:
    return render_template('home.html')


@app.route('/search')
def summarize() -> str:
    query = request.args.get('q')
    if not query:
        return {'error': 'Query parameter is required'}, 400

    search_results = search_client.search(query)

    summary = ai_api_client.get_response(
        PROMPT.format(query=query, results=search_results))

    markdown_content = f"# Search Results for: {query}\n\n{summary}"
    html_content = markdown.markdown(markdown_content)

    return render_template('search_results.html', html_content=html_content)


if __name__ == '__main__':
    app.run(debug=True)
