import { pages, profileViews, navButtons, pageTitle } from "./main.js";
import { state } from "./state.js";
import { renderLogList } from "./components/log.js";

export function showPage(pageName) {
    console.log(`[Navigation] Showing page: ${pageName}`);
    Object.values(pages).forEach((p) => {
        if (p) {
            p.classList.add("hidden");
        }
    });
    if (pages[pageName]) {
        pages[pageName].classList.remove("hidden");
        pageTitle.textContent = pageName.charAt(0).toUpperCase() + pageName.slice(1);
    }
    if (pageName === "diary") pageTitle.textContent = "Today";

    navButtons.forEach((btn) => {
        const isActive = btn.dataset.page === pageName;
        btn.classList.toggle("text-slate-900", isActive);
        btn.classList.toggle("text-slate-400", !isActive);
    });

    if (pageName === "profile") {
        showProfileView("main");
    }

    const backButton = document.getElementById("back-button");
    if (backButton) {
        if (pageName === "quickAdd" || pageName === "history" || pageName === "foodDetail") {
            backButton.classList.remove("hidden");
        } else {
            backButton.classList.add("hidden");
        }
    }

    // Specifically for the History page to load logs when navigated to
    if (pageName === "history" && state.dailyLog) {
        renderLogList(state.dailyLog.logs, "history-log-list");
    }
}

export function showProfileView(viewName) {
    console.log(`[Navigation] Showing profile view: ${viewName}`);
    Object.values(profileViews).forEach((view) => {
        if (view) {
            view.classList.add("hidden");
        }
    });
    if (profileViews[viewName]) {
        profileViews[viewName].classList.remove("hidden");
    }
    const backButton = document.getElementById("back-button");
    if (backButton) {
        backButton.classList.toggle("hidden", viewName === "main");
    }
    pageTitle.textContent = viewName === "main" ? "Profile" : `Update ${viewName.charAt(0).toUpperCase() + viewName.slice(6)}`;
}

export function showFoodDetailPage(food) {
    showPage("foodDetail");
}
