import { render, screen } from '@testing-library/react';
import HomePage from '../pages/homePage';

describe('HomePage Component', () => {
    test('Test 9: Strona główna się renderuje', () => {
    render(<HomePage />);
    expect(screen.getByText('Upload your images')).toBeInTheDocument();
    expect(screen.getByText('Cropped Image')).toBeInTheDocument();
    expect(screen.getByText('Reference Image')).toBeInTheDocument();
    console.log('HomePage renderuje się poprawnie');
    });

    test('Test 10: Przycisk nieaktywny bez plików', () => {
        render(<HomePage />);
        const button = screen.getByText('Process image');
        expect(button.closest('button')).toHaveStyle({
            backgroundColor: '#C8E0FF'
        });
        console.log('Przycisk nieaktywny domyślnie');
    });
});