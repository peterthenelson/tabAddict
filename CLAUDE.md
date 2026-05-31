# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TabAddict is a lightweight Chrome extension for saving and restoring browser sessions as plain-text files. It has no build system — it's plain HTML, CSS, and JS loaded directly by Chrome.

**Core design constraints (non-negotiable):**
- Sessions must always be importable/exportable as plain text. No opaque formats.
- No third party ever sees the user's tab list. No sync services, no remote storage.
- Keep it compact and simple. This is not a complex app.

## Loading & Testing

There is no build step. To develop:

1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select this directory

After any JS/HTML/CSS change, click the refresh icon on the extension card in `chrome://extensions/`. Changes to the popup require closing and reopening it.

## Architecture

The extension has three pages that communicate via message passing:

- **`background.js`** — Service/background context. Handles the toolbar icon click, provides utility functions (`minimizeAll`, `launchDndNewWin`, `launchMain`) that the launch page calls via `chrome.extension.getBackgroundPage()`.
- **`launch.html`/`launch.js`** — Main UI. Contains the session editor textarea, the three action buttons (Open, Capture, Launch), and the core session logic (`fill_from_windows`, `process_links`, `open_tabs`).
- **`dnd.html`/`dnd.js`** — A small popup window for drag-and-drop file import. Sends the file's text content back to the launch page via `chrome.extension.sendMessage`, then closes.
- **`options.html`** — Static about/help page.

**Message flow for file open:** launch page minimizes all windows → opens dnd window → user drops file → dnd reads it and sends `{content: <string>}` → launch page receives it, restores its window, populates textarea.

## Session Format

Plain text, parsed line by line:
- Lines starting with `http://` or `https://` → open as a tab
- Lines starting with `>` → open a new window (subsequent URLs go there)
- All other lines → ignored (use for comments/labels)

The first "window" is the current window. The launch tab closes itself after launching.

## Revival: What Needs to Change

The extension uses Manifest v2 (Chrome has been sunset MV2; MV3 is required):

| MV2 | MV3 equivalent |
|---|---|
| `"manifest_version": 2` | `"manifest_version": 3` |
| `"browser_action"` | `"action"` |
| `"background": {"page": "background.html"}` | `"background": {"service_worker": "background.js"}` |
| `chrome.extension.sendMessage` | `chrome.runtime.sendMessage` |
| `chrome.extension.onMessage` | `chrome.runtime.onMessage` |
| `chrome.extension.getBackgroundPage()` | Not available in MV3 — use message passing instead |

**jQuery 1.7.2** should be dropped in favor of vanilla JS. The actual usage is minimal: `$(document).ready`, `.click()`, `.val()`, `.text()`, and `.css()` — all trivially replaceable.

**CSS vendor prefixes** (`-webkit-gradient`) should be replaced with standard properties.

**File export** was previously manual copy-paste. The [File System Access API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API) (`showSaveFilePicker`) or a `<a download>` trick can now save files directly — this is a natural improvement that preserves the text-format constraint.

## Feature Ideas Compatible with Original Intention

- **Named sessions:** Use `chrome.storage.local` to save multiple named sessions. Keep the textarea as the editing surface; add save/load UI alongside it.
- **Direct file save (export):** Replace the copy-paste instruction with a "Save" button using `<a download>` or the File System Access API.
- **Tab groups:** When capturing, emit a group marker (e.g. `>> Group Name`) and restore tab groups on launch if the Tab Groups API is available.
- **Keyboard shortcuts:** Chrome supports declaring `commands` in the manifest for keyboard-triggered actions.
