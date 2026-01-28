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
