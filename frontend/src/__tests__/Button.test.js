import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../components/button';

describe('Button Component', () => {
    test('Test 6: Przycisk renderuje się z tekstem', () => {
        render(<Button text='Test Button' active ={true} />);
        expect(screen.getByText('Test Button')).toBeInTheDocument();
        console.log('Button renderuje się poprawnie');
    });

test('Test 7: Zmiana koloru w zależności od stanu', () => {
    const { rerender } = render(<Button text='Test' active = {true} />);
    let button = screen.getByText('Test');
    expect(button).toHaveStyle({ backgroundColor: '#2476FF' });

    rerender(<Button text='Test' active = {false} />);
    button = screen.getByText('Test');
    expect(button).toHaveStyle({ backgroundColor: '#C8E0FF' });
    console.log('Kolor zmienia się poprawnie');
    });

test('Test 8: onClick funkcjonuje', () => {
    const handleClick = jest.fn();
    render(<Button text='Click' active={true} onClick={handleClick} />);

    fireEvent.click(screen.getByText('Click').closest('a'));
    expect(handleClick).toHaveBeenCalled();
    console.log('onClick funkcjonuje poprawnie');
    });

});