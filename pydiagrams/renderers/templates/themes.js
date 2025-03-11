/* Theme functions for Mermaid diagrams */

// Available themes
const THEMES = [
    "default", 
    "forest", 
    "dark", 
    "neutral", 
    "blue",
    "high-contrast"
];

// Current theme
let currentTheme = "default";
let isDarkMode = false;

/**
 * Set the active theme
 * @param {string} theme - The theme name
 */
function setTheme(theme) {
    if (!THEMES.includes(theme)) {
        console.warn(`Theme "${theme}" not found, using default theme instead`);
        theme = "default";
    }
    
    currentTheme = theme;
    
    // Update mermaid config
    mermaid.initialize({
        theme: getMermaidTheme(theme, isDarkMode),
        startOnLoad: true
    });
}

/**
 * Set the dark mode state
 * @param {boolean} darkMode - Whether dark mode is active
 */
function setDarkMode(darkMode) {
    isDarkMode = darkMode;
    
    // Update body class
    if (darkMode) {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }
    
    // Update mermaid config
    mermaid.initialize({
        theme: getMermaidTheme(currentTheme, isDarkMode),
        startOnLoad: true
    });
}

/**
 * Get the current theme name
 * @returns {string} The current theme name
 */
function getCurrentTheme() {
    return getMermaidTheme(currentTheme, isDarkMode);
}

/**
 * Map our theme names to Mermaid theme names
 * @param {string} theme - Our theme name
 * @param {boolean} darkMode - Whether dark mode is active
 * @returns {string} The corresponding Mermaid theme name
 */
function getMermaidTheme(theme, darkMode) {
    if (darkMode) {
        // In dark mode, map to appropriate Mermaid dark themes
        switch (theme) {
            case "default":
                return "dark";
            case "forest":
                return "forest";
            case "dark":
                return "dark";
            case "neutral":
                return "dark";
            case "blue":
                return "dark";
            case "high-contrast":
                return "dark";
            default:
                return "dark";
        }
    } else {
        // In light mode, map to appropriate Mermaid light themes
        switch (theme) {
            case "default":
                return "default";
            case "forest":
                return "forest";
            case "dark":
                return "dark";
            case "neutral":
                return "neutral";
            case "blue":
                return "default";
            case "high-contrast":
                return "default";
            default:
                return "default";
        }
    }
} 