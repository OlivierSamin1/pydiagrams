/**
 * PyDiagrams Theme Management
 * This file contains functions for managing themes in PyDiagrams HTML output
 */

// Available themes
const THEMES = [
    { id: 'default', name: 'Default', icon: 'theme-default' },
    { id: 'blue', name: 'Blue', icon: 'theme-blue' },
    { id: 'green', name: 'Green', icon: 'theme-green' },
    { id: 'purple', name: 'Purple', icon: 'theme-purple' },
    { id: 'high-contrast', name: 'High Contrast', icon: 'theme-high-contrast' }
];

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
    
    // Create theme selector
    const themeSelector = document.createElement('div');
    themeSelector.id = 'theme-selector';
    
    // Add theme options
    THEMES.forEach(theme => {
        const themeOption = document.createElement('div');
        themeOption.className = `theme-option ${theme.icon}`;
        themeOption.dataset.theme = theme.id;
        themeOption.title = theme.name;
        themeSelector.appendChild(themeOption);
    });
    
    themeControls.appendChild(themeSelector);
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
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('pydiagrams-theme');
    if (savedTheme && savedTheme !== 'default') {
        document.body.classList.add(`theme-${savedTheme}`);
        
        // Mark the active theme
        const themeOptions = document.querySelectorAll('.theme-option');
        themeOptions.forEach(option => {
            if (option.dataset.theme === savedTheme) {
                option.classList.add('active');
            }
        });
    } else {
        // Mark default theme as active
        const defaultTheme = document.querySelector('.theme-option[data-theme="default"]');
        if (defaultTheme) {
            defaultTheme.classList.add('active');
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
    
    // Theme options
    const themeOptions = document.querySelectorAll('.theme-option');
    themeOptions.forEach(option => {
        option.addEventListener('click', function() {
            const theme = this.dataset.theme;
            setTheme(theme);
        });
    });
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

// Set theme
function setTheme(themeId) {
    // Remove all theme classes
    THEMES.forEach(theme => {
        if (theme.id !== 'default') {
            document.body.classList.remove(`theme-${theme.id}`);
        }
    });
    
    // Add the selected theme class
    if (themeId !== 'default') {
        document.body.classList.add(`theme-${themeId}`);
    }
    
    // Update active state on theme options
    const themeOptions = document.querySelectorAll('.theme-option');
    themeOptions.forEach(option => {
        option.classList.remove('active');
        if (option.dataset.theme === themeId) {
            option.classList.add('active');
        }
    });
    
    // Save preference
    localStorage.setItem('pydiagrams-theme', themeId);
    
    // Dispatch event for diagram-specific renderers
    document.dispatchEvent(new CustomEvent('themeChanged', {
        detail: { 
            theme: themeId,
            darkMode: document.body.classList.contains('dark-mode')
        }
    }));
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', initThemeSystem); 