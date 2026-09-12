import { StyledExampleBox, ExampleTypography, ExampleTitleBox, ExampleTitleTypography } from './ExampleBox.styles';
import type { JSX } from '@emotion/react/jsx-dev-runtime';

type ExampleBoxProps = {
    example: string;
};

/**
 * Component that displays an example sentence in a styled box.
 * 
 * @param {string} example The example sentence to display.
 * @returns {JSX.Element} A JSX element representing the example box.
 */
const ExampleBox = ({ example }: ExampleBoxProps): JSX.Element => {
    return (
        <StyledExampleBox>
            <ExampleTitleBox>
                <ExampleTitleTypography>Example</ExampleTitleTypography>
            </ExampleTitleBox>
            <ExampleTypography variant="body2" gutterBottom>
                {example}
            </ExampleTypography>
        </StyledExampleBox>
    )
};
export default ExampleBox;