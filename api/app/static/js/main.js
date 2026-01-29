import { state } from './state.js';
import { apiRequest } from './api.js';
import { showPage, showProfileView } from './navigation.js';
import { renderDashboard } from './components/dashboard.js';
import { renderProfile } from './components/profile.js';
import { renderSearchResults, renderFoodDetail } from './components/quickAdd.js';
import { renderLogList } from './components/log.js';

// --- DOM ELEMENT REFERENCES ---
export const views = { userSetup: document.getElementById('user-setup-view'), appShell: document.getElementById('app-shell') };
export const pages = { diary: document.getElementById('diary-page'), quickAdd: document.getElementById('quick-add-page'), log: document.getElementById('log-page'), scan: document.getElementById('scan-page'), plan: document.getElementById('plan-page'), profile: document.getElementById('profile-page'), foodDetail: document.getElementById('food-detail-page') };
export const profileViews = { main: document.getElementById('profile-main-view'), updateGoals: document.getElementById('update-goals-view'), updateInfo: document.getElementById('update-info-view') };
export const navButtons = document.querySelectorAll('.nav-btn');
export const pageTitle = document.getElementById('page-title');
export const goalButtons = document.querySelectorAll('.goal-btn');
const userSetupForm = document.getElementById('user-setup-form');
const deleteModal = document.getElementById('delete-modal');
const updateInfoForm = document.getElementById('update-info-form');
const addLogForm = document.getElementById('add-log-form');
const foodSearchInput = document.getElementById('food-search-input');
const searchResultsDiv = document.getElementById('search-results');
const gramsInput = document.getElementById('grams'); // Global reference for grams input

// --- EVENT LISTENERS ---
navButtons.forEach(button => button.addEventListener('click', () => showPage(button.dataset.page)));
document.getElementById('quick-add-btn').addEventListener('click', () => {
    showPage('quickAdd');
    foodSearchInput.value = '';
    searchResultsDiv.innerHTML = '';
    const foodDetailPage = document.getElementById('food-detail-page');
    if (foodDetailPage) foodDetailPage.classList.add('hidden');
    if (gramsInput) gramsInput.value = '100'; // Reset grams when entering Quick Add
    state.selectedLogId = null; // Clear selected log when going to Quick Add for a new entry
});
document.getElementById('log-btn').addEventListener('click', () => showPage('log')); // Updated from history-btn
document.getElementById('update-goals-btn').addEventListener('click', () => showProfileView('updateGoals'));
document.getElementById('update-info-btn').addEventListener('click', () => showProfileView('updateInfo'));
document.getElementById('back-button').addEventListener('click', () => {
    console.log('[Back Button] Clicked.');
    if (pages.profile && !pages.profile.classList.contains('hidden') && profileViews.main && profileViews.main.classList.contains('hidden')) {
        console.log('[Back Button] Currently in a profile sub-view, returning to main profile.');
        showProfileView('main');
    } else if (pages.foodDetail && !pages.foodDetail.classList.contains('hidden')) {
        console.log('[Back Button] Currently on food detail page. Checking if editing or adding...');
        if (state.selectedLogId !== null) {
            console.log('[Back Button] Editing existing log, returning to Diary.');
            state.selectedLogId = null; // Clear edit state
            showPage('diary');
        } else {
            console.log('[Back Button] Adding new log, returning to Quick Add search.');
            showPage('quickAdd');
        }
    } else {
        console.log('[Back Button] Returning to Diary page.');
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
        // Remove highlighting from all buttons first
        goalButtons.forEach(b => {
            b.classList.remove('bg-slate-900', 'text-white');
            b.classList.add('bg-white', 'border-slate-200');
        });
        // Add highlighting to the clicked button
        btn.classList.add('bg-slate-900', 'text-white');
        btn.classList.remove('bg-white', 'border-slate-200');
        state.selectedGoal = btn.dataset.goal; 
        console.log("Selected goal for update:", state.selectedGoal);
    });
});

