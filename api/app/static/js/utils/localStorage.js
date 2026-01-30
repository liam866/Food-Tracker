const LLM_RESPONSE_KEY = "llmResponse";

export function saveLLMResponse(response) {
    const dataToSave = {
        timestamp: new Date().toISOString().split("T")[0], // YYYY-MM-DD
        response: response
    };
    localStorage.setItem(LLM_RESPONSE_KEY, JSON.stringify(dataToSave));
    console.log("[LocalStorage] LLM response saved.", dataToSave);
}

export function loadLLMResponse() {
    const savedData = localStorage.getItem(LLM_RESPONSE_KEY);
    if (savedData) {
        const parsedData = JSON.parse(savedData);
        const today = new Date().toISOString().split("T")[0];
        if (parsedData.timestamp === today) {
            console.log("[LocalStorage] Valid LLM response loaded for today.", parsedData.response);
            return parsedData.response;
        } else {
            console.log("[LocalStorage] Stale LLM response found (not from today). Clearing.");
            localStorage.removeItem(LLM_RESPONSE_KEY);
        }
    }
    console.log("[LocalStorage] No valid LLM response found.");
    return null;
}

export function clearLLMResponse() {
    localStorage.removeItem(LLM_RESPONSE_KEY);
    console.log("[LocalStorage] LLM response cleared from local storage.");
}
