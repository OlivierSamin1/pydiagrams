/**
 * PyDiagrams Theme Management
 * This file contains functions for managing themes in PyDiagrams HTML output
 */

// Initialize theme system
function initThemeSystem() {
    // Create theme controls if they don't exist
    if (!document.getElementById('theme-controls')) {
        createThemeControls();
    }
    
    // Load saved theme preferences
    loadThemePreferences();
    
    // Set up event listeners
    setupThemeEventListeners();
}

// Create theme controls
function createThemeControls() {
    const themeControls = document.createElement('div');
    themeControls.id = 'theme-controls';
    
    // Create dark mode toggle
    const darkModeToggle = document.createElement('button');
    darkModeToggle.id = 'theme-toggle';
    darkModeToggle.textContent = '🌙';
    darkModeToggle.title = 'Toggle Dark Mode';
    themeControls.appendChild(darkModeToggle);
    
    document.body.appendChild(themeControls);
}

// Load saved theme preferences
function loadThemePreferences() {
    // Check for saved dark mode preference
    const darkMode = localStorage.getItem('pydiagrams-dark-mode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.textContent = '☀️';
            themeToggle.title = 'Switch to Light Mode';
        }
    }
}

// Set up event listeners for theme controls
function setupThemeEventListeners() {
    // Dark mode toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleDarkMode);
    }
}

// Toggle dark mode
function toggleDarkMode() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    const themeToggle = document.getElementById('theme-toggle');
    
    if (isDarkMode) {
        themeToggle.textContent = '☀️';
        themeToggle.title = 'Switch to Light Mode';
    } else {
        themeToggle.textContent = '🌙';
        themeToggle.title = 'Switch to Dark Mode';
    }
    
    // Save preference
    localStorage.setItem('pydiagrams-dark-mode', isDarkMode);
    
    // Dispatch event for diagram-specific renderers
    document.dispatchEvent(new CustomEvent('themeChanged', {
        detail: { darkMode: isDarkMode }
    }));
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', initThemeSystem); 