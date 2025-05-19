function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
  const csrftoken = getCookie('csrftoken');
  document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', async () => {
      const postId = button.dataset.postId;
      const formData = new FormData();
      formData.append('post_id', postId);

      try {
        const response = await fetch("/likes/ajax/like-toggle/", {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: formData
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        button.innerHTML = data.liked ? '❤️ Unlike' : '🤍 Like';
        button.dataset.liked = data.liked.toString();

        const countSpan = document.getElementById(`likes-count-${data.post_id}`);
        countSpan.textContent = `${data.likes_count} like${data.likes_count === 1 ? '' : 's'}`;
      } catch (error) {
        console.error('Error toggling like:', error);
        alert('Something went wrong. Please try again.');
      }
    });
  });
});
