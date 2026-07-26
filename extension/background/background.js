let currentVideo = null;

chrome.runtime.onInstalled.addListener(() => {
    console.log("TLDW AI Installed")
})

chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
    if(!tab.url) return

    if(tab.url.startsWith("https://www.youtube.com/")) {
        await chrome.sidePanel.setOptions({
            tabId,
            path: "sidepanel/sidepanel.html",
            enabled: true
        })
    }
})

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    switch (message.type) {
        case "VIDEO_CHANGED":
            currentVideo = message.payload;
            console.log("Current Video Updated");
            console.log(currentVideo);
            
            chrome.runtime.sendMessage({
                type: "VIDEO_UPDATED",
                payload: currentVideo
            });
            break;
        case "GET_CURRENT_VIDEO":
            sendResponse(currentVideo);
            break;
    }
    return true;
});