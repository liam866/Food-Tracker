import { state } from "../state.js";
import { apiRequest } from "../api.js";
import { showPage } from "../navigation.js";
import { renderFoodDetail } from "./quickAdd.js";
import { initApp } from "../main.js"; // Import initApp directly

export function renderLogList(logs, listId) {
    const listEl = document.getElementById(listId);
    if (!listEl) {
        console.error(`[Log] List element with ID ${listId} not found.`);
        return;
    }
    listEl.innerHTML = "";

    if (!logs || logs.length === 0) {
        listEl.innerHTML =
            `<p class="text-center text-slate-500 text-sm">No food logged yet.</p>`;
        return;
    }

    logs.forEach((log) => {
        const logItem = document.createElement("div");
        logItem.className =
            "bg-white px-4 py-5 rounded-xl border border-slate-200 flex justify-between items-center";
        logItem.innerHTML = `
            <div class="space-y-1">
                <p class="font-semibold text-slate-800">${log.name}</p>
                <p class="text-sm text-slate-500">${log.grams}g</p>
            </div>
            <div class="flex items-center space-x-4">
                <div class="text-right space-y-1">
                    <p class="font-medium text-emerald-600">${Math.round(
                        log.calories
                    )} kcal</p>
                    <div class="text-xs text-slate-400">
                        <span>Protein: ${Math.round(log.protein)}g</span>
                    </div>
                </div>
                <div class="flex flex-col space-y-1">
                    <button class="text-slate-400 hover:text-slate-600 transition"
                            data-log-id="${log.id}"
                            data-food-id="${log.food_id}"
                            data-grams="${log.grams}"
                            data-food-name="${log.name}"
                            id="edit-log-${log.id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="text-rose-400 hover:text-rose-600 transition"
                            data-log-id="${log.id}"
                            id="delete-log-${log.id}">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
        `;
        listEl.append(logItem);

        // Attach event listeners to the new buttons
        document.getElementById(`edit-log-${log.id}`).addEventListener("click", async () => {
            console.log(`[Log] Edit button clicked for log ID: ${log.id}`);
            state.selectedLogId = log.id;
            let food = state.foodCache[log.food_id];
            if (!food) {
                console.log(`[Log] Food ID ${log.food_id} not in cache. Fetching from API.`);
                try {
                    food = await apiRequest(`/foods/${log.food_id}`);
                    state.foodCache[log.food_id] = food; // Add to cache
                    console.log(`[Log] Fetched food ID ${log.food_id}:`, food);
                } catch (error) {
                    console.error(`[Log] Failed to fetch food ID ${log.food_id}:`, error);
                    return; // Stop if food cannot be fetched
                }
            }
            
            // Set grams input on food detail page
            const gramsInput = document.getElementById("grams");
            if(gramsInput) gramsInput.value = log.grams;

            showPage("foodDetail");
            renderFoodDetail(food);
        });

        document.getElementById(`delete-log-${log.id}`).addEventListener("click", async () => {
            console.log(`[Log] Delete button clicked for log ID: ${log.id}`);
            if (confirm("Are you sure you want to delete this food log entry?")) {
                try {
                    await apiRequest(`/log/${log.id}`, "DELETE");
                    console.log(`[Log] Log ID ${log.id} deleted successfully. Re-initializing app.`);
                    state.selectedLogId = null; // Clear selected log after deletion
                    initApp(); // Call initApp directly
                } catch (error) {
                    console.error(`[Log] Failed to delete log ID ${log.id}:`, error);
                }
            }
        });
    });
}
