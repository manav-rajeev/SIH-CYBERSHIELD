const API_URL = "http://127.0.0.1:5000/analyze";


async function getCurrentTab() {
    const tabs = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    return tabs[0];
}


function showLoading() {
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result").classList.add("hidden");
    document.getElementById("error").classList.add("hidden");
}


function showError(message) {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("result").classList.add("hidden");

    const error = document.getElementById("error");
    const errorMessage = document.getElementById("errorMessage");

    errorMessage.textContent = message;
    error.classList.remove("hidden");
}


function setStatus(classification) {
    const card = document.getElementById("statusCard");
    const icon = document.getElementById("statusIcon");
    const title = document.getElementById("classification");

    card.classList.remove(
        "status-safe",
        "status-suspicious",
        "status-danger"
    );

    icon.classList.remove(
        "status-safe",
        "status-suspicious",
        "status-danger"
    );

    if (classification === "SAFE") {
        title.textContent = "SAFE";
        icon.textContent = "✓";

        card.classList.add("status-safe");
        icon.classList.add("status-safe");

    } else if (classification === "SUSPICIOUS") {
        title.textContent = "SUSPICIOUS";
        icon.textContent = "⚠";

        card.classList.add("status-suspicious");
        icon.classList.add("status-suspicious");

    } else {
        title.textContent = classification;
        icon.textContent = "⚠";

        card.classList.add("status-danger");
        icon.classList.add("status-danger");
    }
}


function renderReasons(reasons) {
    const container = document.getElementById("reasons");

    container.innerHTML = "";

    if (!reasons || reasons.length === 0) {
        const row = document.createElement("div");
        row.className = "reason";
        row.textContent = "No significant indicators detected.";
        container.appendChild(row);
        return;
    }

    reasons.forEach(reason => {
        const row = document.createElement("div");
        row.className = "reason";

        const icon = document.createElement("span");
        icon.className = "reason-icon";
        icon.textContent = "⚠";

        const text = document.createElement("span");
        text.textContent = reason;

        row.appendChild(icon);
        row.appendChild(text);

        container.appendChild(row);
    });
}


function formatName(name) {
    return name
        .replaceAll("_", " ")
        .replace(/\b\w/g, char => char.toUpperCase());
}


function renderFeatures(features, title = "URL Analysis") {
    const container = document.getElementById("features");

    const heading = document.createElement("div");
    heading.className = "feature-section-title";
    heading.textContent = title;

    container.appendChild(heading);

    const importantFeatures = [
        "uses_https",
        "url_length",
        "domain_length",
        "subdomain_count",
        "has_ip_address",
        "has_at_symbol",
        "has_encoded_characters",
        "has_port",
        "suspicious_keyword_count",
        "query_parameter_count"
    ];

    importantFeatures.forEach(key => {
        if (!features || !(key in features)) {
            return;
        }

        const row = document.createElement("div");
        row.className = "feature-row";

        const name = document.createElement("span");
        name.className = "feature-name";
        name.textContent = formatName(key);

        const value = document.createElement("span");
        value.className = "feature-value";
        value.textContent = String(features[key]);

        row.appendChild(name);
        row.appendChild(value);

        container.appendChild(row);
    });
}


function renderWebsiteFeatures(features) {
    const container = document.getElementById("features");

    const heading = document.createElement("div");
    heading.className = "feature-section-title";
    heading.textContent = "Website Analysis";

    container.appendChild(heading);

    const importantFeatures = [
        "form_count",
        "password_field_count",
        "iframe_count",
        "script_count",
        "external_script_count",
        "hidden_element_count",
        "suspicious_keyword_count",
        "form_action_count",
        "meta_refresh",
        "obfuscation_detected"
    ];

    importantFeatures.forEach(key => {
        if (!features || !(key in features)) {
            return;
        }

        const row = document.createElement("div");
        row.className = "feature-row";

        const name = document.createElement("span");
        name.className = "feature-name";
        name.textContent = formatName(key);

        const value = document.createElement("span");
        value.className = "feature-value";

        if (typeof features[key] === "boolean") {
            value.textContent = features[key] ? "Yes" : "No";
        } else {
            value.textContent = String(features[key]);
        }

        row.appendChild(name);
        row.appendChild(value);

        container.appendChild(row);
    });
}


function renderResult(result) {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("error").classList.add("hidden");
    document.getElementById("result").classList.remove("hidden");

    document.getElementById("score").textContent = result.score;

    document.getElementById("currentUrl").textContent = result.url;

    setStatus(result.classification);

    renderReasons(result.reasons);

    const featuresContainer = document.getElementById("features");
    featuresContainer.innerHTML = "";

    // Phase 5: URL features
    renderFeatures(
        result.url_features || {},
        "URL Analysis"
    );

    // Phase 5: Website/HTML features
    renderWebsiteFeatures(
        result.website_features || {}
    );
}


async function analyzeCurrentWebsite() {
    showLoading();

    try {
        const tab = await getCurrentTab();

        if (!tab || !tab.url) {
            throw new Error(
                "Unable to read the current website URL."
            );
        }

        /*
         * Ask the content script for the current page's
         * URL and HTML structure.
         */
        let pageData = null;

        try {
            pageData = await new Promise((resolve, reject) => {
                chrome.tabs.sendMessage(
                    tab.id,
                    {
                        type: "GET_PAGE_DATA"
                    },
                    response => {
                        if (chrome.runtime.lastError) {
                            reject(
                                new Error(
                                    chrome.runtime.lastError.message
                                )
                            );
                            return;
                        }

                        resolve(response);
                    }
                );
            });
        } catch {
            // Some browser/system pages do not allow content scripts.
            // Fall back to URL-only analysis.
            pageData = {
                url: tab.url,
                html: ""
            };
        }

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: pageData?.url || tab.url,
                html: pageData?.html || ""
            })
        });

        if (!response.ok) {
            let message =
                "The CyberShield API returned an error.";

            try {
                const data = await response.json();

                if (data.error) {
                    message = data.error;
                }
            } catch {
                // Ignore invalid error responses.
            }

            throw new Error(message);
        }

        const result = await response.json();

        renderResult(result);

    } catch (error) {
        console.error(
            "CyberShield analysis error:",
            error
        );

        showError(
            `${error.message} Make sure browser_api.py is running.`
        );
    }
}


document.addEventListener("DOMContentLoaded", () => {
    analyzeCurrentWebsite();

    const reanalyze =
        document.getElementById("reanalyze");

    if (reanalyze) {
        reanalyze.addEventListener(
            "click",
            analyzeCurrentWebsite
        );
    }
});