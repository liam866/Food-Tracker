import { state } from "../state.js";
import { showPage } from "../navigation.js";

export function renderSearchResults(foods) {
    const resultsEl = document.getElementById("search-results");
    if (!resultsEl) {
        console.error("[QuickAdd] Search results element not found.");
        return;
    }
    resultsEl.innerHTML = "";
    if (!foods || foods.length === 0) {
        resultsEl.innerHTML = `<p class="text-center text-slate-500 text-sm">No results found.</p>`;
        return;
    }
    foods.forEach((food) => {
        const item = document.createElement("button");
        item.className =
            "w-full text-left hover:bg-slate-100 rounded-lg px-4 py-2 transition";
        item.textContent = food.name;
        item.onclick = () => {
            console.log("[QuickAdd] Food selected:", food.name);
            state.foodCache[food.id] = food;
            const gramsInput = document.getElementById("grams");
            if (gramsInput) {
                gramsInput.value = "100"; // Reset grams to 100g
            }
            showPage("foodDetail");
            console.log(
                "[QuickAdd] Navigated to foodDetail page. Deferring renderFoodDetail."
            );
            setTimeout(() => renderFoodDetail(food), 0);
        };
        resultsEl.appendChild(item);
    });
}

export function renderFoodDetail(food) {
    console.log("[QuickAdd] Attempting to render food detail for:", food);

    const foodDetailName = document.getElementById("food-detail-name");
    const foodDetailId = document.getElementById("food-detail-id");
    const gramsInput = document.getElementById("grams");
    const nutritionCalories = document.getElementById("nutrition-calories");
    const nutritionProtein = document.getElementById("nutrition-protein");
    const nutritionCarbs = document.getElementById("nutrition-carbs");
    const nutritionFat = document.getElementById("nutrition-fat");

    if (
        !foodDetailName ||
        !foodDetailId ||
        !gramsInput ||
        !nutritionCalories ||
        !nutritionProtein ||
        !nutritionCarbs ||
        !nutritionFat
    ) {
        console.error(
            "[QuickAdd] One or more food detail elements not found. Cannot render food detail.",
            {
                foodDetailName: !!foodDetailName,
                foodDetailId: !!foodDetailId,
                gramsInput: !!gramsInput,
                nutritionCalories: !!nutritionCalories,
                nutritionProtein: !!nutritionProtein,
                nutritionCarbs: !!nutritionCarbs,
                nutritionFat: !!nutritionFat,
            }
        );
        return;
    }

    const grams = parseFloat(gramsInput.value) || 100;
    const multiplier = grams / 100;

    foodDetailName.textContent = food.name;
    foodDetailId.value = food.id;

    nutritionCalories.textContent = Math.round(food.calories_per_100g * multiplier);
    nutritionProtein.textContent = Math.round(food.protein_per_100g * multiplier);
    nutritionCarbs.textContent = Math.round(food.carbs_per_100g * multiplier);
    nutritionFat.textContent = Math.round(food.fat_per_100g * multiplier);

    console.log("[QuickAdd] Successfully rendered food detail.");
}
