document.addEventListener('DOMContentLoaded', () => {
  const text = document.getElementById('text');
  let position = null;

  function processLinks(result) {
    const windows = [[]];
    for (const line of result.split('\n')) {
      if (line[0] === '>') {
        windows.push([]);
      } else if (line.startsWith('http://') || line.startsWith('https://')) {
        windows[windows.length - 1].push(line.trim());
      }
    }
    return windows;
  }

  function openTabs(result) {
    const windows = processLinks(result);
    for (const url of windows[0]) {
      chrome.tabs.create({ url });
    }
    for (let i = 1; i < windows.length; i++) {
      if (windows[i].length > 0) {
        chrome.windows.create({ url: windows[i] });
      }
    }
    chrome.tabs.getCurrent(tab => chrome.tabs.remove(tab.id));
  }

  function fillFromWindows() {
    text.value = '';
    chrome.tabs.getCurrent(currentTab => {
      chrome.windows.getAll({ populate: true }, windows => {
        let n = 0;
        for (const win of windows) {
          if (win.type === 'normal' || win.type === 'popup') {
            n++;
            text.value += `> Window #${n}\n`;
            for (const tab of win.tabs) {
              if (tab.id !== currentTab.id) {
                text.value += tab.url + '\n';
              }
            }
            text.value += '\n';
          }
        }
      });
    });
  }

  function minimizeAll(callback) {
    chrome.windows.getAll(wins => {
      let count = wins.length;
      for (const win of wins) {
        chrome.windows.update(win.id, { state: 'minimized' }, () => {
          if (--count === 0) callback();
        });
      }
    });
  }

  function launchDndWin() {
    chrome.windows.create({
      url: chrome.runtime.getURL('dnd.html'),
      left: 600,
      top: 150,
      width: 430,
      height: 545,
    });
  }

  document.getElementById('open').addEventListener('click', e => {
    e.preventDefault();
    chrome.windows.getCurrent(win => {
      position = { left: win.left, top: win.top, height: win.height, width: win.width };
      minimizeAll(launchDndWin);
    });
  });

  document.getElementById('capture').addEventListener('click', e => {
    e.preventDefault();
    fillFromWindows();
  });

  document.getElementById('launch').addEventListener('click', e => {
    e.preventDefault();
    openTabs(text.value);
  });

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.content || request.content === '') {
      text.value = request.content;
    }
    if (position) {
      chrome.windows.update(
        chrome.windows.WINDOW_ID_CURRENT,
        { ...position, state: 'normal', focused: true },
        () => text.focus()
      );
    }
  });
});
