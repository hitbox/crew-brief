function copy_to_clipboard(text) {
    navigator.clipboard.writeText(text);
    show_toast(text);
}

function init_query_form() {
    // XXX
    // query_form_id injection
    // if this is still wanted.
    document.getElementById("{{ query_form_id }}").addEventListener("submit", function(e) {
        /* remove empty fields from submission */
        const elements = this.elements;
        for (let i = elements.length - 1; i >= 0; i--) {
            const elem = elements[i];
            if (elem.name && !elem.value.trim()) {
                elem.removeAttribute("name");
            }
        }
    });
}

function show_toast(message, duration=2000) {
    const toast = document.getElementById("toast");

    toast.textContent = message;

    toast.classList.add("show");

    setTimeout(function() {
        toast.classList.remove("show");
    }, duration);
}

function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
}

function loadTheme() {
    const saved = localStorage.getItem(THEME);
    const theme = saved || getSystemTheme();
    applyTheme(theme);

    // Sync dropdown to current theme
    const select = document.getElementById('theme-select');
    if (select) {
        select.value = saved || theme;
    }
}

function setupThemeSelector() {
    const select = document.getElementById('theme-select');
    if (!select) {
        return;
    }

    select.addEventListener('change', function() {
        const selected = select.value;
        const system = getSystemTheme();

        if (selected === 'system' || selected === system) {
            localStorage.removeItem(THEME);
            applyTheme(system);
        } else {
            localStorage.setItem(THEME, selected);
            applyTheme(selected);
        }
    });

    // Respond to system theme changes if no user override
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {
        const saved = localStorage.getItem(THEME);
        if (!saved || saved === 'system') {
            applyTheme(getSystemTheme());
        }
    });
}

loadTheme();
setupThemeSelector();
