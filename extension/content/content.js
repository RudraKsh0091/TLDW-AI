let lastTitle = "";
console.log("Content script loaded");

function getVideoInfo() {
    const url = window.location.href;
    const videoId = new URL(url).searchParams.get("v");
    const title = document.querySelector("yt-formatted-string.style-scope.ytd-watch-metadata")?.textContent.trim();
    return {
        url,
        videoId,
        title
    };
}

function sendVideoInfo() {
    const info = getVideoInfo();
    if (!info.videoId) return;
    chrome.runtime.sendMessage({
        type: "VIDEO_CHANGED",
        payload: info
    });
}

let titleObserver = null;

function watchTitle() {
    if (titleObserver) {
        titleObserver.disconnect();
    }
    const target = document.querySelector("h1.ytd-watch-metadata");
    if (!target) return;
    titleObserver = new MutationObserver(() => {
        const title = target.textContent.trim();
        if (title !== lastTitle) {
            lastTitle = title;
            sendVideoInfo();
        }
    });
    titleObserver.observe(target, {
        childList: true,
        subtree: true,
        characterData: true
    });
}

window.addEventListener("yt-navigate-finish", () => {
    watchTitle();
});