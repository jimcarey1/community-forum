
document.addEventListener('DOMContentLoaded', function() {
    const loginLink = document.getElementById('login-link');
    const signupLink = document.getElementById('signup-link');

    function openAuthWindow(event, url) {
        event.preventDefault(); // Prevent default link behavior

        const width = 600;
        const height = 700;
        const left = (window.screen.width / 2) - (width / 2);
        const top = (window.screen.height / 2) - (height / 2);
        const features = `width=${width},height=${height},left=${left},top=${top},popup=true,scrollbars=yes,resizable=yes`;

        const authWindow = window.open(url, '_blank', features);

        // Periodically check if the pop-up window has been closed or redirected
        const checkPopupInterval = setInterval(() => {
            if (authWindow.closed) {
                clearInterval(checkPopupInterval);
                console.log('Auth window closed by user.');
                // You might want to refresh the parent page here if authentication status changed
                // For example, if you know the user should now be logged in.
                // window.location.reload(); 
            } else {
                try {
                    // Attempt to access a property to check if it's still on the Allauth domain
                    // This might trigger a cross-origin error if the popup redirects to your main domain
                    // and you try to access its location before it closes.
                    // A more robust solution involves a postMessage listener.
                    if (authWindow.location.href.includes('localhost:8000/') || 
                        authWindow.location.href.includes('localhost:8000/')) { // Adjust to your actual success URL pattern
                        //authWindow.close();
                        clearInterval(checkPopupInterval);
                        console.log('Auth successful, closing window and reloading parent.');
                        //window.location.reload(); // Reload parent page to reflect login status
                    }
                } catch (e) {
                    // Cross-origin error typically means the popup has redirected to your domain
                    // This is a good sign that authentication might be complete.
                    authWindow.close();
                    clearInterval(checkPopupInterval);
                    console.log('Cross-origin access denied, assuming auth successful and reloading parent.');
                    window.location.reload();
                }
            }
        }, 500); // Check every 500ms
    }

    if (loginLink) {
        loginLink.addEventListener('click', (event) => openAuthWindow(event, loginLink.href));
    }

    if (signupLink) {
        signupLink.addEventListener('click', (event) => openAuthWindow(event, signupLink.href));
    }
});