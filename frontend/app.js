document.addEventListener("DOMContentLoaded", () => {
    // API base URL configuration (dynamically fallback to Railway in production)
    const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
        ? ""
        : "https://your-backend-railway-url.railway.app"; // Replace with your Railway deployment URL

    // DOM Elements
    const form = document.getElementById("recommender-form");
    const locationSelect = document.getElementById("location-input");
    const cuisinesContainer = document.getElementById("cuisines-container");
    const ratingSlider = document.getElementById("rating-slider");
    const ratingValue = document.getElementById("rating-value");
    const additionalInput = document.getElementById("additional-input");
    
    const submitBtn = document.getElementById("submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnIcon = submitBtn.querySelector(".btn-icon");
    const btnLoader = submitBtn.querySelector(".btn-loader");
    
    const healthBadge = document.getElementById("health-badge");
    const healthText = document.getElementById("health-text");
    
    // Panel States
    const stateWelcome = document.getElementById("results-welcome");
    const stateLoading = document.getElementById("results-loading");
    const stateEmpty = document.getElementById("results-empty");
    const stateError = document.getElementById("results-error");
    const emptyMessage = document.getElementById("empty-message");
    const errorMessage = document.getElementById("error-message");
    const recommendationsContainer = document.getElementById("recommendations-container");
    const recommendationsList = document.getElementById("recommendations-list");
    const resultsCount = document.getElementById("results-count");
    
    const resetFiltersBtn = document.getElementById("reset-filters-btn");
    const retryBtn = document.getElementById("retry-btn");
    const forceMockBtn = document.getElementById("force-mock-btn");

    // Local state stores
    let locationsList = [];
    let cuisinesList = [];
    let selectedCuisines = [];
    let isGroqConfigured = true;

    // Helper: list of popular default cuisines to show if API fails
    const defaultPopularCuisines = [
        "Italian", "Chinese", "North Indian", "South Indian", "Japanese", 
        "Continental", "Desserts", "Mexican", "Cafe", "Fast Food", "Street Food"
    ];

    // Initialize application
    init();

    async function init() {
        // 1. Check server health
        await checkServerHealth();

        // 2. Fetch autocomplete pools
        await fetchAutocompleteData();

        // 3. Register Event Listeners
        registerListeners();
    }

    // Check system connectivity and AI key setup
    async function checkServerHealth() {
        try {
            const res = await fetch(`${API_BASE}/api/health`);
            if (!res.ok) throw new Error("Health check returned bad response");
            
            const data = await res.json();
            isGroqConfigured = data.groq_configured;
            
            healthBadge.className = "health-badge flex items-center gap-2 px-3 py-1 rounded-full text-xs"; // Reset classes
            
            if (data.status === "healthy") {
                const dot = healthBadge.querySelector(".indicator-dot");
                if (data.groq_configured) {
                    healthBadge.classList.add("bg-green-100", "dark:bg-green-900/30", "border-green-200", "dark:border-green-800", "text-green-800", "dark:text-green-300");
                    if (dot) dot.className = "indicator-dot h-2 w-2 rounded-full bg-green-500 animate-pulse";
                    healthText.textContent = "System Online";
                } else {
                    healthBadge.classList.add("bg-amber-100", "dark:bg-amber-900/30", "border-amber-200", "dark:border-amber-800", "text-amber-800", "dark:text-amber-300");
                    if (dot) dot.className = "indicator-dot h-2 w-2 rounded-full bg-amber-500";
                    healthText.textContent = "Mock Mode (Offline)";
                }
            } else {
                healthBadge.classList.add("bg-red-100", "dark:bg-red-900/30", "border-red-200", "dark:border-red-800", "text-red-800", "dark:text-red-300");
                const dot = healthBadge.querySelector(".indicator-dot");
                if (dot) dot.className = "indicator-dot h-2 w-2 rounded-full bg-red-500";
                healthText.textContent = "Database Error";
            }
        } catch (err) {
            console.error("Health check error:", err);
            healthBadge.className = "health-badge flex items-center gap-2 px-3 py-1 rounded-full text-xs bg-red-100 dark:bg-red-900/30 border-red-200 dark:border-red-800 text-red-800 dark:text-red-300";
            const dot = healthBadge.querySelector(".indicator-dot");
            if (dot) dot.className = "indicator-dot h-2 w-2 rounded-full bg-red-500";
            healthText.textContent = "Server Unreachable";
        }
    }

    // Fetch data for dropdowns and cuisine tags
    async function fetchAutocompleteData() {
        // Fetch locations list
        try {
            const locRes = await fetch(`${API_BASE}/api/locations`);
            if (locRes.ok) {
                const data = await locRes.json();
                locationsList = data.locations || [];
                populateLocations(locationsList);
            }
        } catch (err) {
            console.error("Failed to load locations:", err);
            // Minimal fallback
            populateLocations(["Delhi, NCR", "Bangalore, KA", "Mumbai, MH", "Hyderabad, TS"]);
        }

        // Fetch cuisines list
        try {
            const cuiRes = await fetch(`${API_BASE}/api/cuisines`);
            if (cuiRes.ok) {
                const data = await cuiRes.json();
                cuisinesList = data.cuisines || [];
                renderCuisineChips(cuisinesList);
            } else {
                renderCuisineChips(defaultPopularCuisines);
            }
        } catch (err) {
            console.error("Failed to load cuisines:", err);
            renderCuisineChips(defaultPopularCuisines);
        }
    }

    // Populate the dropdown menu for locations
    function populateLocations(locations) {
        locationSelect.innerHTML = '<option value="">Select Location</option>';
        locations.forEach(loc => {
            const opt = document.createElement("option");
            opt.value = loc;
            opt.textContent = loc;
            locationSelect.appendChild(opt);
        });
    }

    // Render popular cuisines as toggleable tags
    function renderCuisineChips(cuisines) {
        cuisinesContainer.innerHTML = "";
        
        // Show top 12 cuisines to keep UI neat
        const displayCuisines = cuisines.slice(0, 12);
        
        displayCuisines.forEach(cui => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "cuisine-chip px-4 py-2 bg-surface-container dark:bg-zinc-800 text-on-surface dark:text-zinc-300 rounded-full text-label-sm font-label-sm border border-outline-variant/30 dark:border-zinc-700 hover:border-primary transition-all";
            btn.textContent = cui;
            
            // Check if already selected (for reset/retry flows)
            if (selectedCuisines.includes(cui)) {
                btn.classList.add("active");
            }
            
            btn.addEventListener("click", () => {
                btn.classList.toggle("active");
                if (btn.classList.contains("active")) {
                    if (!selectedCuisines.includes(cui)) {
                        selectedCuisines.push(cui);
                    }
                } else {
                    selectedCuisines = selectedCuisines.filter(item => item !== cui);
                }
            });
            
            cuisinesContainer.appendChild(btn);
        });
    }

    function registerListeners() {
        // Rating slider text feedback
        ratingSlider.addEventListener("input", (e) => {
            const val = parseFloat(e.target.value).toFixed(1);
            ratingValue.textContent = val;
        });

        // Quick tags for textarea wishes
        document.querySelectorAll(".pref-tag").forEach(tag => {
            tag.addEventListener("click", () => {
                // Get only text content (ignoring the symbol span)
                const textNode = Array.from(tag.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
                if (textNode) {
                    const text = textNode.textContent.trim();
                    const currentText = additionalInput.value.trim();
                    if (currentText) {
                        // Append if not already present
                        if (!currentText.toLowerCase().includes(text.toLowerCase())) {
                            additionalInput.value = currentText + ", " + text;
                        }
                    } else {
                        additionalInput.value = text;
                    }
                }
            });
        });

        // Form Submit
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            await getRecommendations();
        });

        // State handlers action buttons
        resetFiltersBtn.addEventListener("click", () => {
            locationSelect.value = "";
            selectedCuisines = [];
            
            // Un-active all cuisine chips
            document.querySelectorAll(".cuisine-chip").forEach(chip => {
                chip.classList.remove("active");
            });
            
            ratingSlider.value = "3.5";
            ratingValue.textContent = "3.5";
            additionalInput.value = "";
            
            // Reset budget back to Medium
            const medRadio = document.querySelector("input[name='budget'][value='Medium']");
            if (medRadio) medRadio.checked = true;
            
            showState(stateWelcome);
        });

        retryBtn.addEventListener("click", getRecommendations);
        forceMockBtn.addEventListener("click", getRecommendations);
    }

    // Helper: Show specific state and hide others
    function showState(stateElement) {
        stateWelcome.style.display = "none";
        stateLoading.style.display = "none";
        stateEmpty.style.display = "none";
        stateError.style.display = "none";
        recommendationsContainer.style.display = "none";
        
        stateElement.style.display = "flex";
        if (stateElement === recommendationsContainer) {
            stateElement.style.display = "block";
        }
    }

    // Fetch recommendations API call
    async function getRecommendations() {
        const locationVal = locationSelect.value;
        const cuisineVal = selectedCuisines.join(", ") || "Any";
        
        const budgetRadio = document.querySelector("input[name='budget']:checked");
        const budgetVal = budgetRadio ? budgetRadio.value : "Medium";
        
        const ratingVal = parseFloat(ratingSlider.value);
        const additionalVal = additionalInput.value.trim();

        // 1. Activate loading state in button & panel
        setSubmitLoading(true);
        showState(stateLoading);

        // Prepare request body
        const payload = {
            location: locationVal || "Any",
            cuisine: cuisineVal,
            budget_level: budgetVal,
            min_rating: ratingVal,
            additional: additionalVal,
            top_n: 3
        };

        try {
            const res = await fetch(`${API_BASE}/api/recommend`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                throw new Error(`Server returned HTTP ${res.status}`);
            }

            const data = await res.json();
            
            if (!data.recommendations || data.recommendations.length === 0) {
                // Empty response state
                emptyMessage.textContent = data.message || "No restaurants found matching your criteria. Try widening your filters!";
                showState(stateEmpty);
            } else {
                // Populate and display recommendations
                renderRecommendations(data.recommendations);
                showState(recommendationsContainer);
            }
            
            // Re-check status silently to keep online indicator fresh
            checkServerHealth();

        } catch (err) {
            console.error("API Call error:", err);
            errorMessage.textContent = `Unable to generate recommendations: ${err.message}. Ensure the FastAPI server is running.`;
            showState(stateError);
        } finally {
            setSubmitLoading(false);
        }
    }

    // Toggle loading states for submit button
    function setSubmitLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.style.display = "none";
            btnIcon.style.display = "none";
            btnLoader.style.display = "block";
        } else {
            submitBtn.disabled = false;
            btnText.style.display = "inline";
            btnIcon.style.display = "inline";
            btnLoader.style.display = "none";
        }
    }

    // Get beautiful food imagery depending on cuisine type
    function getCuisineImage(cuisineStr) {
        const c = (cuisineStr || "").toLowerCase();
        if (c.includes("italian") || c.includes("pizza") || c.includes("pasta") || c.includes("cafe")) {
            return "https://lh3.googleusercontent.com/aida-public/AB6AXuBGXCQp5MYUH-u8nVZ_9VkY2UgnpnkffuSzkQoECAdKgXRb380JXIO4L3hVK-QcnzWsoGstVFaoenufxv79dMecLtrN_X8q-ggfQk5iA4CPC6NBNwoSh7moK8Ci31-Tn5CTGsCX7bGdpj8J0cDgPznEfq8qNHXtr9l-zm0G03Bfji8xy60tiMtJ6DiJLY2Wjgzxo3-t5qhNtGCCbkISshXABriZ9GAzPkI5xu5WwicoOI_wBI7W3gJe8NnSjBU5AaGU0VHI00tU4g8";
        }
        if (c.includes("japanese") || c.includes("sushi") || c.includes("asian") || c.includes("chinese")) {
            return "https://lh3.googleusercontent.com/aida-public/AB6AXuClQeEXxfPhFM8csn8JuhiYFBul1SPBrZMBjHkBG6AcrulnuoBTov4be45qapXDT0RkkWEfVgNHagu5vjtHLkkuCheqnETfs8q9IfSrCa0d2UAARa6wHVLHH9GsgHiol80sOzwiC0uuLhoATlbhY_zH4gt5UUwsQpGT5L1UUPzeoli6890cNP5jfRL8ev5mfDsjOKGQ-CofhaP_Im2r8m0ipQxg_s_GTHKZ-wRTMuMr9q7PNniND9L-FiPydyewMX24BFGKOIjDkRE";
        }
        // Premium Fusion or Indian dish
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuBuUvk1ccE2kQQqRrr3RX8pimWDDeFTk7QtuUiP_BkIyHz2UlPyT1QOSeSRTV5W4nZLSYXtQhHuizFaj1HkvVPW2Y5SQm00Sj9D7I4UUONVdskn65tsrt03hZ-XyLogi4n6Tu7kqEfP7XEPfUjBzplKrR3xkGoo8teWVt-SnY0fgcxzv9V-KAjmHsju3FU9wM2Sppshj5c6boXTctK5jufYmOzA526nr7skYNBoZjTVosIwCqB2t88v-ubrZXENdkDrPz7IqajlSM4";
    }

    // Inject recommendation card items into DOM using premium Google Stitch layouts
    function renderRecommendations(recommendations) {
        recommendationsList.innerHTML = "";
        resultsCount.textContent = `${recommendations.length} Option${recommendations.length > 1 ? 's' : ''} Ranked`;

        recommendations.forEach((rec, idx) => {
            const card = document.createElement("article");
            card.className = "bg-white dark:bg-zinc-900 rounded-xl overflow-hidden shadow-md flex flex-col hover:shadow-xl hover:translate-y-[-4px] transition-all duration-300 group border border-outline-variant/20 dark:border-zinc-800";

            // Format cost display
            const costFormatted = rec.cost ? `₹${rec.cost} for two` : "Price details N/A";
            
            // Set cover image
            const imgUrl = getCuisineImage(rec.cuisine);

            // Determine badge label
            let badgeText = "Top Match";
            if (idx === 1) badgeText = "AI Choice";
            else if (idx === 2) badgeText = "Trending";

            card.innerHTML = `
                <div class="relative h-48 overflow-hidden">
                    <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="${imgUrl}" alt="${rec.name}" />
                    <div class="absolute top-4 left-4 bg-primary text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg select-none">
                        ${badgeText}
                    </div>
                </div>
                <div class="p-stack-md flex-1 flex flex-col">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-headline-md text-headline-md text-zinc-900 dark:text-white leading-tight font-semibold">${rec.name}</h3>
                        <div class="flex items-center gap-1 px-2 py-0.5 bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-300 rounded-lg">
                            <span class="material-symbols-outlined text-[16px] text-amber-500" style="font-variation-settings: 'FILL' 1;">star</span>
                            <span class="font-bold text-label-md">${parseFloat(rec.rating).toFixed(1)}</span>
                        </div>
                    </div>
                    
                    <div class="flex flex-col gap-0.5 text-on-surface-variant dark:text-zinc-400 text-xs mb-4">
                        <div class="flex items-center gap-1">
                            <span class="material-symbols-outlined text-sm">restaurant</span>
                            <span>${rec.cuisine || "Cuisine details N/A"}</span>
                        </div>
                        <div class="flex items-center gap-1">
                            <span class="material-symbols-outlined text-sm">payments</span>
                            <span>${costFormatted}</span>
                        </div>
                        <div class="flex items-center gap-1">
                            <span class="material-symbols-outlined text-sm">location_on</span>
                            <span class="truncate">${rec.address || "Location details N/A"}</span>
                        </div>
                    </div>

                    <!-- AI Rationale Container -->
                    <div class="bg-primary/5 dark:bg-primary/10 border border-primary/10 dark:border-primary/20 p-3 rounded-xl mb-4 flex gap-2 items-start mt-auto">
                        <span class="material-symbols-outlined text-primary text-[18px] mt-0.5 shrink-0">auto_awesome</span>
                        <p class="text-xs text-on-surface-variant dark:text-zinc-300 leading-relaxed">
                            ${rec.explanation}
                        </p>
                    </div>
                    
                    <button class="w-full py-2.5 border border-primary text-primary hover:bg-primary hover:text-white font-label-md rounded-xl transition-colors font-medium">
                        View Details
                    </button>
                </div>
            `;

            recommendationsList.appendChild(card);
        });
    }
});
