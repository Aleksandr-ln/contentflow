document.addEventListener('DOMContentLoaded', function () {
  const thumbnails = Array.from(document.querySelectorAll('.thumbnail-link'));
  let currentIndex = 0;
  let currentImages = [];

  function preserveLineBreaks(text) {
    return text.replace(/\r\n|\r/g, '\n').replace(/\n/g, '<br>');
  }

  function linkifyHashtags(text) {
    const tagBase = window.tagUrlBase || "/posts/tag/";
    const seen = new Set();
    return text.replace(/#([\wа-яА-ЯёЁїЇіІєЄґҐ]+)/gu, (_, tag) => {
        if (seen.has(tag)) return '';
        seen.add(tag);
        return `<a href="${tagBase}${encodeURIComponent(tag)}" class="post-tag">#${tag}</a>`;
    });
  }

  function updateModalImage(index) {
    const img = currentImages[index];
    const modalImage = document.getElementById('modal-image');
    const caption = document.getElementById('image-caption');
    const counter = document.getElementById('image-counter');

    const url = img.dataset.full;
    if (!url) return;

    modalImage.src = url;
    modalImage.alt = img.dataset.caption || '';

    const rawCaption = img.dataset.caption || 'No description';
    let decodedCaption = rawCaption;
    try {
      decodedCaption = JSON.parse(`"${rawCaption}"`);
    } catch (e) {
      decodedCaption = rawCaption;
    }

    decodedCaption = decodedCaption.replace(/([\n\r]|<br\s*\/?>)+$/gi, '');
    const htmlCaption = linkifyHashtags(preserveLineBreaks(decodedCaption))
                      .replace(/(<br\s*\/?>)+(<a )/i, '$2');
    caption.innerHTML = htmlCaption;

    counter.textContent = `${index + 1} / ${currentImages.length}`;
  }

  thumbnails.forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      const postElement = link.closest('.post');
      if (!postElement) return;
      currentImages = Array.from(postElement.querySelectorAll('.thumbnail-link'));
      currentIndex = currentImages.indexOf(link);
      MicroModal.show('image-modal');
      updateModalImage(currentIndex);
    });
  });

  document.getElementById('prev-image').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
    updateModalImage(currentIndex);
  });

  document.getElementById('next-image').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % currentImages.length;
    updateModalImage(currentIndex);
  });

  document.addEventListener('keydown', event => {
    if (!document.getElementById('image-modal').classList.contains('is-open')) return;
    if (event.key === 'ArrowLeft') {
      currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
      updateModalImage(currentIndex);
    } else if (event.key === 'ArrowRight') {
      currentIndex = (currentIndex + 1) % currentImages.length;
      updateModalImage(currentIndex);
    } else if (event.key === 'Escape') {
      MicroModal.close('image-modal');
    }
  });
});

MicroModal.init();
