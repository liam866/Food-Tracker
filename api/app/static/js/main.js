import { state } from './state.js';
import { apiRequest } from './api.js';
import { showPage, showProfileView } from './navigation.js';
import { renderDashboard, renderProfile, renderSearchResults, updateSelectedFoodView } from './render.js';

// --- DOM ELEMENT REFERENCES ---
export const views = {
    userSetup: document.getElementById('user-setup-view'),
    appShell: document.getElementById('app-shell'),
};
export const pages = {
    diary: document.getElementById('diary-page'),
    quickAdd: document.getElementById('quick-add-page'),
    history: document.getElementById('history-page'),
    scan: document.getElementById('scan-page'),
    plan: document.getElementById('plan-page'),
    profile: document.getElementById('profile-page'),
};
export const profileViews = {
    main: document.getElementById('profile-main-view'),
    updateGoals: document.getElementById('update-goals-view'),
    updateInfo: document.getElementById('update-info-view'),
};
export const navButtons = document.querySelectorAll('.nav-btn');
export const pageTitle = document.getElementById('page-title');
export const goalButtons = document.querySelectorAll('.goal-btn');
const userSetupForm = document.getElementById('user-setup-form');
const deleteModal = document.getElementById('delete-modal');
const updateInfoForm = document.getElementById('update-info-form');

// --- EVENT LISTENERS ---
navButtons.forEach(button => button.addEventListener('click', () => showPage(button.dataset.page)));
document.getElementById('quick-add-btn').addEventListener('click', () => showPage('quickAdd'));
document.getElementById('history-btn').addEventListener('click', () => showPage('history'));
document.getElementById('update-goals-btn').addEventListener('click', () => showProfileView('updateGoals'));
document.getElementById('update-info-btn').addEventListener('click', () => showProfileView('updateInfo'));
document.getElementById('back-button').addEventListener('click', () => {
    if (pages.profile.style.display !== 'none' && profileViews.main.classList.contains('hidden')) {
        showProfileView('main');
    } else {
        showPage('diary');
    }
});
document.getElementById('delete-account-btn').addEventListener('click', () => deleteModal.classList.remove('hidden'));
document.getElementById('cancel-delete-btn').addEventListener('click', () => deleteModal.classList.add('hidden'));
document.getElementById('confirm-delete-btn').addEventListener('click', async () => {
    try {
        await apiRequest('/user/profile', 'DELETE');
        state.userProfile = null;
        state.dailyLog = null;
        views.userSetup.classList.remove('hidden');
        views.appShell.classList.add('hidden');
        deleteModal.classList.add('hidden');
    } catch (error) { console.error("Failed to delete account:", error); }
});

goalButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        state.selectedGoal = btn.dataset.goal;
        renderProfile();
    });
});

document.getElementById('save-goal-btn').addEventListener('click', async () => {
    if (!state.selectedGoal || !state.userProfile) return;
    const updatedProfileData = { ...state.userProfile, goal: state.selectedGoal };
    try {
        const updatedProfile = await apiRequest('/user/profile', 'POST', updatedProfileData);
        state.userProfile = updatedProfile;
        renderDashboard();
        renderProfile();
        showProfileView('main');
    } catch (error) { console.error("Failed to update goal:", error); }
});

updateInfoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(updateInfoForm);
    const updatedData = Object.fromEntries(formData.entries());
    updatedData.age = parseInt(updatedData.age);
    updatedData.height_cm = parseFloat(updatedData.height_cm);
    updatedData.weight_kg = parseFloat(updatedData.weight_kg);
    
    const fullProfile = { ...state.userProfile, ...updatedData };
    
    try {
        const updatedProfile = await apiRequest('/user/profile', 'POST', fullProfile);
        state.userProfile = updatedProfile;
        renderDashboard();
        renderProfile();
        showProfileView('main');
    } catch (error) { console.error("Failed to update info:", error); }
});

userSetupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(userSetupForm);
    const profileData = Object.fromEntries(formData.entries());
    profileData.age = parseInt(profileData.age);
    profileData.height_cm = parseFloat(profileData.height_cm);
    profileData.weight_kg = parseFloat(profileData.weight_kg);
    
    try {
        const newUserProfile = await apiRequest('/user/profile', 'POST', profileData);
        state.userProfile = newUserProfile;
        initApp();
    } catch (error) {
        console.error("Failed to create profile:", error);
    }
});

let searchTimeout;
document.getElementById('food-search-input').addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value;
    if (query.length < 2) {
        document.getElementById('search-results').innerHTML = '';
        return;
    };
    searchTimeout = setTimeout(async () => {
        try {
            const results = await apiRequest(`/foods/search?q=${query}`);
            renderSearchResults(results);
        } catch (error) {
            console.error("Food search failed:", error);
        }
    }, 300);
});

document.getElementById('add-log-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const food_id = parseInt(document.getElementById('selected-food-id').value);
    const grams = parseFloat(document.getElementById('grams').value);

    if (!food_id || !grams) return;

    try {
        await apiRequest('/log/add', 'POST', { food_id, grams });
        const dailyLog = await apiRequest('/log/today');
        state.dailyLog = dailyLog;
        renderDashboard();
        showPage('diary');
        document.getElementById('food-search-input').value = '';
        document.getElementById('search-results').innerHTML = '';
        document.getElementById('selected-food-view').classList.add('hidden');
    } catch (error) {
        console.error("Failed to add food log:", error);
    }
});

// --- INITIALIZATION ---
async function initApp() {
    console.log('[Init] App initialization started.');
    try {
        const userProfile = await apiRequest('/user/profile');
        if (userProfile) {
            state.userProfile = userProfile;
            const dailyLog = await apiRequest('/log/today');
            state.dailyLog = dailyLog;
            views.appShell.classList.remove('hidden');
            views.userSetup.classList.add('hidden');
            renderDashboard();
            renderProfile();
            showPage('diary');
        } else {
            views.userSetup.classList.remove('hidden');
            views.appShell.classList.add('hidden');
        }
    } catch (error) {
        console.error("Initialization failed:", error);
        views.userSetup.classList.remove('hidden');
        views.appShell.classList.add('hidden');
    }
}

initApp();
