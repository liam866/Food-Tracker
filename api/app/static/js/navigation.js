import { pages, profileViews, navButtons, pageTitle } from './main.js';

export function showPage(pageName) {
    console.log(`[Navigation] Showing page: ${pageName}`);
    Object.values(pages).forEach(p => p.classList.add('hidden'));
    if (pages[pageName]) {
        pages[pageName].classList.remove('hidden');
        pageTitle.textContent = pageName.charAt(0).toUpperCase() + pageName.slice(1);
    }
    if (pageName === 'diary') pageTitle.textContent = "Today";

    navButtons.forEach(btn => {
        const isActive = btn.dataset.page === pageName;
        btn.classList.toggle('text-slate-900', isActive);
        btn.classList.toggle('text-slate-400', !isActive);
    });
    
    if(pageName === 'profile') {
        showProfileView('main');
    }

    // Show back button on Quick Add and History pages
    if (pageName === 'quickAdd' || pageName === 'history') {
        document.getElementById('back-button').classList.remove('hidden');
    } else if (pageName === 'diary') {
        document.getElementById('back-button').classList.add('hidden');
    }
}

export function showProfileView(viewName) {
    console.log(`[Navigation] Showing profile view: ${viewName}`);
    Object.values(profileViews).forEach(view => view.classList.add('hidden'));
    if (profileViews[viewName]) {
        profileViews[viewName].classList.remove('hidden');
    }
    document.getElementById('back-button').classList.toggle('hidden', viewName === 'main');
     pageTitle.textContent = viewName === 'main' ? 'Profile' : `Update ${viewName.charAt(0).toUpperCase() + viewName.slice(6)}`;
}
