console.log("CyberShield browser security active.");

// Collect passive webpage information.
// We analyze page structure only and do not collect passwords,
// cookies, form values, or other user-entered data.
function collectPageData() {
    const clone = document.documentElement.cloneNode(true);

    // Remove user-entered values from copied HTML.
    clone.querySelectorAll("input, textarea").forEach((element) => {
        element.removeAttribute("value");
        element.textContent = "";
    });

    // Limit the amount of HTML sent to the local API.
    let html = clone.outerHTML || "";

    const MAX_HTML_SIZE = 200000;

    if (html.length > MAX_HTML_SIZE) {
        html = html.substring(0, MAX_HTML_SIZE);
    }

    return {
        url: window.location.href,
        html: html
    };
}

// Send the current page to the background service worker.
function analyzeCurrentPage() {
    const pageData = collectPageData();

    chrome.runtime.sendMessage(
        {
            type: "ANALYZE_PAGE",
            data: pageData
        },
        (response) => {
            if (chrome.runtime.lastError) {
                console.error(
                    "CyberShield:",
                    chrome.runtime.lastError.message
                );
                return;
            }

            if (response?.error) {
                console.error(
                    "CyberShield analysis error:",
                    response.error
                );
                return;
            }

            if (response?.result) {
                console.log(
                    "CyberShield analysis result:",
                    response.result
                );
            }
        }
    );
}

// Wait until the page has loaded before analyzing it.
if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        analyzeCurrentPage,
        { once: true }
    );
} else {
    analyzeCurrentPage();
}
chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {
        if (message.type !== "GET_PAGE_DATA") {
            return;
        }

        const clone =
            document.documentElement.cloneNode(true);

        // Never send user-entered values.
        clone.querySelectorAll(
            "input, textarea"
        ).forEach(element => {
            element.removeAttribute("value");
            element.textContent = "";
        });

        let html = clone.outerHTML || "";

        const MAX_HTML_SIZE = 200000;

        if (html.length > MAX_HTML_SIZE) {
            html = html.substring(0, MAX_HTML_SIZE);
        }

        sendResponse({
            url: window.location.href,
            html: html
        });
    }
);