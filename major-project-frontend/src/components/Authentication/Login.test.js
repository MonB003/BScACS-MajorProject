import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import Login from './Login';

test('Login component renders toolkit name', () => {
    // Render the Login component in MemoryRouter to provide the necessary router context
    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );

    const toolkitElement = screen.getByText(/Secure MoniTor Toolkit/i); // Find text in the DOM
    expect(toolkitElement).toBeInTheDocument(); // Check it exists
});

test('Login component renders form fields', async () => {
    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );

    const usernameElement = await screen.findByPlaceholderText(/Username/i); // Find text in the DOM
    const passwordElement = await screen.findByPlaceholderText(/Password/i); // Find text in the DOM
    expect(usernameElement).toBeInTheDocument(); // Check it exists
    expect(passwordElement).toBeInTheDocument(); // Check it exists
});

test('Login component, login button is clickable', async () => {
    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );

    const loginButton = screen.getByRole('button', { name: /Login/i });
    expect(loginButton).toBeInTheDocument();
    expect(loginButton).toBeEnabled(); // Check it's clickable
});

test('Login component, type in username and password fields', async () => {
    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );

    const usernameField = await screen.findByPlaceholderText(/Username/i);
    const passwordField = await screen.findByPlaceholderText(/Password/i);
    // Values to type
    let usernameValue = 'user';
    let passwordValue = 'password';

    // Type in the text fields
    userEvent.type(usernameField, usernameValue);
    userEvent.type(passwordField, passwordValue);
    // Check the typed values are in the text fields
    expect(usernameField).toHaveValue(usernameValue);
    expect(passwordField).toHaveValue(passwordValue);
});

test('Login component, form submission request success', async () => {
    let usernameValue = 'user';
    let passwordValue = 'password';

    const mockFetch = jest.fn(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ user_id: 1, username: usernameValue }),
        })
    );
    global.fetch = mockFetch;

    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );

    const usernameField = await screen.findByPlaceholderText(/Username/i);
    const passwordField = await screen.findByPlaceholderText(/Password/i);
    const loginButton = screen.getByRole('button', { name: /Login/i });

    // Type in the text fields
    userEvent.type(usernameField, usernameValue);
    userEvent.type(passwordField, passwordValue);
    userEvent.click(loginButton);

    // Check the mock fetch request is made and returns a result
    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining('/login'), expect.any(Object));
});