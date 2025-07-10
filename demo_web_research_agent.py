#!/usr/bin/env python3
"""
Grok4 Web Research Agent
Advanced tool use demo for web scraping and API integration
"""

import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse
import time
from bs4 import BeautifulSoup

load_dotenv()

class WebResearchAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_webpage(self, url: str) -> Dict[str, Any]:
        """Fetch and parse webpage content"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract metadata
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title"
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ''
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    links.append({
                        'url': href,
                        'text': link.get_text().strip()
                    })
            
            return {
                "success": True,
                "url": url,
                "title": title_text,
                "description": description,
                "content": text[:5000],  # Limit content length
                "links": links[:10],  # Limit number of links
                "status_code": response.status_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def search_web(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Search web using DuckDuckGo API"""
        try:
            # Using DuckDuckGo Instant Answer API
            search_url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            
            # Extract instant answer
            if data.get('Abstract'):
                results.append({
                    'type': 'instant_answer',
                    'title': data.get('Heading', ''),
                    'content': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', ''),
                    'source': data.get('AbstractSource', '')
                })
            
            # Extract related topics
            for topic in data.get('RelatedTopics', [])[:num_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'type': 'related_topic',
                        'title': topic.get('Text', '').split(' - ')[0],
                        'content': topic.get('Text', ''),
                        'url': topic.get('FirstURL', '')
                    })
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "total_results": len(results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e)
            }
    
    def analyze_competitor(self, domain: str) -> Dict[str, Any]:
        """Analyze competitor website structure and content"""
        try:
            url = f"https://{domain}" if not domain.startswith('http') else domain
            
            # Fetch main page
            main_page = self.fetch_webpage(url)
            if not main_page["success"]:
                return main_page
            
            # Analyze common pages
            common_paths = ['/about', '/services', '/products', '/contact', '/pricing']
            pages_found = []
            
            for path in common_paths:
                test_url = urljoin(url, path)
                try:
                    response = self.session.head(test_url, timeout=5)
                    if response.status_code == 200:
                        pages_found.append({
                            'path': path,
                            'url': test_url,
                            'status': 'found'
                        })
                except:
                    pass
            
            # Extract technology indicators
            tech_indicators = []
            content = main_page["content"].lower()
            
            tech_keywords = {
                'react': 'React.js',
                'angular': 'Angular',
                'vue': 'Vue.js',
                'wordpress': 'WordPress',
                'shopify': 'Shopify',
                'woocommerce': 'WooCommerce',
                'bootstrap': 'Bootstrap'
            }
            
            for keyword, tech in tech_keywords.items():
                if keyword in content:
                    tech_indicators.append(tech)
            
            return {
                "success": True,
                "domain": domain,
                "main_page": {
                    "title": main_page["title"],
                    "description": main_page["description"]
                },
                "pages_found": pages_found,
                "technology_indicators": tech_indicators,
                "total_links": len(main_page["links"]),
                "analysis_timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "domain": domain,
                "error": str(e)
            }
    
    def get_tools_definition(self):
        """Define tools for Grok4 function calling"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "fetch_webpage",
                    "description": "Fetch and analyze content from a specific webpage",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL of the webpage to fetch"
                            }
                        },
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the web for information on a topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "Number of results to return",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_competitor",
                    "description": "Analyze competitor website structure and technology",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "description": "Domain name to analyze (e.g., example.com)"
                            }
                        },
                        "required": ["domain"]
                    }
                }
            }
        ]
    
    def conduct_research(self, research_query: str):
        """Conduct research using Grok4 with web tools"""
        tools = self.get_tools_definition()
        
        messages = [
            {
                "role": "system",
                "content": "You are a web research specialist. Use the available tools to gather information from the web, analyze websites, and provide comprehensive research insights. Always cite sources and provide actionable intelligence."
            },
            {
                "role": "user",
                "content": research_query
            }
        ]
        
        response = self.client.chat.completions.create(
            model="grok-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        # Handle tool calls
        if response.choices[0].message.tool_calls:
            messages.append(response.choices[0].message)
            
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the function
                if function_name == "fetch_webpage":
                    result = self.fetch_webpage(**function_args)
                elif function_name == "search_web":
                    result = self.search_web(**function_args)
                elif function_name == "analyze_competitor":
                    result = self.analyze_competitor(**function_args)
                else:
                    result = {"error": f"Unknown function: {function_name}"}
                
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id
                })
            
            # Get final response
            final_response = self.client.chat.completions.create(
                model="grok-4",
                messages=messages,
                tools=tools
            )
            
            return final_response.choices[0].message.content
        else:
            return response.choices[0].message.content

def main():
    agent = WebResearchAgent()
    
    print("Grok4 Web Research Agent")
    print("=" * 50)
    
    sample_queries = [
        "Research the latest trends in AI development",
        "Analyze the website structure of tesla.com",
        "Find information about sustainable energy solutions",
        "Compare the features of top project management tools",
        "Research market trends for electric vehicles"
    ]
    
    print("Sample research queries:")
    for i, query in enumerate(sample_queries, 1):
        print(f"{i}. {query}")
    
    print("\nEnter your research request (or 'quit' to exit):")
    
    while True:
        user_input = input("\nResearch Query: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        try:
            result = agent.conduct_research(user_input)
            print(f"\nResearch Results:\n{result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
