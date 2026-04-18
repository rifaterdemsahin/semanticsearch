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

    // 5. Simple Search Implementation
    const searchInput = document.getElementById('site-search');
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        // Implementation for simple search placeholder
        if(query.length > 2) {
            console.log('Searching for:', query);
        }
    });
});
