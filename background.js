var bkg = chrome.extension.getBackgroundPage();

bkg.launchDndNewWin = function () {
  chrome.windows.create(
    {
      'url': chrome.extension.getURL('dnd.html'),
      'left': 600,
      'top': 150,
      'width': 430,
      'height': 545
    },
    // NOTE: chrome currently has a bug where
    // if the current window is maximized, any
    // windows launched will also be maximized.
    // We don't have to worry about this at the
    // moment since we minimize everything else first
    function (win) {}
  );
};

bkg.launchMain = function () {
  chrome.tabs.create(
    {
      'url': chrome.extension.getURL('launch.html')
    },
    function (win) {}
  );
};

bkg.minimizeAll = function (onmin) {
  var data = {
    'onmin': onmin,
    'min_callback': function () {
      this.count--;
      if (this.count === 0) {
        this.onmin();
      }
    },
    'getall_callback': function (wins) {
      var i;
      this.count = wins.length;
      for (i = 0; i < wins.length; i++) {
        chrome.windows.update(
          wins[i].id,
          { 'state': 'minimized' },
          this.min_callback.bind(this)
        );
      }
    }
  };
  chrome.windows.getAll(data.getall_callback.bind(data));
};

chrome.browserAction.onClicked.addListener(function(tab) {
  var bkg = chrome.extension.getBackgroundPage();
  bkg.launchMain();
});