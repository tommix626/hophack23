chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'getCurrentTabURL') {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            let currentTab = tabs[0];
            if (currentTab && currentTab.url) {
                sendResponse({url: currentTab.url});
            } else {
                sendResponse({url: null});
            }
        });
        return true;  // Will respond asynchronously.
    }
});
