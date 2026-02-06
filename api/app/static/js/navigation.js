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
        // Remove existing Tailwind text color classes and apply custom orange/black classes
        btn.classList.remove("text-slate-900"); // Remove default active color
        btn.classList.remove("text-slate-400"); // Remove default inactive color
        btn.classList.toggle("navigation-word-orange", isActive); // Apply orange if active
        btn.classList.toggle("navigation-word-black", !isActive); // Apply black if inactive
    });

    if (pageName === "profile") {
        showProfileView("main");
    }

    const backButton = document.getElementById("back-button");
    if (backButton) {
        if (pageName === "quickAdd" || pageName === "log" || pageName === "foodDetail") {
            backButton.classList.remove("hidden");
        }
        else {
            backButton.classList.add("hidden");
        }
    }

    // Specifically for the Log page to load logs when navigated to
    if (pageName === "log" && state.dailyLog) {
        console.log("[Navigation] Rendering food logs for log page.");
        renderLogList(state.dailyLog.logs, "log-list");
    }
    else if (pageName === "log") {
        // If dailyLog is null, clear the list or show a message
        const logListEl = document.getElementById("log-list");
        if (logListEl) {
            logListEl.innerHTML = `<p class="text-center text-slate-500 text-sm">No food logged yet.</p>`;
        }
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