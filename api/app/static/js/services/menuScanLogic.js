import { apiRequest } from "../api.js";

export async function analyzeMenuImage(file) {
    console.log("[Menu Logic] Initiating menu analysis for file:", file.name);
    
    const formData = new FormData();
    formData.append("image", file);

    try {
        // We use fetch directly or adapt apiRequest to handle FormData
        // apiRequest uses JSON.stringify by default, so we'll use a manual fetch here
        const response = await fetch("/menu/analyze", {
            method: "POST",
            body: formData,
            // Headers like Content-Type are automatically set by fetch for FormData
        });

        if (!response.ok) {
            throw new Error(`Analysis failed with status ${response.status}`);
        }

        const result = await response.json();
        console.log("[Menu Logic] Analysis successful:", result);
        return result;
    } catch (error) {
        console.error("[Menu Logic] Error during analysis:", error);
        throw error;
    }
}
