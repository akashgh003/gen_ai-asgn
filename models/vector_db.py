from typing import Dict, List, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorSearchMatch:
    def __init__(self, id: int, score: float):
        self.id = id
        self.score = score

def simple_embedding(text: str) -> np.ndarray:
    embedding = np.zeros(384)
    seed = sum(ord(char) for char in text)
    
    for i in range(embedding.shape[0]):
        angle = (seed + i) * 0.1
        embedding[i] = np.sin(angle)
    
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    
    return embedding

class VectorDb:
    
    def __init__(self):
        self.embeddings = {} 
        self.product_texts = {}  
    
    def add_product(self, product: Dict[str, Any]) -> None:

        product_id = product['id']

        product_text = self._create_product_text(product)

        embedding = simple_embedding(product_text)
        
        self.embeddings[product_id] = embedding
        self.product_texts[product_id] = product_text
    
    def get_embedding(self, query: str) -> np.ndarray:
        return simple_embedding(query)
    
    def similarity_search(self, query_vector: np.ndarray, limit: int = 5, score_threshold: float = 0.5) -> List[VectorSearchMatch]:
        results = []
        
        for product_id, embedding in self.embeddings.items():
            similarity = cosine_similarity([query_vector], [embedding])[0][0]
            
            if similarity >= score_threshold:
                results.append(VectorSearchMatch(product_id, similarity))
        
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:limit]
    
    def get_size(self) -> int:
        return len(self.embeddings)
    
    def _create_product_text(self, product: Dict[str, Any]) -> str:
        parts = [
            product.get('name', ''),
            product.get('description', ''),
            f"Category: {product.get('category', '')}",
        ]
        
        specs = product.get('specs', {})
        for key, value in specs.items():
            parts.append(f"{key}: {value}")
        
        return '. '.join(parts)

def setup_vector_db() -> VectorDb:
    return VectorDb()