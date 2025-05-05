let selectedProduct = null;

document.addEventListener('DOMContentLoaded', function() {
    init();
});

function init() {
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleSearch();
        });
    }
    
    const followUpForm = document.getElementById('followup-form');
    if (followUpForm) {
        followUpForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFollowUp();
        });
    }
    
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            applyTheme(savedTheme);
        }
    }
    
    const textSearchButton = document.getElementById('text-search-button');
    if (textSearchButton) {
        textSearchButton.addEventListener('click', handleTextSearch);
    }
    
    const textSearchInput = document.getElementById('text-search-input');
    if (textSearchInput) {
        textSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleTextSearch();
            }
        });
    }
    
    const modal = document.getElementById('product-modal');
    const closeBtn = document.querySelector('.close-btn');
    
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
        
        window.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
    
    fetchTechnicalInfo();
    fetchModelInfo();
}

async function handleSearch() {
    const queryInput = document.getElementById('query-input');
    const query = queryInput.value.trim();
    
    if (!query) {
        alert('Please enter a query');
        return;
    }
    
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '<div class="loading">Processing your query...</div>';
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        if (!response.ok) {
            throw new Error('Failed to process query');
        }
        
        const data = await response.json();
        displayResults(data, query);
    } catch (error) {
        console.error('Error:', error);
        const resultsContainer = document.getElementById('results-container');
        resultsContainer.innerHTML = `<div class="error">Error processing your query. Please try again.</div>`;
    }
}

async function handleFollowUp() {
    const followUpInput = document.getElementById('followup-input');
    const followupQuery = followUpInput.value.trim();
    const originalQuery = document.getElementById('query-input').value.trim();
    
    if (!followupQuery) {
        alert('Please enter a follow-up question');
        return;
    }
    
    const followupContainer = document.getElementById('followup-response');
    followupContainer.innerHTML = '<div class="loading">Processing your follow-up question...</div>';
    
    try {
        const response = await fetch('/api/query/followup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                originalQuery, 
                followupQuery 
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to process follow-up query');
        }
        
        const data = await response.json();
        
        followupContainer.innerHTML = `
            <div class="followup-question">"${followupQuery}"</div>
            <div class="followup-answer">${data.response}</div>
        `;
    } catch (error) {
        console.error('Error:', error);
        const followupContainer = document.getElementById('followup-response');
        followupContainer.innerHTML = `<div class="error">Error processing your follow-up question. Please try again.</div>`;
    }
    
    followUpInput.value = '';
}

async function handleTextSearch() {
    const searchInput = document.getElementById('text-search-input');
    const query = searchInput.value.trim();
    
    if (!query) {
        alert('Please enter a search query');
        return;
    }
    
    try {
        const resultsContainer = document.getElementById('search-results');
        resultsContainer.innerHTML = '<div class="loading">Processing your query...</div>';
        
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Search request failed');
        }
        
        const data = await response.json();
        
        displaySearchResults(data, query);
    } catch (error) {
        console.error('Error during search:', error);
        alert('An error occurred while processing your search. Please try again.');
    }
}

function displaySearchResults(data, query) {
    const resultsContainer = document.getElementById('search-results');
    
    resultsContainer.innerHTML = '';
    
    const responseHeader = document.createElement('div');
    responseHeader.className = 'response-header';
    responseHeader.textContent = data.response;
    resultsContainer.appendChild(responseHeader);
    
    if (data.products.length === 0) {
        return;
    }
    
    const productGrid = document.createElement('div');
    productGrid.className = 'product-grid';
    
    data.products.forEach(product => {
        const productCard = createProductCard(product);
        productGrid.appendChild(productCard);
    });
    
    resultsContainer.appendChild(productGrid);
    
    if (data.rationale && data.rationale.length > 0) {
        const rationaleSection = document.createElement('div');
        rationaleSection.className = 'rationale-section';
        
        const rationaleTitle = document.createElement('h3');
        rationaleTitle.textContent = 'Why these results?';
        rationaleSection.appendChild(rationaleTitle);
        
        const rationaleList = document.createElement('ul');
        data.rationale.forEach(point => {
            const listItem = document.createElement('li');
            listItem.textContent = point;
            rationaleList.appendChild(listItem);
        });
        
        rationaleSection.appendChild(rationaleList);
        resultsContainer.appendChild(rationaleSection);
    }
}

