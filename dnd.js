$(function () {
  // Set up the drag and drop
  var holder = $('#open')[0];
  holder.ondragover = function () {
    $(this).addClass('hover');
    return false;
  };
  holder.ondragend = function () { 
    $(this).removeClass('hover'); 
    return false;
  };
  holder.ondrop = function (e) {
    var file, reader;
    $(this).removeClass('hover');
    e.preventDefault();
    file = e.dataTransfer.files[0];
    reader = new FileReader();
    reader.onload = function (event) {
      chrome.extension.sendMessage(
        {'content': event.target.result}
      );
      window.close();
    };
    reader.readAsText(file);
    return false;
  };
  
  $('#cancel').click(function (e) {
    e.preventDefault();
    chrome.extension.sendMessage(
      {'content': false}
    );
    window.close();
  });
});
