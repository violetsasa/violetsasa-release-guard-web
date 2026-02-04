import './style.css'
import { marked } from 'marked'
import 'github-markdown-css/github-markdown-dark.css'

const app = {
    async init() {
        try {
            const response = await fetch('./encyclopedia.md');
            if (!response.ok) throw new Error('Failed to load content');
            const navText = await response.text();

            // Render Markdown
            const contentDiv = document.getElementById('markdown-content');
            contentDiv.innerHTML = marked.parse(navText);

            // Build Table of Contents
            this.buildTOC();

            // Setup Search
            this.setupSearch();

            // Show Content
            document.getElementById('loading').style.display = 'none';
            contentDiv.style.display = 'block';

        } catch (error) {
            console.error(error);
            document.getElementById('loading').innerHTML = '<p style="color:red">Error loading document.</p>';
        }
    },

    buildTOC() {
        const tocNav = document.getElementById('toc');
        const headers = document.querySelectorAll('.markdown-body h2, .markdown-body h3');

        headers.forEach((header, index) => {
            // Generate robust ID
            const id = 'header-' + index;
            header.id = id;

            const link = document.createElement('a');
            link.href = '#' + id;
            link.textContent = header.textContent;
            link.className = header.tagName.toLowerCase();

            link.onclick = (e) => {
                e.preventDefault();
                header.scrollIntoView({ behavior: 'smooth' });
                // Update active state manually
                document.querySelectorAll('.toc-nav a').forEach(a => a.classList.remove('active'));
                link.classList.add('active');
            };

            tocNav.appendChild(link);
        });
    },

    setupSearch() {
        const input = document.getElementById('searchInput');
        input.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const content = document.getElementById('markdown-content');

            // Simple highlight/search logic (can be improved)
            // Ideally shows/hides sections, but for markdown monolithic blob, text highlighting is standard.
            // For now, let's just highlight text.

            // Note: Implementing a full "hide unmatched sections" in a single markdown blob is complex without granular HTML structure.
            // A simpler approach for this MVP: Scroll to first match?

            // Let's implement a filter for the TOC instead
            const links = document.querySelectorAll('.toc-nav a');
            links.forEach(link => {
                if (link.textContent.toLowerCase().includes(term)) {
                    link.style.display = 'block';
                } else {
                    link.style.display = 'none';
                }
            });
        });
    }
}

app.init();
