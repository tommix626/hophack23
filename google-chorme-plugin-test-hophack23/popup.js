document.getElementById('openLocalhostLink').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let currentTab = tabs[0];
        let newUrl = 'http://localhost:8050/data?url=' + encodeURIComponent(currentTab.url);
        window.open(newUrl, '_blank');

        showFeedback();
    });
});

document.getElementById('openOtherSite').addEventListener('click', function() {
    // Change this to your desired URL
    let otherSiteUrl = 'https://rliu79.wixsite.com/my-site';
    window.open(otherSiteUrl, '_blank');

    showFeedback();
});

function showFeedback() {
    let feedbackDiv = document.getElementById('feedback');
    feedbackDiv.style.display = "block";
    feedbackDiv.style.animation = "fadein 0.5s";
}
