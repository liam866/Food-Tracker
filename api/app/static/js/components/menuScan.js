import { analyzeMenuImage } from "../services/menuScanLogic.js";

export function initMenuScan() {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("menu-file-input");

    if (!dropZone || !fileInput) return;

    dropZone.onclick = () => fileInput.click();

    fileInput.onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            await handleScan(file);
        }
    };

    // Simple drag & drop support
    dropZone.ondragover = (e) => {
        e.preventDefault();
        dropZone.classList.add("border-slate-400");
    };

    dropZone.ondragleave = () => {
        dropZone.classList.remove("border-slate-400");
    };

    dropZone.ondrop = async (e) => {
        e.preventDefault();
        dropZone.classList.remove("border-slate-400");
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith("image/")) {
            await handleScan(file);
        }
    };
}

async function handleScan(file) {
    console.log("[Menu Component] Starting scan for:", file.name);
    const resultsContainer = document.getElementById("menu-analysis-results");
    const recommendationsList = document.getElementById("recommendations-container");
    const loadingIndicator = document.getElementById("menu-loading-indicator");

    resultsContainer.classList.remove("hidden");
    recommendationsList.innerHTML = "";
    loadingIndicator.classList.remove("hidden");

    try {
        const result = await analyzeMenuImage(file);
        renderRecommendations(result.recommendations);
    } catch (error) {
        console.error("[Menu Component] Scan failed:", error);
        recommendationsList.innerHTML = `
            <div class="p-4 bg-rose-50 text-rose-600 rounded-xl text-sm border border-rose-100">
                Failed to analyze menu. Please try again with a clearer image.
            </div>
        `;
    } finally {
        loadingIndicator.classList.add("hidden");
    }
}

function renderRecommendations(recommendations) {
    const recommendationsList = document.getElementById("recommendations-container");
    
    if (!recommendations || recommendations.length === 0) {
        recommendationsList.innerHTML = `
            <div class="p-4 bg-slate-100 text-slate-600 rounded-xl text-sm text-center">
                No recommendations found. Try a different image.
            </div>
        `;
        return;
    }

    recommendationsList.innerHTML = recommendations.map(rec => {
        const contextHtml = rec.context && rec.context.length > 0 
            ? `
                <div class="mt-3 pt-3 border-t border-slate-100">
                    <p class="text-[10px] font-medium text-slate-400 uppercase tracking-wider mb-2">Grounded Context</p>
                    <ul class="space-y-1">
                        ${rec.context.map(ctx => `
                            <li class="text-xs text-slate-500 flex justify-between">
                                <span>${ctx.food_name}</span>
                                <span class="font-medium text-slate-700">${Math.round(ctx.calories)} kcal | ${Math.round(ctx.protein)}g protein</span>
                            </li>
                        `).join("")}
                    </ul>
                </div>
            `
            : "";

        return `
            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm animate-in fade-in slide-in-from-bottom-2 duration-300">
                <h3 class="font-semibold text-slate-900 mb-1">${rec.name}</h3>
                <p class="text-sm text-slate-600 leading-relaxed">${rec.reasoning}</p>
                ${contextHtml}
            </div>
        `;
    }).join("");
}
