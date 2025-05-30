describe('EduTask To-Do GUI Tests (R8UC1, R8UC2, R8UC3)', () => {
    beforeEach(() => {
      cy.visit('/taskdetail/12345');
      cy.get('ul.todo-list').should('exist');
    });
  
    it('R8UC1 - user can create a new todo item', () => {
      const newTodo = 'Test todo item from Cypress';
  
      cy.get('input[placeholder="Add a new todo item"]').type(newTodo);
      cy.get('input[type="submit"][value="Add"]').click();
      cy.contains('li.todo-item', newTodo).should('exist');
    });
  
    it('R8UC2 - user can toggle a todo item done status', () => {
      cy.get('ul.todo-list li.todo-item').first().as('firstTodo');
      cy.get('@firstTodo').find('span.checker').as('toggleBtn');
  
      cy.get('@toggleBtn').then($el => {
        const initialClass = $el.hasClass('checked') ? 'checked' : 'unchecked';
        cy.get('@toggleBtn').click();
        cy.get('@toggleBtn').should('have.class', initialClass === 'checked' ? 'unchecked' : 'checked');
      });
    });
  
    it('R8UC3 - user can delete a todo item', () => {
      const todoToDelete = 'Todo to delete';
  
      cy.get('input[placeholder="Add a new todo item"]').type(todoToDelete);
      cy.get('input[type="submit"][value="Add"]').click();
  
      cy.contains('li.todo-item', todoToDelete).as('todoItemToDelete').should('exist');
      cy.get('@todoItemToDelete').find('span.remover').click();
      cy.contains('li.todo-item', todoToDelete).should('not.exist');
    });
  });
  