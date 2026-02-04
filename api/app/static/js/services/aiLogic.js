import { apiRequest } from "../api.js";
import { state } from "../state.js";
import { saveLLMResponse, loadLLMResponse, clearLLMResponse } from "../utils/localStorage.js";
import { setAiOverviewLoadingState } from "../components/aiOverview.js";

export async function getAiOverviewData(forceNewRequest = false) {
    console.log(`[AI Logic] Initiating AI overview data retrieval. Force new request: ${forceNewRequest}`);

    let aiResponseData = null;

    if (!forceNewRequest) {
        const savedResponse = loadLLMResponse();
        if (savedResponse) {
            console.log("[AI Logic] Returning saved LLM response for today.");
            return {
                type: "ai",
                data: savedResponse
            };
        }
    }

    const latestLog = state.dailyLog?.logs?.[0];

    // No logs at all
    if (!latestLog) {
        console.log("[AI Logic] No food logs found. Returning default 'Start logging' message and clearing saved response.");
        clearLLMResponse();
        return {
            type: "empty",
            message: "Start logging"
        };
    }

        const logDateString = new Date(latestLog.datetime).toISOString().split('T')[0];
        const todayDateString = new Date().toISOString().split('T')[0];

        const isToday = logDateString === todayDateString;

        if (!isToday) {
            console.log(`[AI Logic] Log date (${logDateString}) does not match today (${todayDateString}).`);
            clearLLMResponse();
            return {
                type: "empty",
                message: "Start logging"
            };
        }

    // Proceed to make an LLM request
    console.log("[AI Logic] Latest log is from today. Sending LLM request...");
    setAiOverviewLoadingState();
    try {
        aiResponseData = await apiRequest("/chat", "POST");
        console.log("[AI Logic] LLM response received successfully. Saving and returning.", aiResponseData);
        saveLLMResponse(aiResponseData);
        return {
            type: "ai",
            data: aiResponseData
        };
    } catch (error) {
        console.error("[AI Logic] Failed to get LLM response:", error);
        clearLLMResponse(); // Clear on error to prevent displaying stale/failed response
        return {
            type: "empty",
            message: "Failed to load AI overview. Please try again later."
        };
    }
}