document.getElementById('save-goal-btn').addEventListener('click', async () => {
    if (!state.selectedGoal || !state.userProfile) return;
    const { name, age, height_cm, weight_kg, sex } = state.userProfile;
    const updatedProfileData = { name, age, height_cm, weight_kg, sex, goal: state.selectedGoal };
    try {
        console.log("Saving updated goal:", updatedProfileData);
        const updatedProfile = await apiRequest('/user/profile', 'POST', updatedProfileData);
        state.userProfile = updatedProfile;
        await initApp(); // Re-initialize to update dashboard and profile with new calorie/protein targets
        showProfileView('main');
        console.log("Goal updated successfully. Re-initialized app and showed main profile view.");
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
        console.log("Saving updated user info:", fullProfile);
        const updatedProfile = await apiRequest('/user/profile', 'POST', fullProfile);
        state.userProfile = updatedProfile;
        await initApp(); // Re-initialize to update dashboard and profile with new calorie/protein targets
        showProfileView('main');
        console.log("User info updated successfully. Re-initialized app and showed main profile view.");
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
        console.log("Creating user profile:", profileData);
        await apiRequest('/user/profile', 'POST', profileData);
        await initApp();
        console.log("User profile created and app initialized.");
    } catch (error) { console.error("Failed to create profile:", error); }
});

let searchTimeout;
document.getElementById('food-search-input').addEventListener("input", (e) => {
    console.log("[QuickAdd] Food search input changed:", e.target.value);
    clearTimeout(searchTimeout);
    const query = e.target.value;

    if (query.length < 2) {
        console.log("[QuickAdd] Search query too short. Clearing results.");
        searchResultsDiv.innerHTML = "";
        return;
    }

    searchTimeout = setTimeout(async () => {
        console.log("[QuickAdd] Performing food search for query:", query);
        try {
            const results = await apiRequest(`/foods/search?q=${query}`);
            console.log("[QuickAdd] Food search results received:", results);
            renderSearchResults(results);
        } catch (error) { console.error("[QuickAdd] Food search failed:", error); }
    }, 300);
});

addLogForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const food_id = parseInt(document.getElementById("food-detail-id").value);
    const grams = parseFloat(document.getElementById("grams").value);

    if (!food_id || !grams) return;

    let apiEndpoint = '';
    let apiMethod = '';

    if (state.selectedLogId !== null) {
        console.log(`[FoodLog] Updating existing food log ID: ${state.selectedLogId}`);
        apiEndpoint = `/log/${state.selectedLogId}`;
        apiMethod = "PUT";
    } else {
        console.log("[FoodLog] Adding new food log.");
        apiEndpoint = "/log/add";
        apiMethod = "POST";
    }

    try {
        await apiRequest(apiEndpoint, apiMethod, { food_id, grams });
        state.selectedLogId = null; // Clear selected log after update/add
        await initApp();
        showPage("diary");
        console.log("[FoodLog] Food log saved and app re-initialized. Redirecting to diary.");
    } catch (error) { console.error("Failed to save food log:", error); }
});

document.getElementById("grams").addEventListener("input", () => {
    const foodId = document.getElementById("food-detail-id").value;
    if (foodId && state.foodCache[foodId]) {
        renderFoodDetail(state.foodCache[foodId]);
    }
});

// --- INITIALIZATION ---
export async function initApp() {
    console.log("[Init] App initialization started.");
    try {
        const userProfile = await apiRequest("/user/profile");
        console.log("[Init] User profile fetched:", userProfile);
        if (userProfile) {
            state.userProfile = userProfile;
            console.log("[Init] State.userProfile updated. Calorie Target:", state.userProfile.calorie_target, "Protein Target:", state.userProfile.protein_target);
            const dailyLog = await apiRequest("/log/today");
            state.dailyLog = dailyLog;
            console.log("[Init] Daily log fetched. State.dailyLog:", state.dailyLog);
            views.appShell.classList.remove("hidden");
            views.userSetup.classList.add("hidden");
            console.log("[Init] Views updated. Rendering dashboard and profile.");
            renderDashboard();
            renderProfile();
            showPage("diary");
        } else {
            console.log("[Init] No user profile found. Showing setup view.");
            views.userSetup.classList.remove("hidden");
            views.appShell.classList.add("hidden");
        }
        console.log("[Init] App initialization completed.");
    } catch (error) {
        console.error("[Init] Initialization failed:", error);
        views.userSetup.classList.remove("hidden");
        views.appShell.classList.add("hidden");
    }
}

initApp();
