/**
 * Dashboard Logic for Oscar Legal Practitioners
 */

document.addEventListener('DOMContentLoaded', () => {
    // Load User Data
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.full_name) {
        document.getElementById('user-welcome').textContent = `Hello, ${user.full_name.split(' ')[0]}`;
        document.getElementById('user-avatar').src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.full_name)}&background=2563eb&color=fff`;
    }

    // Initialize Dashboard Data
    fetchDashboardStats();
    fetchRecentCases();

    // AI Quick Tool
    const aiInput = document.getElementById('ai-quick-query');
    const aiSend = document.getElementById('ai-quick-send');

    async function handleAIQuery() {
        const query = aiInput.value.trim();
        if (!query) return;

        aiInput.value = 'Thinking...';
        aiInput.disabled = true;

        try {
            const response = await fetch('/api/v1/research', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ query })
            });

            if (response.ok) {
                const data = await response.json();
                alert(`AI Response Preview:\n\n${data.answer.substring(0, 300)}...`);
                // In a real app, logic to navigate to research page with results
                window.location.href = `research.html?query=${encodeURIComponent(query)}`;
            } else {
                alert('AI Service is currently busy. Please try again later.');
            }
        } catch (err) {
            console.error('AI error:', err);
        } finally {
            aiInput.value = '';
            aiInput.disabled = false;
        }
    }

    aiSend.addEventListener('click', handleAIQuery);
    aiInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAIQuery();
    });

    // Blog Publishing Logic
    const blogBtn = document.getElementById('publish-insight-btn');
    const blogModal = document.getElementById('blog-modal');
    const saveBlogBtn = document.getElementById('save-blog');

    if (blogBtn) {
        blogBtn.addEventListener('click', () => {
            blogModal.style.display = 'flex';
        });
    }

    if (saveBlogBtn) {
        saveBlogBtn.addEventListener('click', async () => {
            const data = {
                title: document.getElementById('blog-title').value,
                excerpt: document.getElementById('blog-excerpt').value,
                content: document.getElementById('blog-content').value,
                slug: document.getElementById('blog-title').value.toLowerCase().replace(/ /g, '-')
            };

            if (!data.title || !data.content) return alert('Title and Content are required');

            saveBlogBtn.disabled = true;
            try {
                const response = await fetch('/api/v1/blog/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    alert('Legal Insight published successfully!');
                    blogModal.style.display = 'none';
                    // Clear inputs
                    document.getElementById('blog-title').value = '';
                    document.getElementById('blog-excerpt').value = '';
                    document.getElementById('blog-content').value = '';
                } else {
                    alert('Error publishing. Please try again.');
                }
            } catch (err) {
                console.error(err);
            } finally {
                saveBlogBtn.disabled = false;
            }
        });
    }
});

async function fetchDashboardStats() {
    const token = localStorage.getItem('access_token');
    try {
        // Parallel fetch for stats
        const [clientsRes, casesRes, tasksRes] = await Promise.all([
            fetch('/api/v1/clients/', { headers: { 'Authorization': `Bearer ${token}` } }),
            fetch('/api/v1/cases/', { headers: { 'Authorization': `Bearer ${token}` } }),
            fetch('/api/v1/tasks/', { headers: { 'Authorization': `Bearer ${token}` } })
        ]);

        if (clientsRes.ok) {
            const clients = await clientsRes.json();
            document.getElementById('count-clients').textContent = clients.length;
        }
        if (casesRes.ok) {
            const cases = await casesRes.json();
            document.getElementById('count-cases').textContent = cases.length;
        }
        if (tasksRes.ok) {
            const tasks = await tasksRes.json();
            document.getElementById('count-tasks').textContent = tasks.length;
        }
    } catch (err) {
        console.error('Error fetching stats:', err);
    }
}

async function fetchRecentCases() {
    const token = localStorage.getItem('access_token');
    const listElement = document.getElementById('recent-cases-list');

    try {
        const response = await fetch('/api/v1/cases/?limit=5', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const cases = await response.json();
            if (cases.length > 0) {
                listElement.innerHTML = cases.map(c => `
                    <tr>
                        <td style="font-weight:600">${c.title}</td>
                        <td>Client #${c.client_id}</td>
                        <td><span class="case-badge badge-${c.status === 'open' ? 'med' : 'high'}">${c.status}</span></td>
                        <td><a href="cases.html?id=${c.id}" class="link-btn">View</a></td>
                    </tr>
                `).join('');
            }
        }
    } catch (err) {
        console.error('Error fetching cases:', err);
    }
}
