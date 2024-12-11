// src/MyComponent.test.js
import React from "react";
import { render, screen } from "@testing-library/react";
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from "react-router-dom";
import FileUploadForm from "./FileUploadForm";

test('FileUploadForm component renders upload title', () => {
    // Render the FileUploadForm component in MemoryRouter to provide the necessary router context
    render(
        <MemoryRouter>
            <FileUploadForm />
        </MemoryRouter>
    );

    const titleElement = screen.getByRole('heading', { name: /File Upload/i });
    expect(titleElement).toBeInTheDocument(); // Check title exists
});

test('FileUploadForm component, upload button is clickable', async () => {
    render(
        <MemoryRouter>
            <FileUploadForm />
        </MemoryRouter>
    );

    const uploadButton = screen.getByRole('button', { name: /Upload File/i });
    expect(uploadButton).toBeInTheDocument(); // Check button exists
    expect(uploadButton).toBeEnabled(); // Check it's clickable
});

// NOT WORKING
test('FileUploadForm component, form submission request success', async () => {
    const filenameValue = "test.txt";
    let messageValue = "The file: " + filenameValue + " was uploaded successfully."

    // Mock the fetch API
    const mockFetch = jest.fn(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ message: messageValue, filename: filenameValue }),
        })
    );
    global.fetch = mockFetch;

    render(<FileUploadForm userID={1} onUploadSuccess={jest.fn()} />);

    // Create a mock file
    const mockFile = new File(["file content"], filenameValue, { type: "text/plain" });

    // Select the file in the file input
    const fileInput = screen.getByTestId('fileInput');
    await userEvent.upload(fileInput, mockFile);

    // Click the upload button
    const uploadButton = screen.getByRole('button', { name: /Upload File/i });
    await userEvent.click(uploadButton);

    // Check the mock fetch request is made and returns a result
    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/upload-file'),
        expect.objectContaining({
            method: 'POST',
            body: expect.any(FormData),
        })
    );

    // Check that file upload message is shown during upload
    const formMessage = screen.getByText(/File upload in progress/i);
    expect(formMessage).toBeVisible();
});