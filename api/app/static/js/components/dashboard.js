import { state } from '../state.js';
import { renderLogList } from './log.js';

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
}
