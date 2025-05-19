/**
 * @jest-environment jsdom
 */
import '@testing-library/jest-dom';
import { fireEvent } from '@testing-library/dom';

global.window.tagUrlBase = '/posts/tag/';

describe('modal.js core behavior', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="post">
        <a class="thumbnail-link" data-full="image1.jpg" data-caption="First #Tag1">Thumbnail 1</a>
        <a class="thumbnail-link" data-full="image2.jpg" data-caption="Second #Tag2">Thumbnail 2</a>
      </div>
      <div id="image-modal" class="is-open"></div>
      <img id="modal-image" />
      <div id="image-caption"></div>
      <div id="image-counter"></div>
      <button id="prev-image"></button>
      <button id="next-image"></button>
    `;

    global.MicroModal = {
      show: jest.fn(),
      close: jest.fn(),
      init: jest.fn(),
    };

    require('../../static/js/modal.js');

    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('should open modal and update image on thumbnail click', () => {
    const thumb = document.querySelector('.thumbnail-link');
    fireEvent.click(thumb);

    expect(global.MicroModal.show).toHaveBeenCalledWith('image-modal');
    const modalImage = document.getElementById('modal-image');
    expect(modalImage.src).toContain('image1.jpg');
    expect(modalImage.alt).toBe('First #Tag1');

    const caption = document.getElementById('image-caption');
    expect(caption.innerHTML).toContain('<a href="/posts/tag/Tag1" class="post-tag">#Tag1</a>');

    const counter = document.getElementById('image-counter');
    expect(counter).toHaveTextContent('1 / 2');
  });

  it('should switch image on next button click', () => {
    const thumb = document.querySelector('.thumbnail-link');
    fireEvent.click(thumb);

    const nextBtn = document.getElementById('next-image');
    fireEvent.click(nextBtn);

    const modalImage = document.getElementById('modal-image');
    expect(modalImage.src).toContain('image2.jpg');
    expect(modalImage.alt).toBe('Second #Tag2');
  });

  it('should close modal on Escape key press', () => {
    const event = new KeyboardEvent('keydown', { key: 'Escape' });
    document.dispatchEvent(event);

    expect(global.MicroModal.close).toHaveBeenCalledWith('image-modal');
  });
});
