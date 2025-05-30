describe('EduTask To-Do GUI Tests (R8UC1, R8UC2, R8UC3)', () => {
  const baseUrl = 'http://localhost:5000';
  const taskId = '12345';

  before(() => {
    cy.request('POST', `${baseUrl}/api/login`, {
      username: 'testuser',
      password: 'testpass'
    });
  });

  beforeEach(() => {
    cy.request('DELETE', `${baseUrl}/api/tasks/${taskId}/todos`);

    cy.request('POST', `${baseUrl}/api/tasks/${taskId}/todos`, {
      description: 'Existing todo item',
      done: false
    });

    cy.visit(`/taskdetail/${taskId}`);
    cy.get('ul.todo-list').should('exist');
  });

  after(() => {
    cy.request('DELETE', `${baseUrl}/api/tasks/${taskId}/todos`);
  });

  it('R8UC1 - user can create a new todo item', () => {
    const newTodo = 'New todo item from GUI';

    cy.get('input[placeholder="Add a new todo item"]').type(newTodo);
    cy.get('input[type="submit"][value="Add"]').click();
    cy.contains('li.todo-item', newTodo).should('exist');
  });

  it('R8UC2 - user can toggle a todo item done status', () => {
    cy.contains('li.todo-item', 'Existing todo item').as('todo');
    cy.get('@todo').find('span.checker').click();
    cy.get('@todo').find('span.checker').should('have.class', 'checked'); // or however your app reflects 'done'
  });

  it('R8UC3 - user can delete a todo item', () => {
    cy.contains('li.todo-item', 'Existing todo item').as('todoToDelete');
    cy.get('@todoToDelete').find('span.remover').click();
    cy.contains('li.todo-item', 'Existing todo item').should('not.exist');
  });
});
