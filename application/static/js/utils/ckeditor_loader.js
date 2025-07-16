function initializeCKEditor(textarea) {
    if (textarea && !textarea.hasAttribute('data-ckeditor-initialized')) {
        ClassicEditor
            .create(textarea)
            .then(editor => {
                textarea.setAttribute('data-ckeditor-initialized', 'true');
                textarea.ckeditorInstance = editor;
            })
            .catch(error => {
                console.error('There was a problem initializing the editor:', error);
            });
    }
}