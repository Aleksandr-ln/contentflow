describe('Modal Image Viewer', () => {
  beforeEach(() => {
    cy.visit('/posts/');

    cy.get('.thumbnail-link').should('exist');
  });

  it('opens modal and displays correct image and caption', () => {
    cy.get('.thumbnail-link').first().click();

    cy.get('#image-modal').should('have.class', 'is-open');
    cy.get('#modal-image').should('have.attr', 'src').and('not.be.empty');
    cy.get('#image-caption').should('contain', '#'); // має бути хоч один тег
    cy.get('#image-counter').should('match', /1 \/ \d+/); // 1 / N
  });

  it('navigates to next and previous image', () => {
    cy.get('.thumbnail-link').first().click();

    cy.get('#next-image').click();
    cy.get('#image-counter').should('match', /2 \/ \d+/);

    cy.get('#prev-image').click();
    cy.get('#image-counter').should('match', /1 \/ \d+/);
  });

  it('navigates with keyboard arrows', () => {
    cy.get('.thumbnail-link').first().click();

    cy.get('body').trigger('keydown', { key: 'ArrowRight' });
    cy.get('#image-counter').should('match', /2 \/ \d+/);

    cy.get('body').trigger('keydown', { key: 'ArrowLeft' });
    cy.get('#image-counter').should('match', /1 \/ \d+/);
  });

  it('closes modal with Escape key', () => {
    cy.get('.thumbnail-link').first().click();

    cy.get('body').trigger('keydown', { key: 'Escape' });

    cy.get('#image-modal').should('not.have.class', 'is-open');
  });
});
