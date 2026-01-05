// /js/layout.js
(async function () {
    const mount = document.getElementById('site-footer');
    if (!mount) return;

    try {
        const res = await fetch('/partials/footer.html', { cache: 'no-store' });
        if (!res.ok) throw new Error(`Footer fetch failed: ${res.status}`);

        mount.innerHTML = await res.text();

        // 👇 ADD THIS LINE HERE (footer is now in the DOM)
        document.dispatchEvent(new Event('hogga:footer-ready'));

    } catch (e) {
        console.warn('[layout] footer partial failed:', e);
    }
})();
