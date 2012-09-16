About TabAddict
---------------

### How to Use TabAddict ###

After installation, the TabAddict button will show up to the
right of the omnibox. Click it to open TabAddict.

The TabAddict page has three buttons: _Open_, _Capture_, 
and _Launch_. Below the buttons is the Session Editor.

The _Open_ button loads a file into the Session Editor using
drag-and-drop. The _Capture_ button puts a snapshot of the current
session into the Session Editor. The _Launch_ button launches
the session you are editing.

Interactions with the local file system are very limited in
Chrome Extensions. If you want to save a captured session, you're
going to have to copy-and-paste it into Notepad or something. Sorry.

### The Format for Sessions ###

Each line that starts with `http://` or `https://` will be 
interpreted as a link and cause a new tab to open.

Each `>` will cause an additional window to be opened.

All other lines will be ignored. For example:

    # Google!
    http://www.google.com
    > My favorites
    http://foo.com
    # This one's really awesome
    http://bar.net
    > My less favorite sites
    http://foobar.org

In the above example, `google.com` will be opened in the
current window, `foo.com` and `bar.net` will open in
a second window, and `foobar.org` will open in a third window.

### Credits ###

TabAddict was created by [Peter Nelson][1].

It is provided under the [GPL][2].

Icons were provided by [IcoMoon][3] and [Umut Pulat][4].

[1]: http://peterthenelson.com
[2]: http://www.gnu.org/licenses/gpl.html
[3]: http://icomoon.io/
[4]: http://www.umutpulat.com/
