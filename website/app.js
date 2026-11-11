// Render Gallery
function renderGallery(data) {
    const grid = document.getElementById('galleryGrid');
    grid.innerHTML = data.map(item => `
        <div class="gallery-card card rounded-lg p-0 fade-in" data-name="${item.name}" data-category="${item.category}">
            <div class="h-40 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                <i class="fas fa-sparkles text-4xl text-green-400/50"></i>
            </div>
            <div class="gallery-overlay">
                <h3 class="font-bold text-white">${item.name}</h3>
                <p class="text-xs text-gray-300 mt-1 line-clamp-2">${item.description}</p>
                <div class="flex gap-2 mt-2">
                    <span class="tag ${item.edition === 'java' ? 'tag-java' : 'tag-bedrock'}">${item.edition}</span>
                    <span class="tag tag-cosmetic">${item.category}</span>
                </div>
            </div>
            <div class="p-4 border-t border-[#30363d]">
                <div class="flex justify-between text-xs text-gray-500">
                    <span><i class="fas fa-particles mr-1"></i>${item.particles} particles</span>
                    <span><i class="fas fa-brain mr-1"></i>${item.complexity}</span>
                </div>
                <div class="text-xs text-gray-500 mt-1">
                    <i class="fas fa-square-root-variable mr-1"></i>${item.math}
                </div>
            </div>
        </div>
    `).join('');
}

// Render Agents
function renderAgents(data) {
    const grid = document.getElementById('agentsGrid');
    grid.innerHTML = data.map(item => `
        <div class="card rounded-lg p-6 fade-in">
            <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg bg-${item.color}-500/20 flex items-center justify-center">
                    <i class="fas ${item.icon} text-${item.color}-400"></i>
                </div>
                <h3 class="font-bold">${item.name}</h3>
            </div>
            <p class="text-sm text-gray-400 mb-3">${item.role}</p>
            <div class="text-xs text-gray-500 space-y-1">
                <div><span class="text-gray-400">Model:</span> ${item.model}</div>
                <div><span class="text-gray-400">Input:</span> ${item.input}</div>
                <div><span class="text-gray-400">Output:</span> ${item.output}</div>
            </div>
        </div>
    `).join('');
}

// Render Docs
function renderDocs(data) {
    const grid = document.getElementById('docsGrid');
    grid.innerHTML = data.map(item => `
        <a href="https://github.com/Erudition-Computing-Group/minecraft-production-factory/blob/main/docs/${item.file}"
           target="_blank" class="card rounded-lg p-4 flex items-center gap-3 fade-in hover:no-underline">
            <i class="fas ${item.icon} text-green-400 text-xl w-6 text-center"></i>
            <div>
                <h3 class="font-semibold text-sm">${item.title}</h3>
                <p class="text-xs text-gray-500">${item.description}</p>
            </div>
        </a>
    `).join('');
}

// Search
let fuse;
function initSearch() {
    const searchData = [
        ...galleryData.map(d => ({ type: 'effect', title: d.name, desc: d.description, category: d.category, keywords: d.math })),
        ...agentsData.map(d => ({ type: 'agent', title: d.name, desc: d.role, category: 'Agent', keywords: d.model })),
        ...docsData.map(d => ({ type: 'doc', title: d.title, desc: d.description, category: 'Documentation', keywords: d.file })),
    ];
    fuse = new Fuse(searchData, {
        keys: ['title', 'desc', 'category', 'keywords'],
        threshold: 0.4,
        includeScore: true,
    });

    const input = document.getElementById('searchInput');
    const results = document.getElementById('searchResults');

    input.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        if (query.length < 2) {
            results.classList.add('hidden');
            return;
        }
        const hits = fuse.search(query).slice(0, 8);
        if (hits.length === 0) {
            results.innerHTML = '<p class="text-gray-500 text-sm p-4">No results found.</p>';
            results.classList.remove('hidden');
            return;
        }
        results.innerHTML = hits.map(h => {
            const item = h.item;
            const icon = item.type === 'effect' ? 'fa-sparkles' : item.type === 'agent' ? 'fa-robot' : 'fa-file-alt';
            return `
                <div class="card rounded-lg p-3 mb-2 flex items-center gap-3 fade-in">
                    <i class="fas ${icon} text-green-400"></i>
                    <div>
                        <div class="font-semibold text-sm">${item.title}</div>
                        <div class="text-xs text-gray-500">${item.desc}</div>
                    </div>
                    <span class="ml-auto text-xs text-gray-600">${item.category}</span>
                </div>
            `;
        }).join('');
        results.classList.remove('hidden');
    });

    // Hide results on click outside
    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !results.contains(e.target)) {
            results.classList.add('hidden');
        }
    });
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(a.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
});

// Init
document.addEventListener('DOMContentLoaded', () => {
    renderGallery(galleryData);
    renderAgents(agentsData);
    renderDocs(docsData);
    initSearch();
});
