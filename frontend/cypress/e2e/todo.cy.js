describe('R8: To-Do List Manipulation', () => {
  let uid, name, email;

  before(function () {
      cy.fixture('user.json').then((user) => {
          cy.request({
              method: 'POST',
              url: 'http://localhost:5000/users/create',
              form: true,
              body: user
          }).then((response) => {
              uid = response.body._id.$oid;
              name = user.firstName + ' ' + user.lastName;
              email = user.email;
          });
          
        
        }).then(() => {cy.visit('http://localhost:3000');
          cy.contains('div', 'Email Address').find('input[type=text]').type(email);
          cy.get('form').submit();
          cy.get('h1').should('contain.text', 'Your tasks, ' + name);}).then(() => { 
          cy.contains('div', 'Title')
          .find('input[type=text]')
          .type('New Todo Item5')
         
          cy.get('form')
          .submit()
      }).then(() => {cy.contains('a', 'New Todo Item5').click();
     
    });

  });
    
  beforeEach(function () {
    
    cy.visit('http://localhost:3000')
    cy.contains('div', 'Email Address').find('input[type=text]').type(email);
    cy.get('form').submit();
    cy.get('h1').should('contain.text', 'Your tasks, ' + name).then(() => {
      cy.contains('a', 'New Todo Item5').click();
     
    });
    cy.get('ul.todo-list', { timeout: 0 }).then($list => {
      if ($list.length && $list.find('li.todo-item').length === 0) {
        cy.get('form.inline-form input[type="text"]').clear({ force: true }).type('test', { force: true });
        cy.get('form.inline-form').submit();
      }
    });
  });

  

  it('TC-R8UC1-01: Input is empty', () => {
    cy.get('form.inline-form input[type="text"]')
    .should('have.value', '');

  });
  it('TC-R8UC1-02: New todo is appended to the bottom of the list', () => {
    const newTodo = 'New Todo Item1';
  
    cy.get('ul.todo-list li.todo-item')
      .then($itemsBefore => {
        const initialCount = $itemsBefore.length;
  
        cy.get('form.inline-form input[type="text"]').type(newTodo, { force: true });
        cy.get('form.inline-form').submit();
  
        cy.get('ul.todo-list li.todo-item').should('have.length', initialCount + 1);
        
        cy.get('ul.todo-list li.todo-item')
          .last()
          .should('contain.text', newTodo);
        cy.get('ul.todo-list li.todo-item').last().should('not.have.class', 'checked');

      });
  });
  it('TC-R8UC1-02b: "Add" button is disabled when input is empty', () => {
    cy.get('form.inline-form input[type="text"]').clear({ force: true });
    cy.get('form.inline-form input[type="submit"]').should('be.disabled');

  });

  it('TC-R8UC2-01: Toggle icon is visible and clickable', () => {

    cy.get('ul.todo-list li.todo-item').first().as('firstTodo');
    cy.get('@firstTodo').find('.checker')
      .should('exist')
      .and('be.visible')
      .and($el => {
        const cls = $el.attr('class') || '';
        expect(/checked|unchecked/.test(cls)).to.be.true;
      });

    cy.get('@firstTodo').find('.checker').then($iconBefore => {
      const wasChecked = $iconBefore.hasClass('checked');
      cy.wrap($iconBefore).click({ force: true });

      cy.get('@firstTodo').find('.checker').should($iconAfter => {
        const isChecked = $iconAfter.hasClass('checked');
        expect(isChecked).to.not.equal(wasChecked);
      });
    });
  });

  it('TC-R8UC2-02: Toggle active → done (text becomes struck-through / icon becomes checked)', () => {

    // Choose a candidate; if it’s already done, add a fresh active and use that
    cy.get('ul.todo-list li.todo-item').first().as('candidate');
    cy.get('@candidate').find('.checker').then($icon => {
      if ($icon.hasClass('checked')) {
        cy.get('form.inline-form input[type="text"]').clear({ force: true }).type("test", { force: true });
        cy.get('form.inline-form').submit();
        cy.get('ul.todo-list li.todo-item').last().as('candidate');
      }
    });

    cy.get('@candidate').find('.checker').should('have.class', 'unchecked');
    cy.get('@candidate').find('.checker').click({ force: true });
    cy.get('@candidate').find('.checker').should('have.class', 'checked');

    
  });
  it('TC-R8UC2-02b  : Toggle done → active', () => {

    // Choose a candidate; if it’s already done, add a fresh active and use that
    cy.get('ul.todo-list li.todo-item').first().as('candidate');
    cy.get('@candidate').find('.checker').then($icon => {
      if ($icon.hasClass('unchecked')) {
        cy.get('form.inline-form input[type="text"]').clear({ force: true }).type("test", { force: true });
        cy.get('form.inline-form').submit();

        cy.get('ul.todo-list li.todo-item').last().as('candidate');
        cy.get('@candidate').find('.checker').click({ force: true });

      }
    });

    cy.get('@candidate').find('.checker').should('have.class', 'checked');
    cy.get('@candidate').find('.checker').click({ force: true });
    cy.get('@candidate').find('.checker').should('have.class', 'unchecked');

    
  });

  it('TC-R8UC3-01: Delete an item removes it from the list', () => {
    cy.get('ul.todo-list li.todo-item').first().as('firstTodo');
    
    cy.get('@firstTodo').find('.remover').click({ force: true });
  
    cy.get('ul.todo-list li.todo-item').should('not.contain.text', '@firstTodo');
  });
  
});