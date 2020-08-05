(() => {
    const webShareTestEl = document.querySelector('.web-share-test');

    // CHECK IF SHARE IS AVAILABLE
    if (!navigator.share) {
        webShareTestEl.children[0].innerText = 'error';
        return;
    }

    let resetTimeout;

    // METHODS
    const resetButton = () => {
        clearTimeout(resetTimeout);
        resetTimeout = setTimeout(() => {
            webShareTestEl.children[0].innerText = 'share';
        }, 1000);
    };

    const getOpenGraphData = function(property) {
        return document.querySelector(`meta[property="${property}"]`).getAttribute('content')
    };

    const sharePage = () => {
        navigator.share({
                title: getOpenGraphData('og:title'),
                text: getOpenGraphData('og:description'),
                url: getOpenGraphData('og:url')
            }).then(() => {
                webShareTestEl.children[0].innerText = 'done';
                resetButton();
            })
            .catch(error => {
                console.log('Error sharing:', error);

                webShareTestEl.children[0].innerText = 'error';
                resetButton();
            });
    };

    // EVENTS
    webShareTestEl.addEventListener('click', sharePage);
})();