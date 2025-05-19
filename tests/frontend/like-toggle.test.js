/**
 * @jest-environment jsdom
 */
import '@testing-library/jest-dom';
import { fireEvent } from '@testing-library/dom';

import '../../static/js/like-toggle.js';

describe('like-toggle.js', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <button class="like-button" data-post-id="1" data-liked="false">🤍 Like</button>
      <span id="likes-count-1">0 likes</span>
    `;

    Object.defineProperty(document, 'cookie', {
      writable: true,
      value: 'csrftoken=faketoken'
    });

    global.fetch = jest.fn();

    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('should toggle like button and update likes count', async () => {
    const button = document.querySelector('.like-button');
    const countSpan = document.getElementById('likes-count-1');

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ liked: true, likes_count: 5, post_id: 1 })
    });

    fireEvent.click(button);

    await new Promise(process.nextTick);

    expect(fetch).toHaveBeenCalledWith('/likes/ajax/like-toggle/', expect.any(Object));
    expect(button).toHaveTextContent('❤️ Unlike');
    expect(button.dataset.liked).toBe('true');
    expect(countSpan).toHaveTextContent('5 likes');
  });

  it('should handle fetch error gracefully', async () => {
    const button = document.querySelector('.like-button');

    fetch.mockRejectedValueOnce(new Error('Network Error'));
    global.alert = jest.fn();

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    fireEvent.click(button);
    await new Promise(process.nextTick);

    expect(global.alert).toHaveBeenCalledWith('Something went wrong. Please try again.');
    consoleErrorSpy.mockRestore();
  });
});
