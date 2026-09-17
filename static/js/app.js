/**
 * Weather-Based Activity Agent - Client Script
 * -------------------------------------------
 * Handles asynchronous form submission, quick preset loading, and dynamic DOM updates.
 */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("weather-form");
    const submitBtn = document.getElementById("btn-submit");
    const errorBox = document.getElementById("error-box");
    const errorList = document.getElementById("error-list");

    const emptyState = document.getElementById("empty-state");
    const resultsContent = document.getElementById("results-content");

    // Dynamic result elements
    const verdictBanner = document.getElementById("verdict-banner");
    const verdictTag = document.getElementById("verdict-tag");
    const verdictTitle = document.getElementById("verdict-title");
    const reasoningText = document.getElementById("reasoning-text");
    const reasonsList = document.getElementById("reasons-list");
    const cautionContainer = document.getElementById("caution-container");
    const cautionList = document.getElementById("caution-list");
    const primaryActivitiesGrid = document.getElementById("primary-activities");
    const outdoorList = document.getElementById("outdoor-list");
    const indoorList = document.getElementById("indoor-list");

    // Inputs
    const tempInput = document.getElementById("temperature");
    const condSelect = document.getElementById("condition");
    const humInput = document.getElementById("humidity");
    const windInput = document.getElementById("wind_speed");

    // Quick Preset Buttons
    const presetButtons = document.querySelectorAll(".btn-preset");
    presetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tempInput.value = btn.dataset.temp;
            condSelect.value = btn.dataset.cond;
            humInput.value = btn.dataset.hum;
            windInput.value = btn.dataset.wind;

            // Visual feedback on clicked button
            presetButtons.forEach(b => b.style.outline = "none");
            btn.style.outline = "2px solid var(--accent-blue)";

            // Automatically trigger evaluation for instant gratification
            submitWeatherEvaluation();
        });
    });

    // Form Submit Handler
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        submitWeatherEvaluation();
    });

    async function submitWeatherEvaluation() {
        hideErrors();
        setLoadingState(true);

        const payload = {
            temperature: parseFloat(tempInput.value),
            condition: condSelect.value,
            humidity: parseFloat(humInput.value),
            wind_speed: parseFloat(windInput.value)
        };

        try {
            const response = await fetch("/api/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                const errors = data.errors || ["An error occurred while evaluating weather percepts."];
                showErrors(errors);
            } else {
                renderResults(data.data);
            }
        } catch (error) {
            showErrors([`Network or server error: ${error.message}`]);
        } finally {
            setLoadingState(false);
        }
    }

    function renderResults(decision) {
        // Toggle view containers
        if (emptyState) emptyState.classList.add("hidden");
        resultsContent.classList.remove("hidden");

        // 1. Verdict Banner
        verdictBanner.className = `verdict-banner banner-${decision.verdict_color}`;
        verdictTag.textContent = decision.summary_badge;
        verdictTitle.textContent = decision.classification;

        // 2. Reasoning Explanation
        reasoningText.textContent = decision.explanation;

        // 3. Reasons Rule Trace
        reasonsList.innerHTML = "";
        (decision.reasons || []).forEach(r => {
            const li = document.createElement("li");
            li.textContent = r;
            reasonsList.appendChild(li);
        });

        // 4. Caution Notes
        cautionList.innerHTML = "";
        if (decision.caution_notes && decision.caution_notes.length > 0) {
            decision.caution_notes.forEach(c => {
                const li = document.createElement("li");
                li.textContent = c;
                cautionList.appendChild(li);
            });
            cautionContainer.classList.remove("hidden");
        } else {
            cautionContainer.classList.add("hidden");
        }

        // 5. Primary Activities
        primaryActivitiesGrid.innerHTML = "";
        (decision.primary_activities || []).forEach(act => {
            const card = document.createElement("div");
            card.className = "activity-card primary-card";
            card.innerHTML = `
                <div class="activity-icon">${escapeHtml(act.icon)}</div>
                <div class="activity-details">
                    <h5>${escapeHtml(act.name)}</h5>
                    <p>${escapeHtml(act.desc)}</p>
                </div>
            `;
            primaryActivitiesGrid.appendChild(card);
        });

        // 6. Outdoor List Pool
        outdoorList.innerHTML = "";
        (decision.outdoor_suggestions || []).forEach(act => {
            const item = document.createElement("div");
            item.className = "pool-item";
            item.innerHTML = `
                <span class="item-icon">${escapeHtml(act.icon)}</span>
                <div>
                    <strong>${escapeHtml(act.name)}</strong>
                    <small>${escapeHtml(act.desc)}</small>
                </div>
            `;
            outdoorList.appendChild(item);
        });

        // 7. Indoor List Pool
        indoorList.innerHTML = "";
        (decision.indoor_suggestions || []).forEach(act => {
            const item = document.createElement("div");
            item.className = "pool-item";
            item.innerHTML = `
                <span class="item-icon">${escapeHtml(act.icon)}</span>
                <div>
                    <strong>${escapeHtml(act.name)}</strong>
                    <small>${escapeHtml(act.desc)}</small>
                </div>
            `;
            indoorList.appendChild(item);
        });

        // Smooth scroll to results on smaller screens
        if (window.innerWidth < 960) {
            resultsContent.scrollIntoView({ behavior: "smooth" });
        }
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span>Agent Reasoning...</span> <span class="spinner">⏳</span>`;
        } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<span>Evaluate Weather & Recommend</span> <span class="btn-arrow">→</span>`;
        }
    }

    function showErrors(errors) {
        errorList.innerHTML = "";
        errors.forEach(err => {
            const li = document.createElement("li");
            li.textContent = err;
            errorList.appendChild(li);
        });
        errorBox.classList.remove("hidden");
    }

    function hideErrors() {
        errorBox.classList.add("hidden");
        errorList.innerHTML = "";
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text || "";
        return div.innerHTML;
    }
});
