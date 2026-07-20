const state = { benefits: [], sources: [], query: '', category: 'all' };
const el = id => document.getElementById(id);
const normalize = value => String(value || '').toLowerCase();

async function loadData() {
  try {
    const response = await fetch('./data/current/benefits.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    state.benefits = Array.isArray(data.benefits) ? data.benefits : [];
    state.sources = Array.isArray(data.sources) ? data.sources : [];
    el('updated').textContent = `Source information last checked: ${formatDate(data.last_checked)}`;
    populateCategories();
    render();
    renderSourceHealth();
  } catch (error) {
    el('updated').textContent = 'Dashboard data could not be loaded. Use GitHub Pages or a local web server.';
    el('benefit-grid').innerHTML = `<div class="empty">Unable to load benefit data: ${escapeHtml(error.message)}</div>`;
    el('source-health').textContent = 'Unavailable';
  }
}

function populateCategories() {
  const categories = [...new Set(state.benefits.map(item => item.category))].sort();
  el('category').innerHTML = '<option value="all">All categories</option>' + categories.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');
}

function render() {
  const query = normalize(state.query);
  const filtered = state.benefits.filter(item => {
    const text = normalize([item.title,item.category,item.summary,...(item.keywords || [])].join(' '));
    return (state.category === 'all' || item.category === state.category) && (!query || text.includes(query));
  });
  el('result-count').textContent = `${filtered.length} benefit resource${filtered.length === 1 ? '' : 's'} shown`;
  el('empty').hidden = filtered.length !== 0;
  el('benefit-grid').innerHTML = filtered.map(card).join('');
}

function card(item) {
  const apply = item.apply_url ? `<a href="${safeUrl(item.apply_url)}" target="_blank" rel="noopener">Apply or get started</a>` : '';
  return `<article class="benefit-card"><span class="badge">${escapeHtml(item.category)}</span><h2>${escapeHtml(item.title)}</h2><p>${escapeHtml(item.summary)}</p><div class="card-actions"><a href="${safeUrl(item.official_url)}" target="_blank" rel="noopener">Official VA information</a>${apply}</div></article>`;
}

function renderSourceHealth() {
  if (!state.sources.length) { el('source-health').textContent = 'No checks recorded.'; return; }
  el('source-health').innerHTML = state.sources.map(source => `<div class="health-item"><span>${escapeHtml(source.name)}</span><span class="${source.ok ? 'status-ok' : 'status-warn'}">${source.ok ? 'Available' : 'Review'}</span></div>`).join('');
}

function formatDate(value) { if (!value) return 'not yet checked'; const date = new Date(value); return Number.isNaN(date.valueOf()) ? value : date.toLocaleString(); }
function safeUrl(value) { try { const url = new URL(value); return url.protocol === 'https:' ? url.href : '#'; } catch { return '#'; } }
function escapeHtml(value) { return String(value ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }

el('search').addEventListener('input', event => { state.query = event.target.value; render(); });
el('category').addEventListener('change', event => { state.category = event.target.value; render(); });
el('clear').addEventListener('click', () => { state.query=''; state.category='all'; el('search').value=''; el('category').value='all'; render(); });
loadData();
