document.addEventListener('DOMContentLoaded', () => {
  const holder = document.getElementById('open');

  holder.addEventListener('dragover', e => {
    e.preventDefault();
    holder.classList.add('hover');
  });

  holder.addEventListener('dragleave', () => {
    holder.classList.remove('hover');
  });

  holder.addEventListener('drop', e => {
    e.preventDefault();
    holder.classList.remove('hover');
    const file = e.dataTransfer.files[0];
    const reader = new FileReader();
    reader.onload = event => {
      chrome.runtime.sendMessage({ content: event.target.result });
      window.close();
    };
    reader.readAsText(file);
  });

  document.getElementById('cancel').addEventListener('click', e => {
    e.preventDefault();
    chrome.runtime.sendMessage({ content: false });
    window.close();
  });
});
