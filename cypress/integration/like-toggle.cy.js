describe('Like Toggle Feature', () => {
  beforeEach(() => {
    cy.visit('/posts/');

    cy.intercept('POST', '/likes/ajax/like-toggle/', (req) => {
      const liked = req.body.get('post_id') === '1';
      req.reply({
        statusCode: 200,
        body: {
          liked: liked,
          likes_count: liked ? 1 : 0,
          post_id: 1
        }
      });
    }).as('likeToggle');
  });

  it('toggles like button and updates counter', () => {
    cy.get('.like-button[data-post-id="1"]').as('likeBtn');
    cy.get('#likes-count-1').as('likeCount');

    cy.get('@likeBtn').click();
    cy.wait('@likeToggle');
    cy.get('@likeBtn').should('contain', '❤️ Unlike');
    cy.get('@likeCount').should('contain', '1 like');

    cy.get('@likeBtn').click();
    cy.wait('@likeToggle');
    cy.get('@likeBtn').should('contain', '🤍 Like');
    cy.get('@likeCount').should('contain', '0 likes');
  });

  it('shows error alert on failed request', () => {
    cy.intercept('POST', '/likes/ajax/like-toggle/', {
      statusCode: 500,
      body: { error: 'Server error' }
    }).as('likeToggleFail');

    cy.get('.like-button[data-post-id="1"]').click();
    cy.wait('@likeToggleFail');

    cy.on('window:alert', (txt) => {
      expect(txt).to.contains('Something went wrong. Please try again.');
    });
  });
});