function displayResults(data, query) {
    const resultsContainer = document.getElementById('results-container');

    const followupSection = document.getElementById('followup-section');
    if (followupSection) {
        followupSection.classList.remove('hidden');
    }

    resultsContainer.innerHTML = '';

    const responseMessage = document.createElement('div');
    responseMessage.className = 'response-message';
    responseMessage.textContent = data.response;
    resultsContainer.appendChild(responseMessage);

    if (data.products && data.products.length > 0) {
        const productGrid = document.createElement('div');
        productGrid.className = 'product-grid';

        data.products.forEach(product => {
            const productCard = createProductCard(product);
            productGrid.appendChild(productCard);
        });
        
        resultsContainer.appendChild(productGrid);
    }

    if (data.rationale && data.rationale.length > 0) {
        const rationaleSection = document.createElement('div');
        rationaleSection.className = 'rationale-section';
        
        const rationaleTitle = document.createElement('h3');
        rationaleTitle.className = 'rationale-title';
        rationaleTitle.textContent = 'Why these recommendations?';
        rationaleSection.appendChild(rationaleTitle);
        
        const rationaleList = document.createElement('ul');
        rationaleList.className = 'rationale-list';
        
        data.rationale.forEach(item => {
            const rationaleItem = document.createElement('li');
            rationaleItem.className = 'rationale-item';
            rationaleItem.textContent = item;
            rationaleList.appendChild(rationaleItem);
        });
        
        rationaleSection.appendChild(rationaleList);
        resultsContainer.appendChild(rationaleSection);
    }
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.addEventListener('click', () => showProductDetail(product));

    let discountPercentage = '';
    if (product.originalPrice && product.price && product.originalPrice > product.price) {
        const discount = ((product.originalPrice - product.price) / product.originalPrice) * 100;
        discountPercentage = `${Math.round(discount)}% off`;
    }

    const stars = '★'.repeat(Math.floor(product.rating || 0)) + 
                 '☆'.repeat(5 - Math.floor(product.rating || 0));

    let matchScoreHtml = '';
    if (product.matchScore !== undefined) {
        const scorePercentage = Math.round(product.matchScore * 100);
        matchScoreHtml = `<div class="match-score">${scorePercentage}% match</div>`;
    }
    
    card.innerHTML = `
        ${matchScoreHtml}
        <div class="product-header">
            <div class="product-name">${product.name}</div>
            <div class="product-rating">
                <span class="rating-stars">${stars}</span>
                <span class="review-count">(${product.reviewCount || 0} reviews)</span>
            </div>
            <div class="product-price">
                <span class="current-price">$${product.price.toFixed(2)}</span>
                ${product.originalPrice ? `<span class="original-price">$${product.originalPrice.toFixed(2)}</span>` : ''}
                ${discountPercentage ? `<span class="price-savings">${discountPercentage}</span>` : ''}
            </div>
        </div>
        <div class="product-description">${product.description}</div>
        <div class="product-tags">
            <div class="product-tag">${product.category}</div>
            ${product.specs && product.specs.processor ? `<div class="product-tag">${product.specs.processor.split(' ')[0]} ${product.specs.processor.split(' ')[1]}</div>` : ''}
            ${product.specs && product.specs.graphics ? `<div class="product-tag">${product.specs.graphics.split(' ')[2]}</div>` : ''}
        </div>
    `;
    
    return card;
}

