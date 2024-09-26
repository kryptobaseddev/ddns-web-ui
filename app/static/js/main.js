// Add any custom JavaScript functionality here
document.addEventListener('DOMContentLoaded', (event) => {
    // Example: Add confirmation for potentially destructive actions
    const dangerousButtons = document.querySelectorAll('.btn-danger, .btn-warning');
    dangerousButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to perform this action?')) {
                e.preventDefault();
            }
        });
    });
});