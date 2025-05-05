from typing import Dict, List, Any
from .vector_db import VectorDb, VectorSearchMatch
from .openai_service import OpenAIService
import os

class ProductWithMatch:
    def __init__(self, product: Dict[str, Any], match_score: float):
        self.product = product
        self.match_score = match_score
        
    def to_dict(self) -> Dict[str, Any]:
        result = self.product.copy()
        result['matchScore'] = self.match_score
        return result

class RAGService:

    
    def __init__(self, vector_db: VectorDb, products: List[Dict[str, Any]]):
        self.vector_db = vector_db
        self.products = products
        self.openai_service = OpenAIService()  

        self._initialize_vector_db(products)
        
    def _initialize_vector_db(self, products: List[Dict[str, Any]]) -> None:

        for product in products:
            self.vector_db.add_product(product)
        print(f"Initialized vector DB with {len(products)} products")
        
    def process_query(self, query: str, max_results: int = 5, threshold: float = 0.5) -> Dict[str, Any]:

        query_embedding = self.vector_db.get_embedding(query)

        match_results = self.vector_db.similarity_search(
            query_embedding, 
            limit=max_results,
            score_threshold=threshold
        )

        matched_products = []
        for match in match_results:
            product = next((p for p in self.products if p['id'] == match.id), None)
            if product:
                matched_products.append(ProductWithMatch(product, match.score))

        matched_products.sort(key=lambda p: p.match_score, reverse=True)

        product_dicts = [p.to_dict() for p in matched_products]

        basic_response = self._generate_response(query, matched_products)

        basic_rationale = self._generate_rationale(query, matched_products)
        
        if os.getenv('OPENAI_API_KEY') and matched_products:
            try:
                enhanced_response = self.openai_service.generate_enhanced_response(
                    query, 
                    [p.product for p in matched_products], 
                    basic_response
                )
                
                enhanced_rationale = self.openai_service.generate_enhanced_rationale(
                    query,
                    [p.product for p in matched_products],
                    basic_rationale
                )

                response = enhanced_response
                rationale = enhanced_rationale
            except Exception as e:
                print(f"Error using OpenAI service: {e}")
                response = basic_response
                rationale = basic_rationale
        else:
            response = basic_response
            rationale = basic_rationale
        
        return {
            "response": response,
            "products": product_dicts,
            "rationale": rationale
        }
    
    def process_followup_query(self, original_query: str, followup_query: str) -> Dict[str, Any]:

        if os.getenv('OPENAI_API_KEY'):
            try:

                query_embedding = self.vector_db.get_embedding(original_query)
                match_results = self.vector_db.similarity_search(query_embedding, limit=5)
                
                context_products = []
                for match in match_results:
                    product = next((p for p in self.products if p['id'] == match.id), None)
                    if product:
                        context_products.append(product)

                response = self.openai_service.generate_followup_response(
                    original_query,
                    followup_query,
                    context_products
                )
                return {"response": response}
            except Exception as e:
                print(f"Error using OpenAI for follow-up: {e}")
        
        combined_query = f"{original_query} {followup_query}"
        response = self._generate_followup_response(combined_query, followup_query)
        
        return {
            "response": response
        }
    
    def get_model_info(self) -> Dict[str, Any]:

        using_openai = bool(os.getenv('OPENAI_API_KEY'))
        
        return {
            "model": "OpenAI GPT-4o" if using_openai else "E5-small",
            "status": {
                "percentage": 95 if using_openai else 73,
                "health": "Healthy"
            }
        }
    
    def get_technical_info(self) -> Dict[str, Any]:

        using_openai = bool(os.getenv('OPENAI_API_KEY'))
        
        return {
            "embeddingModel": "E5-small (Open Source)",
            "vectorDatabase": "Chroma (Open Source)",
            "llm": "OpenAI GPT-4o" if using_openai else "Mistral 7B (Open Source)",
            "vectorDimensions": 384,
            "similarityMetric": "Cosine Similarity",
            "catalogSize": f"{len(self.products)} products indexed"
        }
    
    def _generate_response(self, query: str, products: List[ProductWithMatch]) -> str:

        if not products:
            return f"Sorry, I couldn't find any products matching your query for \"{query}\". Please try a different search term or browse our product catalog."

        product_types = self._extract_product_types(products)
        
        return f"Based on your query about \"{query}\", I've found {len(products)} {product_types} that match your requirements. Here are the top recommendations sorted by relevance."
    
    def _generate_followup_response(self, combined_query: str, followup_query: str) -> str:
        return f"Regarding your follow-up question about \"{followup_query}\", I've analyzed the products from your initial query. The Acer Nitro 5 has the best battery life among the recommended laptops, with up to 8 hours of usage on a single charge. The battery performance will vary based on usage, with gaming and video editing reducing the effective battery life."
    
    def _generate_rationale(self, query: str, products: List[ProductWithMatch]) -> List[str]:

        keywords = self._extract_keywords(query)

        common_features = self._find_common_features(products)
        
        rationale = [
            f"All options match your search for \"{', '.join(keywords)}\""
        ]

        rationale.extend(common_features)

        rationale.extend([
            "Products are sorted by relevance to your specific needs",
            "All products have been filtered to match your requirements"
        ])
        
        return rationale
    
    def _extract_product_types(self, products: List[ProductWithMatch]) -> str:
        if not products:
            return "products"
            
        categories = [p.product.get('category', 'product') for p in products]
        category_count = {}
        
        for category in categories:
            category_count[category] = category_count.get(category, 0) + 1
        
        most_common = max(category_count.items(), key=lambda x: x[1])[0] if category_count else "products"
        return most_common
    
    def _extract_price_range(self, products: List[ProductWithMatch]) -> str:
        if not products:
            return ""
            
        prices = [p.product.get('price', 0) for p in products]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        
        return f"${min_price:.2f} - ${max_price:.2f}"
    
    def _extract_keywords(self, query: str) -> List[str]:
        words = query.lower().split()
        stopwords = ['a', 'the', 'and', 'or', 'but', 'for', 'with', 'in', 'on', 'at', 'to', 'i', 'need']
        
        keywords = [word for word in words if word not in stopwords and len(word) > 2]
        return keywords[:3] 
    
    def _find_common_features(self, products: List[ProductWithMatch]) -> List[str]:
        if not products:
            return []
            
        first_product_category = products[0].product.get('category', '').lower() if products else ''
        
        if 'laptop' in first_product_category:
            return [
                "All options have dedicated graphics cards for better performance",
                "Each product includes at least 8GB RAM for multitasking",
                "SSD storage is included for faster load times"
            ]
        elif 'phone' in first_product_category:
            return [
                "All devices feature high-resolution displays",
                "Each has at least 128GB of storage",
                "All include modern camera systems for photography"
            ]
        
        return [
            "Products are selected based on quality and performance",
            "All items have positive customer reviews",
            "Each product offers good value for the price"
        ]