function showProductDetail(product) {
    const modal = document.getElementById('product-modal');
    const modalContent = document.getElementById('modal-content-container');
    
    selectedProduct = product;

    let specsHtml = '';
    if (product.specs) {
        specsHtml = Object.entries(product.specs).map(([key, value]) => {
            const icon = getSpecIcon(key);
            return `
                <div class="spec-item">
                    <div class="spec-icon">${icon}</div>
                    <div class="spec-content">
                        <div class="spec-label">${key.charAt(0).toUpperCase() + key.slice(1)}</div>
                        <div class="spec-value">${value}</div>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    let discountPercentage = '';
    if (product.originalPrice && product.price && product.originalPrice > product.price) {
        const discount = ((product.originalPrice - product.price) / product.originalPrice) * 100;
        discountPercentage = `${Math.round(discount)}% off`;
    }
    
    const stars = '★'.repeat(Math.floor(product.rating || 0)) + 
                 '☆'.repeat(5 - Math.floor(product.rating || 0));
    
    let matchScoreHtml = '';
    if (product.matchScore !== undefined) {
        const scorePercentage = Math.round(product.matchScore * 100);
        matchScoreHtml = `<div class="match-score">${scorePercentage}% match</div>`;
    }
    
    modalContent.innerHTML = `
        <div class="product-detail">
            ${matchScoreHtml}
            <div class="product-detail-header">
                <div>
                    <h2 class="product-detail-name">${product.name}</h2>
                    <div class="product-detail-category">${product.category}</div>
                    <div class="product-rating">
                        <span class="rating-stars">${stars}</span>
                        <span class="review-count">(${product.reviewCount || 0} reviews)</span>
                    </div>
                </div>
                <div class="product-detail-price-container">
                    <div class="product-detail-price">$${product.price.toFixed(2)}</div>
                    ${product.originalPrice ? `<div class="product-detail-original">$${product.originalPrice.toFixed(2)}</div>` : ''}
                    ${discountPercentage ? `<div class="price-savings">${discountPercentage}</div>` : ''}
                </div>
            </div>
            
            <div class="product-detail-image">
                ${product.imageUrl ? `<img src="${product.imageUrl}" alt="${product.name}" />` : '<div class="no-image">No image available</div>'}
            </div>
            
            <div class="product-detail-info">
                <div class="product-detail-description">
                    <h3>Description</h3>
                    <p>${product.description}</p>
                </div>
                
                <div class="product-detail-specs">
                    <h3>Specifications</h3>
                    <div class="specs-list">
                        ${specsHtml}
                    </div>
                </div>
            </div>
            
            ${product.recommendation ? `
                <div class="product-detail-recommendation">
                    <h3>Why We Recommend This</h3>
                    <p>${product.recommendation}</p>
                </div>
            ` : ''}
        </div>
    `;
    
    modal.style.display = 'block';
}

function getSpecIcon(specKey) {
    const icons = {
        processor: '💻',
        storage: '💾',
        memory: '🧠',
        graphics: '🖼️',
        display: '🖥️',
        battery: '🔋',
        default: '📊'
    };
    
    return icons[specKey.toLowerCase()] || icons.default;
}

async function fetchTechnicalInfo() {
    try {
        const response = await fetch('/api/technical-info');
        
        if (!response.ok) {
            throw new Error('Failed to fetch technical info');
        }
        
        const data = await response.json();
        displayTechnicalInfo(data);
    } catch (error) {
        console.error('Error fetching technical info:', error);
        const techInfoCard = document.getElementById('technical-info-card');
        
        if (techInfoCard) {
            techInfoCard.innerHTML = `
                <h3>Technical Details</h3>
                <div class="error">Error loading technical information.</div>
            `;
        }
    }
}

function displayTechnicalInfo(data) {
    const techInfoCard = document.getElementById('technical-info-card');
    
    if (!techInfoCard) return;
    
    const items = [
        { label: 'Embedding Model', value: data.embeddingModel },
        { label: 'Vector Database', value: data.vectorDatabase },
        { label: 'LLM', value: data.llm },
        { label: 'Vector Dimensions', value: data.vectorDimensions },
        { label: 'Similarity Metric', value: data.similarityMetric },
        { label: 'Catalog Size', value: data.catalogSize }
    ];
    
    let infoItemsHtml = '';
    
    items.forEach(item => {
        infoItemsHtml += `
            <div class="tech-info-item">
                <div class="tech-info-label">${item.label}:</div>
                <div class="tech-info-value">${item.value}</div>
            </div>
        `;
    });
    
    techInfoCard.innerHTML = `
        <h3>Technical Details</h3>
        <div class="tech-info">
            <div class="tech-info-grid">
                ${infoItemsHtml}
            </div>
        </div>
    `;
}

async function fetchModelInfo() {
    try {
        const response = await fetch('/api/model-info');
        
        if (!response.ok) {
            throw new Error('Failed to fetch model info');
        }
        
        const data = await response.json();
        displayModelInfo(data);
    } catch (error) {
        console.error('Error fetching model info:', error);
        const modelInfoCard = document.getElementById('model-info-card');
        
        if (modelInfoCard) {
            modelInfoCard.innerHTML = `
                <h3>Model Information</h3>
                <div class="error">Error loading model information.</div>
            `;
        }
    }
}

function displayModelInfo(data) {
    const modelInfoCard = document.getElementById('model-info-card');
    
    if (!modelInfoCard) return;
    
    modelInfoCard.innerHTML = `
        <h3>Model Information</h3>
        <div class="model-status">
            <div class="model-info-grid">
                <div class="model-info-label">Model:</div>
                <div class="model-info-value">${data.model}</div>
                
                <div class="model-info-label">Status:</div>
                <div class="model-info-value">${data.status.health}</div>
            </div>
            
            <div>
                <div class="model-info-label">Health:</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.status.percentage}%"></div>
                </div>
            </div>
        </div>
    `;
}

function toggleTheme() {
    const body = document.body;
    
    if (body.classList.contains('light-theme')) {
        applyTheme('dark');
    } else {
        applyTheme('light');
    }
}

function applyTheme(theme) {
    const body = document.body;
    
    if (theme === 'dark') {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
    } else {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
    }
    
    localStorage.setItem('theme', theme);
}