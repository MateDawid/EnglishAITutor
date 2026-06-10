import List from '@mui/material/List';
import LeftbarItem from './LeftbarItem.tsx';
import { OuterBox, InnerBox } from './Leftbar.styles';

import AssistantIcon from '@mui/icons-material/Assistant';
import StickyNote2Icon from '@mui/icons-material/StickyNote2';

const items = [
    { url: '/', label: 'Flashcards', icon: <StickyNote2Icon /> },
    { url: '/chat', label: 'AI Tutor', icon: <AssistantIcon /> },
]
/**
 * Leftbar component to display subpages navigation on left side of screen
 */
const Leftbar = () => {
    return (
        <OuterBox sx={{ display: { xs: 'none', sm: 'none', md: 'block' } }}>
            <InnerBox>
                <List>
                    {items.map((item) => (
                        <LeftbarItem
                            key={item.url}
                            url={item.url}
                            displayText={item.label}
                            icon={item.icon}
                        />
                    ))}
                </List>
            </InnerBox>
        </OuterBox>
    );
};

export default Leftbar;