chrome.runtime.onInstalled.addListener(() => {
    console.log("CyberShield Browser Security installed.");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type !== "ANALYZE_PAGE") {
        return;
    }

    const data = message.data || {};

    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: data.url || "",
            html: data.html || ""
        })
    })
        .then(async (response) => {
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Analysis failed");
            }

            return result;
        })
        .then((result) => {
            console.log("CyberShield analysis:", result);

            sendResponse({
                result: result
            });
        })
        .catch((error) => {
            console.error("CyberShield API error:", error);

            sendResponse({
                error: error.message
            });
        });

    // Keep the message channel open for the asynchronous fetch().
    return true;
});