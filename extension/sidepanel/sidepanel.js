const status = document.getElementById("status");
const videoTitle = document.getElementById("videoTitle");

const processBtn = document.getElementById("processBtn");
const askBtn = document.getElementById("askBtn");
const copyBtn = document.getElementById("copyBtn");
const downloadBtn=document.getElementById("downloadBtn");

const questionBox = document.getElementById("question");
const chatContainer = document.getElementById("chatContainer");
const suggestionsDiv = document.getElementById("suggestions");

let lastAnswer = "";
let chatHistory = [];
let currentVideo = null;
let isIndexed = false;

askBtn.disabled = true;

function renderChat(){
    chatContainer.innerHTML = "";
    chatHistory.forEach(message=>{
        const div=document.createElement("div");
        div.className=`message ${message.role}`;
        div.innerHTML=`
            <strong>${message.role==="user" ? "👤 You":"🤖 TLDW AI"}</strong>
            ${
                message.role==="assistant"
                ? marked.parse(message.content)
                : message.content
            }
        `;
        chatContainer.appendChild(div);
    });
    chatContainer.scrollTop=chatContainer.scrollHeight;
}

processBtn.addEventListener("click", async () => {
    if (!currentVideo) return;

    status.textContent = "⏳ Processing video...";
    processBtn.disabled = true;

    try {
        const response = await fetch(
            `${API_BASE}/index`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    youtube_url: currentVideo.url
                })
            }
        );

        if (!response.ok) {
            throw new Error("Indexing failed");
        }

        const data = await response.json();

        status.textContent = data.from_cache ? "⚡ Already Indexed" : "🟢 Ready";

        isIndexed = true;
        askBtn.disabled = false;
        processBtn.textContent = "Processed ✓";
        processBtn.disabled = true;

        console.log(data);
    }
    catch (err) {
        status.textContent = "🔴 Failed";
        isIndexed = false;
        askBtn.disabled = true;
        console.error(err);
    }
    finally {
        // processBtn.disabled = false;
    }
});

askBtn.addEventListener("click", async () => {
    if (!isIndexed) return;

    const question = questionBox.value.trim();

    if (!question) {
        chatContainer.textContent = "Please enter a question.";
        return;
    }

    chatHistory.push({
        role:"user",
        content:question
    });

    chatHistory.push({
        role:"assistant",
        content:`
        <div class="loading-wrapper">
            <div class="spinner"></div>
            <span>Generating answer...</span>
        </div>
        `
    });

    renderChat();
    askBtn.disabled = true;
    questionBox.disabled = true;

    try {
        const response = await fetch(
            `${API_BASE}/ask`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    youtube_url: currentVideo.url,
                    question
                })
            }
        );

        if (!response.ok) {
            throw new Error("Failed to get answer");
        }

        const data = await response.json();
        
        chatHistory.pop();

        lastAnswer = data.answer;

        chatHistory.push({
            role: "assistant",
            content: data.answer
        });

        copyBtn.disabled = false;
        downloadBtn.disabled=false;

        renderChat();

        renderSuggestions(data.suggestions);
    }
    catch (err) {
        console.error(err);
        chatHistory.pop();
        suggestionsDiv.innerHTML = "";
        lastAnswer = "";

        chatHistory.push({
            role: "assistant",
            content: "❌ Something went wrong."
        });

        copyBtn.disabled = true;

        renderChat();
    }
    finally {
        askBtn.disabled = false;
        questionBox.disabled = false;
    }
});

function updateUI(video) {
    currentVideo = video;
    isIndexed = false;
    askBtn.disabled = true;
    questionBox.value = "";
    chatHistory=[];
    lastAnswer = "";
    copyBtn.disabled = true;
    downloadBtn.disabled=true;
    suggestionsDiv.innerHTML = "";

    renderChat();

    if (!video) {
        status.textContent = "🔴 No Video";
        videoTitle.textContent = "No Video Detected";
        processBtn.disabled = true;
        return;
    }

    processBtn.disabled = false;
    status.textContent = "📺 Video Detected";
    videoTitle.textContent = video.title;
    questionBox.focus();
}

document.addEventListener("DOMContentLoaded", () => {
    chrome.runtime.sendMessage(
        {
            type: "GET_CURRENT_VIDEO"
        },
        (video) => {
            updateUI(video);
        }
    );
});

chrome.runtime.onMessage.addListener((message) => {
    if (message.type !== "VIDEO_UPDATED")
        return;

    updateUI(message.payload);
});

copyBtn.addEventListener("click", async () => {
    if (!lastAnswer)
        return;
    await navigator.clipboard.writeText(lastAnswer);
    const original = copyBtn.textContent;
    copyBtn.textContent = "✅ Copied!";
    setTimeout(() => {
        copyBtn.textContent = original;
    }, 1500);
});

function renderSuggestions(list){
    suggestionsDiv.innerHTML="";

    if (!Array.isArray(list) || list.length === 0) {
        return;
    }

    list.forEach(question=>{
        const btn=document.createElement("button");
        btn.className="suggestion";
        btn.textContent=question;
        btn.onclick=()=>{
            questionBox.value=question;
            askBtn.click();
        };
        suggestionsDiv.appendChild(btn);
    });
}

downloadBtn.addEventListener("click",()=>{
    let text="";
    chatHistory.forEach(msg=>{
        if(msg.role==="user")
            text+=`You: ${msg.content}\n\n`;
        else
            text+=`TLDW AI:\n${msg.content}\n\n`;
    });
    const blob=new Blob([text],{
        type:"text/plain"
    });
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;
    a.download="tldw_notes.txt";
    a.click();
    URL.revokeObjectURL(url);
});

questionBox.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        if (!askBtn.disabled) {
            askBtn.click();
        }
    }
});