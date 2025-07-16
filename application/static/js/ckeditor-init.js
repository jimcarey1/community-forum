document.addEventListener('DOMContentLoaded', function () {
    const textareas = document.querySelectorAll('textarea[data-provide="ckeditor"]');
    textareas.forEach(textarea => {
        initializeCKEditor(textarea);
    });
});
