document.addEventListener('DOMContentLoaded', async () => {
    const debugToggle = document.getElementById('debug-toggle');
    const debugMenu = document.getElementById('debug-menu');
    const debugLinks = document.getElementById('debug-links');
    const contentLinks = document.getElementById('content-links');
    const journeyGrid = document.getElementById('journey');

    // 1. Load Menu Data
    try {
        const response = await fetch('menu.json');
        const data = await response.json();
        renderMenus(data);
        if (journeyGrid) renderJourney(data.navigation);
    } catch (err) {
        console.error('Error loading menu:', err);
    }

    // 2. Debug Mode Handling
    const setCookie = (name, value) => {
        document.cookie = `${name}=${value};path=/;max-age=31536000`;
    };

    const getCookie = (name) => {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    };

    let isDebug = getCookie('debug') === 'true';
    if (isDebug) debugMenu.classList.remove('hidden');

    debugToggle.addEventListener('click', () => {
        isDebug = !isDebug;
        setCookie('debug', isDebug);
        debugMenu.classList.toggle('hidden', !isDebug);
        alert(`Debug mode: ${isDebug ? 'ENABLED' : 'DISABLED'}`);
    });

    // 3. Render Menus
    function renderMenus(data) {
        // Debug Menu (1_Real...7_Testing)
        data.navigation.forEach(item => {
            const a = document.createElement('a');
            a.href = `markdown_renderer.html?file=${item.path}/README.md`;
            a.textContent = item.name;
            debugLinks.appendChild(a);
        });

        // Content Menu
        data.content.forEach(item => {
            const a = document.createElement('a');
            // Check if it's .md or .html
            if (item.path.endsWith('.md')) {
                a.href = `markdown_renderer.html?file=${item.path}`;
            } else {
                a.href = item.path;
            }
            a.textContent = item.name;
            contentLinks.appendChild(a);
        });
    }

    // 4. Render Journey Cards (Index Page only)
    function renderJourney(navigation) {
        navigation.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3>${index + 1}. ${item.name}</h3>
                <p>Explore the details of this project phase.</p>
                <a href="markdown_renderer.html?file=${item.path}/README.md" class="btn-secondary">View Phase</a>
            `;
            journeyGrid.appendChild(card);
        });
    }

    // 5. Search with Autocomplete
    const searchInput = document.getElementById('site-search');
    const searchResults = document.getElementById('search-results');
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        searchResults.innerHTML = '';
        if (query.length < 2) return;

        const allLinks = [
            ...data.navigation.map(n => ({...n, type: 'Phase'})),
            ...data.content.map(c => ({...c, type: 'Page'}))
        ];

        const filtered = allLinks.filter(l => l.name.toLowerCase().includes(query));
        
        filtered.forEach(item => {
            const div = document.createElement('div');
            div.className = 'search-item';
            div.innerHTML = `<span>${item.name}</span> <small>${item.type}</small>`;
            div.onclick = () => {
                window.location.href = item.path.endsWith('.md') 
                    ? `markdown_renderer.html?file=${item.path}` 
                    : (item.path.includes('_') ? `markdown_renderer.html?file=${item.path}/README.md` : item.path);
            };
            searchResults.appendChild(div);
        });
    });

    // 6. Dynamic Carousel (for 3_Simulation phase)
    if (window.location.search.includes('3_Simulation')) {
        initCarousel();
    }

    async function initCarousel() {
        // Placeholder for automatic image discovery (would typically use a JSON index)
        const contentDiv = document.getElementById('content');
        if (!contentDiv) return;
        
        const carouselHtml = `
            <div class="carousel-container">
                <div class="carousel-slide">
                    <img src="3_Simulation/fast_embed.png" alt="Fast Embed Visualization">
                </div>
                <!-- Future images will be appended here -->
            </div>
        `;
        contentDiv.insertAdjacentHTML('afterbegin', carouselHtml);
    }
});
