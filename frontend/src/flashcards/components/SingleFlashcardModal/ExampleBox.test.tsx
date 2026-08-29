import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import type { ReactNode } from 'react';

import ExampleBox from './ExampleBox';

type WrapperProps = { children: ReactNode };

type ExampleTypographyProps = {
  children: ReactNode;
};

vi.mock('./ExampleBox.styles', () => ({
  StyledExampleBox: ({ children }: WrapperProps) => <section>{children}</section>,
  ExampleTitleBox: ({ children }: WrapperProps) => <div>{children}</div>,
  ExampleTitleTypography: ({ children }: WrapperProps) => <h3>{children}</h3>,
  ExampleTypography: ({ children }: ExampleTypographyProps) => <p>{children}</p>,
}));

describe('ExampleBox', () => {
  it('renders title and provided example text', () => {
    render(<ExampleBox example="The cat perched on the windowsill." />);

    expect(screen.getByText('Example')).toBeInTheDocument();
    expect(screen.getByText('The cat perched on the windowsill.')).toBeInTheDocument();
  });
});
