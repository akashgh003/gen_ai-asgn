from typing import List, Dict, Any

def load_product_catalog() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "Acer Nitro 5",
            "description": "Gaming Laptop, 15.6\" FHD IPS Display, Intel Core i5-11400H, NVIDIA GeForce RTX 3050, 16GB DDR4, 512GB NVMe SSD",
            "price": 899.99,
            "originalPrice": 999.99,
            "imageUrl": None,
            "rating": 4.5,
            "reviewCount": 128,
            "category": "Laptops",
            "specs": {
                "processor": "Intel Core i5-11400H (6 cores, up to 4.5GHz)",
                "storage": "512GB NVMe SSD",
                "memory": "16GB DDR4 RAM",
                "graphics": "NVIDIA GeForce RTX 3050 (4GB GDDR6)",
                "display": "15.6\" FHD (1920 x 1080) IPS, 144Hz",
                "battery": "Up to 8 hours battery life"
            },
            "recommendation": "This laptop is recommended for your video editing needs under $1000 because it offers an excellent balance of performance and value. The 6-core Intel processor paired with the NVIDIA RTX 3050 graphics card provides strong rendering capabilities for video editing software like Adobe Premiere Pro and DaVinci Resolve. The 16GB RAM is sufficient for most editing projects, while the 512GB NVMe SSD ensures fast loading times for your footage and projects."
        },
        {
            "id": 2,
            "name": "Dell G15 5511",
            "description": "15.6\" FHD, Intel Core i5-11400H, NVIDIA GeForce RTX 3050 Ti, 16GB RAM, 512GB SSD, Windows 11",
            "price": 949.99,
            "originalPrice": 1049.99,
            "imageUrl": None,
            "rating": 4.3,
            "reviewCount": 95,
            "category": "Laptops",
            "specs": {
                "processor": "Intel Core i5-11400H (6 cores, up to 4.5GHz)",
                "storage": "512GB NVMe SSD",
                "memory": "16GB DDR4 RAM",
                "graphics": "NVIDIA GeForce RTX 3050 Ti (4GB GDDR6)",
                "display": "15.6\" FHD (1920 x 1080) 120Hz",
                "battery": "Up to 6 hours battery life"
            },
            "recommendation": "This Dell G15 is well-suited for video editing tasks under $1000. It features a slightly better GPU than the Acer Nitro 5 with the RTX 3050 Ti, which offers improved rendering performance. The processor and RAM match our top recommendation, making it excellent for multitasking between editing software and other applications. The slightly lower battery life makes it less portable, but the enhanced graphics capabilities make it worth considering if you prioritize rendering speed."
        },
        {
            "id": 3,
            "name": "ASUS TUF Gaming F15",
            "description": "15.6\" 144Hz FHD Display, Intel Core i7-11800H, GeForce RTX 3050, 16GB DDR4, 512GB PCIe SSD",
            "price": 979.99,
            "originalPrice": 1099.99,
            "imageUrl": None,
            "rating": 4.6,
            "reviewCount": 187,
            "category": "Laptops",
            "specs": {
                "processor": "Intel Core i7-11800H (8 cores, up to 4.6GHz)",
                "storage": "512GB PCIe SSD",
                "memory": "16GB DDR4 RAM",
                "graphics": "NVIDIA GeForce RTX 3050 (4GB GDDR6)",
                "display": "15.6\" FHD (1920 x 1080) 144Hz",
                "battery": "Up to 7 hours battery life"
            },
            "recommendation": "The ASUS TUF Gaming F15 features a more powerful 8-core Intel i7 processor, making it especially strong for video encoding and rendering tasks. This processor advantage gives it an edge for timeline scrubbing and preview rendering in video editing software. While it has the same RTX 3050 GPU as the Acer Nitro 5, the processor upgrade significantly improves overall editing performance. The military-grade durability also makes it more resistant to wear and tear if you need to edit on the go."
        },
        {
            "id": 4,
            "name": "MSI GF63 Thin",
            "description": "15.6\" FHD Display, Intel Core i5-11400H, NVIDIA GeForce GTX 1650, 8GB DDR4, 256GB NVMe SSD",
            "price": 799.99,
            "originalPrice": 899.99,
            "imageUrl": None,
            "rating": 4.2,
            "reviewCount": 143,
            "category": "Laptops",
            "specs": {
                "processor": "Intel Core i5-11400H (6 cores, up to 4.5GHz)",
                "storage": "256GB NVMe SSD",
                "memory": "8GB DDR4 RAM",
                "graphics": "NVIDIA GeForce GTX 1650 (4GB GDDR6)",
                "display": "15.6\" FHD (1920 x 1080) 60Hz",
                "battery": "Up to 7 hours battery life"
            },
            "recommendation": "The MSI GF63 Thin is the most budget-friendly option for basic video editing. While it has less RAM and a weaker GPU than our other recommendations, it's still capable of handling 1080p video editing with some optimization. It would benefit from a RAM upgrade to 16GB for better performance with video editing software. The smaller SSD may require an external drive for storing video projects, but the lower price point makes this a good entry-level option."
        },
        {
            "id": 5,
            "name": "Lenovo Legion 5",
            "description": "15.6\" FHD Display, AMD Ryzen 5 5600H, NVIDIA GeForce RTX 3050 Ti, 16GB RAM, 512GB SSD",
            "price": 969.99,
            "originalPrice": 1079.99,
            "imageUrl": None,
            "rating": 4.7,
            "reviewCount": 213,
            "category": "Laptops",
            "specs": {
                "processor": "AMD Ryzen 5 5600H (6 cores, up to 4.2GHz)",
                "storage": "512GB PCIe SSD",
                "memory": "16GB DDR4 RAM",
                "graphics": "NVIDIA GeForce RTX 3050 Ti (4GB GDDR6)",
                "display": "15.6\" FHD (1920 x 1080) 120Hz",
                "battery": "Up to 8 hours battery life"
            },
            "recommendation": "The Lenovo Legion 5 with its AMD Ryzen 5 processor offers excellent multi-core performance for video editing tasks. AMD processors often perform very well in multi-threaded applications like video rendering. The RTX 3050 Ti GPU and 16GB of RAM make this a strong contender for video editing under $1000. It also features an advanced cooling system that helps maintain performance during long rendering sessions, which is particularly valuable for video editing workloads."
        }
    ]