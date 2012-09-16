$(function () {
  // Used to launch tabs
  open_tabs = function (result) {
    var i, windows;
    windows = process_links(result);
    if (windows.length >= 1) {
      for (i = 0; i < windows[0].length; i++) {
        chrome.tabs.create({'url': windows[0][i]});
      }
    }
    for (i = 1; i < windows.length; i++) {
      if (windows[i].length > 0) {
        chrome.windows.create({'url': windows[i]});
      }
    }
    chrome.tabs.getCurrent(function (tab) {
      chrome.tabs.remove(tab.id);
    });
  };
  
  // Processing links
  process_links = function (result) {
    var raw_links, i, link, windows;
    raw_links = result.split('\n');
    windows = [[]];
    // TODO split windows on >
    for (i = 0; i < raw_links.length; i++) {
      link = raw_links[i];
      if (link[0] === '>') {
        windows.push([]);
      } else if (link.substr(0,7) === 'http://' 
        || link.substr(0,8) === 'https://') { // TODO filter better
        windows[windows.length-1].push(raw_links[i])
      }
    }
    return windows;
  }
  
  // Used to fill the save tab with the current session
  fill_from_windows = function () {
    $('#text')[0].value = '';
    chrome.tabs.getCurrent(
      function (current_tab) {
        chrome.windows.getAll(
          {'populate': true},
          function (windows) {
            var i, txt, tabs;
            txt = $('#text')[0];
            for (i = 0; i < windows.length; i++) {
              if (windows[i].type === 'normal' || windows[i].type === 'popup') {
                tabs = windows[i].tabs;
                txt.value += "> Window #" + (i+1) + "\n";
                for (j = 0; j < tabs.length; j++) {
                  if (tabs[j].id !== current_tab.id) {
                    txt.value += tabs[j].url + "\n";
                  }
                }
                txt.value += "\n";
              }
            }
          }
        );
      }
    );
  };
  
  // Set up the buttons
  $('#open').click(function (e) {
    e.preventDefault();
    chrome.windows.getCurrent(
      function (window) {
        var bkg;
        position = {
          'left': window.left,
          'top': window.top,
          'height': window.height,
          'width': window.width
        };
        bkg = chrome.extension.getBackgroundPage();
        bkg.minimizeAll(bkg.launchDndNewWin);
      }
    );
  });
  $('#capture').click(function (e) {
    e.preventDefault();
    fill_from_windows();
  });
  $('#launch').click(function (e) {
    e.preventDefault();
    open_tabs($('#text')[0].value);
  });
  
  // Setup the listening for the dnd popup
  chrome.extension.onMessage.addListener(
    function(request, sender, sendResponse) {
      if (request.content || request.content === '') {
        $('#text')[0].value = request.content;
      }
      chrome.windows.update(
        chrome.windows.WINDOW_ID_CURRENT,
        {
          'left': position['left'],
          'top': position['top'],
          'height': position['height'],
          'width': position['width'],
          'state': 'normal',
          'focused': true
        },
        function () {
          $('#text').focus()
        }
      );
    }
  );
});
