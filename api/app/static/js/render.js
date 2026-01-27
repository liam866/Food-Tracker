import { state } from './state.js';
import { goalButtons } from './main.js';

export function renderDashboard() {
    if (!state.userProfile || !state.dailyLog) return;
    const { calorie_target, protein_target } = state.userProfile;
    const { totals, logs } = state.dailyLog;

    document.getElementById('calories-tracked').textContent = Math.round(totals.calories);
    document.getElementById('calories-target').textContent = Math.round(calorie_target);
    const calPercent = Math.min(100, (totals.calories / calorie_target) * 100);
    document.getElementById('calories-progress').style.width = `${calPercent}%`;

    document.getElementById('protein-tracked').textContent = Math.round(totals.protein);
    document.getElementById('protein-target').textContent = Math.round(protein_target);
    const proPercent = Math.min(100, (totals.protein / protein_target) * 100);
    document.getElementById('protein-progress').style.width = `${proPercent}%`;
    
    renderLogList(logs, 'food-log-list');
    renderLogList(logs, 'history-log-list');
}

export function renderLogList(logs, listId) {
    const listEl = document.getElementById(listId);
    listEl.innerHTML = '';
    if (!logs || logs.length === 0) {
        listEl.innerHTML = `<p class="text-center text-slate-500 text-sm">No food logged yet.</p>`;
        return;
    }
    logs.forEach(log => {
        const logItem = document.createElement('div');
        logItem.className = 'bg-white p-4 rounded-xl border border-slate-200 flex justify-between items-center';
        logItem.innerHTML = `
            <div>
                <p class="font-semibold text-slate-800">${log.name}</p>
                <p class="text-sm text-slate-500">${log.grams}g</p>
            </div>
            <div class="text-right">
                <p class="font-medium text-emerald-600">${Math.round(log.calories)} kcal</p>
                <div class="text-xs text-slate-400">
                    <span>Protein: ${Math.round(log.protein)}g</span>
                </div>
            </div>
        `;
        listEl.appendChild(logItem);
    });
}

export function renderProfile() {
    if (!state.userProfile) return;
    document.getElementById('profile-name').textContent = state.userProfile.name;
    
    // Populate update-info form
    document.getElementById('update-name').value = state.userProfile.name;
    document.getElementById('update-age').value = state.userProfile.age;
    document.getElementById('update-height').value = state.userProfile.height_cm;
    document.getElementById('update-weight').value = state.userProfile.weight_kg;
    document.getElementById('update-sex').value = state.userProfile.sex;

    // Highlight current goal
    state.selectedGoal = state.userProfile.goal;
    goalButtons.forEach(b => {
         const isSelected = b.dataset.goal === state.selectedGoal;
         b.classList.toggle('bg-slate-900', isSelected);
         b.classList.toggle('text-white', isSelected);
         b.classList.toggle('bg-white', !isSelected);
         b.classList.toggle('border-slate-200', !isSelected);
    });
}

export function renderSearchResults(foods) {
    const resultsEl = document.getElementById('search-results');
    resultsEl.innerHTML = '';
    if (!foods || foods.length === 0) {
        resultsEl.innerHTML = `<p class="text-center text-slate-500 text-sm">No results found.</p>`;
        return;
    }
    foods.forEach(food => {
        const item = document.createElement('button');
        item.className = 'w-full text-left hover:bg-slate-100 rounded-lg px-4 py-2 transition';
        item.textContent = food.name;
        item.onclick = () => {
            state.foodCache[food.id] = food;
            updateSelectedFoodView(food);
        };
        resultsEl.appendChild(item);
    });
}

export function updateSelectedFoodView(food) {
    const grams = parseFloat(document.getElementById('grams').value) || 100;
    const multiplier = grams / 100;

    document.getElementById('selected-food-view').classList.remove('hidden');
    document.getElementById('selected-food-name').textContent = food.name;
    document.getElementById('selected-food-id').value = food.id;
    
    document.getElementById('nutrition-calories').textContent = Math.round(food.calories_per_100g * multiplier);
    document.getElementById('nutrition-protein').textContent = Math.round(food.protein_per_100g * multiplier);
    document.getElementById('nutrition-carbs').textContent = Math.round(food.carbs_per_100g * multiplier);
    document.getElementById('nutrition-fat').textContent = Math.round(food.fat_per_100g * multiplier);
}
