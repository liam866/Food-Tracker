export function renderAiOverview(result) {
    console.log("[AI Overview] Rendering AI overview with result:", result);
    const aiOverviewMessages = document.getElementById("ai-overview-messages");
    if (!aiOverviewMessages) {
        console.error("[AI Overview] AI Overview messages element not found during rendering.");
        return;
    }

    if (!result || result.type === "empty") {
        console.log("[AI Overview] Displaying default or empty message.");
        aiOverviewMessages.innerHTML = `
            <li class="text-center text-slate-500">
                ${result?.message ?? "Start logging"}
            </li>
        `;
        return;
    }

    const { progress, improvement, encouragement } = result.data;
    console.log("[AI Overview] Displaying AI generated content.");
    aiOverviewMessages.innerHTML = `
        <li><strong>Progress:</strong> ${progress}</li>
        <li><strong>Improvement:</strong> ${improvement}</li>
        <li><strong>Encouragement:</strong> ${encouragement}</li>
    `;
}
