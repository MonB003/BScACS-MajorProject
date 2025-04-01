import React from "react";
import { render, screen } from "@testing-library/react";
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from "react-router-dom";
import FileForm from "./FileForm";

test('FileForm component renders upload title', () => {
    // Render the FileForm component in MemoryRouter to provide the necessary router context
    render(
        <MemoryRouter>
            <FileForm backendPath={"upload-file"} />
        </MemoryRouter>
    );

    const titleElement = screen.getByRole('heading', { name: /File Upload/i });
    expect(titleElement).toBeInTheDocument(); // Check title exists
});

test('FileForm component renders check title', () => {
    // Render the FileForm component in MemoryRouter to provide the necessary router context
    render(
        <MemoryRouter>
            <FileForm backendPath={"check-file"} />
        </MemoryRouter>
    );

    const titleElement = screen.getByRole('heading', { name: /Check a File/i });
    expect(titleElement).toBeInTheDocument(); // Check title exists
});

test('FileForm component, upload button is clickable', async () => {
    render(
        <MemoryRouter>
            <FileForm backendPath={"upload-file"} />
        </MemoryRouter>
    );

    const uploadButton = screen.getByRole('button', { name: /Upload File/i });
    expect(uploadButton).toBeInTheDocument(); // Check button exists
    expect(uploadButton).toBeEnabled(); // Check it's clickable
});

test('FileForm component, check button is clickable', async () => {
    render(
        <MemoryRouter>
            <FileForm backendPath={"check-file"} />
        </MemoryRouter>
    );

    const checkButton = screen.getByRole('button', { name: /Check File/i });
    expect(checkButton).toBeInTheDocument(); // Check button exists
    expect(checkButton).toBeEnabled(); // Check it's clickable
});

test('FileForm component, type in file path field', async () => {
    render(
        <MemoryRouter>
            <FileForm backendPath={"upload-file"} />
        </MemoryRouter>
    );

    const filePathField = await screen.findByPlaceholderText(/File path/i);
    // Value to type
    let filePathValue = 'data';

    // Type in the text fields
    userEvent.type(filePathField, filePathValue);
    // Check the typed values are in the text fields
    expect(filePathField).toHaveValue(filePathValue);
});