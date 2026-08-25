const editor = document.getElementById("editor");
const lineNumbers = document.getElementById("lineNumbers");

const wordCount = document.getElementById("wordCount");
const charCount = document.getElementById("charCount");
const cursorPosition = document.getElementById("cursorPosition");
const clock = document.getElementById("clock");

const fileName = document.getElementById("fileName");
const fileInput = document.getElementById("fileInput");

function updateStatus() {
    const text = editor.innerText;

    const words = text.trim()
        ? text.trim().split(/\s+/).length
        : 0;

    wordCount.textContent = `Words: ${words}`;
    charCount.textContent = `Characters: ${text.length}`;

    updateLineNumbers();
}

function updateLineNumbers() {
    const text = editor.innerText || "";
    let totalLines = text.split(/\r\n|\r|\n/).length;

    if (text.endsWith("\n") && totalLines > 1) {
        totalLines--;
    }

    let numbers = "";

    for (let i = 1; i <= totalLines; i++) {
        numbers += `<div>${i}</div>`;
    }

    lineNumbers.innerHTML = numbers;
}

function updateClock() {
    const now = new Date();

    clock.textContent = now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();

document.getElementById("newBtn").addEventListener("click", () => {
    if (editor.innerText.trim() !== "") {
        const confirmNew = confirm(
            "Create a new file? Unsaved changes may be lost."
        );
        if (!confirmNew) return;
    }

    editor.innerHTML = "";
    fileName.textContent = "Untitled";

    updateStatus();
});

document.getElementById("openBtn").addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        editor.innerText = e.target.result;
        fileName.textContent = file.name;

        updateStatus();
    };

    reader.readAsText(file);
});

document.getElementById("saveBtn").addEventListener("click", () => {

    const content = editor.innerText;
    const blob = new Blob(
        [content],
        { type: "text/plain" }
    );

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    let name = fileName.textContent;

    if (name === "Untitled") {
        name = "untitled.txt";
    }

    link.download = name;
    link.click();

    URL.revokeObjectURL(link.href);
});

document.getElementById("undoBtn").addEventListener("click", () => {
    document.execCommand("undo");
});

document.getElementById("redoBtn").addEventListener("click", () => {
    document.execCommand("redo");
});

document.getElementById("boldBtn").addEventListener("click", () => {
    document.execCommand("bold");
    editor.focus();
});

document.getElementById("italicBtn").addEventListener("click", () => {
    document.execCommand("italic");
    editor.focus();
});

document.getElementById("underlineBtn").addEventListener("click", () => {
    document.execCommand("underline");
    editor.focus();
});

document.getElementById("fontFamily").addEventListener("change", (event) => {
    editor.style.fontFamily = event.target.value;

    editor.focus();
});

document.getElementById("fontSize").addEventListener("change", (event) => {
    editor.style.fontSize = event.target.value + "px";

    editor.focus();
});

document.getElementById("findBtn").addEventListener("click", () => {

    const searchText = prompt("Enter text to find:");

    if (!searchText) return;

    const content = editor.innerText;

    if (content.toLowerCase().includes(searchText.toLowerCase())) {
        alert(`"${searchText}" was found.`);
    } else {
        alert(`"${searchText}" was not found.`);
    }
});

document.getElementById("darkModeBtn").addEventListener("click", () => {

    document.body.classList.toggle("dark-mode");
});

function updateCursorPosition() {

    const selection = window.getSelection();

    if (selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);

    const preCaretRange = range.cloneRange();

    preCaretRange.selectNodeContents(editor);
    preCaretRange.setEnd(range.endContainer, range.endOffset);

    const textBeforeCursor = preCaretRange.toString();

    const lines = textBeforeCursor.split("\n");

    const line = lines.length;
    const column = lines[lines.length - 1].length + 1;

    cursorPosition.textContent = `Ln: ${line}, Col: ${column}`;
}

editor.addEventListener("input", updateStatus);
editor.addEventListener("keyup", updateLineNumbers);
editor.addEventListener("keyup", updateCursorPosition);
editor.addEventListener("click", updateCursorPosition);

updateStatus();