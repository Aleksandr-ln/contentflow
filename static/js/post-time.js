document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.post-time').forEach(el => {
        const utcDate = new Date(el.dataset.utc);

        const formatted = utcDate.toLocaleString(navigator.language, {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        el.textContent = formatted;
    });
});