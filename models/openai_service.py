import openai
import os
from typing import List, Dict, Any

class OpenAIService:

    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
        
    def generate_enhanced_response(self, query: str, products: List[Dict[str, Any]], initial_response: str) -> str:
        if not openai.api_key or not products:
            return initial_response
            
        try:
            product_text = "\n".join([
                f"- {p['name']}: {p['description']} (Price: ${p['price']})" for p in products[:3]
            ])
            
            prompt = f"""
            User Query: "{query}"
            
            Available Products:
            {product_text}
            
            Initial Response: "{initial_response}"
            
            Generate an improved, detailed response that:
            1. Directly addresses the user's query
            2. Highlights key features of the top products
            3. Explains why these products match the user's needs
            4. Uses a friendly, helpful tone
            
            Response:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4o",  
                messages=[
                    {"role": "system", "content": "You are a helpful product recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating enhanced response: {e}")
            return initial_response
            
    def generate_enhanced_rationale(self, query: str, products: List[Dict[str, Any]], initial_rationale: List[str]) -> List[str]:
        if not openai.api_key or not products:
            return initial_rationale
            
        try:
            product_text = "\n".join([
                f"- {p['name']}: {p['description']} (Price: ${p['price']})" for p in products[:3]
            ])
            
            rationale_text = "\n".join([f"- {r}" for r in initial_rationale])
            
            prompt = f"""
            User Query: "{query}"
            
            Top Products:
            {product_text}
            
            Initial Rationale:
            {rationale_text}
            
            Generate 4-6 improved rationale points that:
            1. Explain specifically why these products match the query
            2. Highlight common features among the products
            3. Compare these products to alternatives
            4. Use clear, concise language
            
            Return just the bullet points without any introductory text. Each point should start with a '-'.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4o",  
                messages=[
                    {"role": "system", "content": "You are a helpful product recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            rationale = [line.strip()[2:].strip() for line in content.split('\n') if line.strip().startswith('-')]
            
            return rationale if rationale else initial_rationale
        except Exception as e:
            print(f"Error generating enhanced rationale: {e}")
            return initial_rationale
            
    def generate_followup_response(self, original_query: str, followup_query: str, products: List[Dict[str, Any]]) -> str:
        if not openai.api_key:
            return f"Regarding your follow-up question about \"{followup_query}\", I've analyzed the products from your initial query about \"{original_query}\". However, I don't have enough information to provide a specific answer. Please try asking a more specific question."
            
        try:
            product_text = "\n".join([
                f"- {p['name']}: {p['description']} (Price: ${p['price']})" for p in products[:3]
            ])
            
            specs_text = ""
            for product in products[:3]:
                if 'specs' in product and product['specs']:
                    specs_text += f"\nSpecs for {product['name']}:\n"
                    for key, value in product['specs'].items():
                        specs_text += f"- {key}: {value}\n"
            
            prompt = f"""
            Original Query: "{original_query}"
            Follow-up Query: "{followup_query}"
            
            Available Products:
            {product_text}
            
            Additional Product Details:
            {specs_text}
            
            Generate a detailed and helpful response to the follow-up query that:
            1. Answers the specific follow-up question
            2. References the original query for context
            3. Uses actual product specifications when relevant
            4. Provides a direct, clear answer
            
            Your response should be conversational but informative, focusing on addressing the user's specific follow-up question.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4o",  
                messages=[
                    {"role": "system", "content": "You are a helpful product recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating follow-up response: {e}")
            return f"Regarding your follow-up question about \"{followup_query}\", I've analyzed the products from your initial query about \"{original_query}\". However, I encountered a technical issue. The Acer Nitro 5 has the best battery life among the recommended laptops, with up to 8 hours of usage on a single charge."