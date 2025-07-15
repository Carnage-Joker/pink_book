(function() {
    const PANIC_CLASS = 'panic-mode';
    const PANIC_IMG = '/static/img/panic_placeholder.jpg';

    function enablePanicMode() {
        document.body.classList.add(PANIC_CLASS);
        // Replace all images
        document.querySelectorAll('img').forEach(img => {
            if (!img.dataset.originalSrc) {
                img.dataset.originalSrc = img.src;
            }
            img.src = PANIC_IMG;
        });
        // Optionally, replace background images
        document.querySelectorAll('[style*="background-image"]').forEach(el => {
            if (!el.dataset.originalBg) {
                el.dataset.originalBg = el.style.backgroundImage;
            }
            el.style.backgroundImage = `url('${PANIC_IMG}')`;
        });
    }

    function disablePanicMode() {
        document.body.classList.remove(PANIC_CLASS);
        // Restore all images
        document.querySelectorAll('img').forEach(img => {
            if (img.dataset.originalSrc) {
                img.src = img.dataset.originalSrc;
            }
        });
        // Restore background images
        document.querySelectorAll('[data-original-bg]').forEach(el => {
            el.style.backgroundImage = el.dataset.originalBg;
        });
    }

    function togglePanicMode() {
        if (document.body.classList.contains(PANIC_CLASS)) {
            disablePanicMode();
        } else {
            enablePanicMode();
        }
    }

    // Hotkey: Ctrl+Shift+P
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey && e.code === 'KeyP') {
            togglePanicMode();
        }
    });

    // Button click
    document.addEventListener('DOMContentLoaded', function() {
        const btn = document.getElementById('panic-mode-btn');
        if (btn) {
            btn.addEventListener('click', togglePanicMode);
        }
    });

    // Expose for debugging
    window.togglePanicMode = togglePanicMode;
})();