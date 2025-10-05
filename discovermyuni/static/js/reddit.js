// Reddit-like front-end enhancements (static demo only)
// Planned dynamic behaviors (NOT IMPLEMENTED):
//  - Voting: POST /api/posts/{id}/vote/
//  - Save: POST /api/posts/{id}/save/
//  - Infinite scroll: GET /api/posts/?cursor=...

(function(){
  document.addEventListener('DOMContentLoaded', function(){
    // Score placeholder
    document.querySelectorAll('.reddit-post .vote-score').forEach((el, idx) => {
      const fake = 231 - idx * 7;
      el.textContent = fake > 0 ? fake : 0;
    });

    // Infinite scroll / load more stub
    const loadMoreBtn = document.getElementById('loadMore');
    if(loadMoreBtn){
      loadMoreBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loadMoreBtn.textContent = 'Loading (demo)';
        setTimeout(()=>{ loadMoreBtn.textContent = 'No more (static demo)'; loadMoreBtn.disabled = true; }, 900);
      });
    }

    // Theme toggles (navbar only now, sidebar removed)
    const body = document.body;
    function syncIcons(){
      const dark = body.classList.contains('theme-dark');
      document.querySelectorAll('#themeToggle .theme-icon-sun, #themeToggle .theme-icon-moon').forEach(icon=>{
        if(icon.classList.contains('theme-icon-sun')) icon.classList.toggle('d-none', dark);
        if(icon.classList.contains('theme-icon-moon')) icon.classList.toggle('d-none', !dark);
      });
    }
    const mainToggle = document.getElementById('themeToggle');
    if(mainToggle){
      mainToggle.addEventListener('click', ()=>{
        body.classList.toggle('theme-dark');
        localStorage.setItem('theme', body.classList.contains('theme-dark') ? 'dark':'light');
        syncIcons();
      });
    }
    syncIcons();

    // Left rail collapsible sections
    document.querySelectorAll('.reddit-left-collapsible').forEach(section => {
      const btn = section.querySelector('[data-collapse-btn]');
      if(!btn) return;
      btn.addEventListener('click', () => {
        const collapsed = section.getAttribute('data-collapsed') === 'true';
        section.setAttribute('data-collapsed', collapsed ? 'false' : 'true');
        btn.classList.toggle('collapsed-rotate', !collapsed);
      });
    });

    // Skeleton demo (non functional placeholder): if a feed has data-skeleton-count, inject mock cards
    document.querySelectorAll('[data-skeleton-count]').forEach(feed => {
      const count = parseInt(feed.getAttribute('data-skeleton-count'),10) || 0;
      if(count>0 && feed.children.length===0){
        for(let i=0;i<count;i++){
          const wrapper=document.createElement('div');
          wrapper.className='card-surface p-4 flex gap-4 animate-pulse';
          wrapper.innerHTML=`<div class="flex flex-col items-center w-10 gap-2">\n              <div class='skeleton h-3 w-3 rounded-sm'></div>\n              <div class='skeleton h-3 w-6 rounded'></div>\n              <div class='skeleton h-3 w-3 rounded-sm'></div>\n            </div>\n            <div class='flex-1 space-y-3'>\n              <div class='skeleton h-3 w-40 rounded'></div>\n              <div class='skeleton h-4 w-3/4 rounded'></div>\n              <div class='skeleton h-4 w-5/6 rounded'></div>\n              <div class='flex gap-2 pt-2'>\n                <div class='skeleton h-6 w-16 rounded'></div>\n                <div class='skeleton h-6 w-16 rounded'></div>\n              </div>\n            </div>`;
          feed.appendChild(wrapper);
        }
      }
    });
  });
})();