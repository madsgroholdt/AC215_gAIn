'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, CameraAltOutlined } from '@mui/icons-material';
import IconButton from '@mui/material/IconButton';
import { useSearchParams } from 'next/navigation';

// Styles
import styles from './ChatInput.module.css';

export default function ChatInput({ onSendMessage }) {
    // Component States
    const [message, setMessage] = useState('');
    const textAreaRef = useRef(null);
    const searchParams = useSearchParams();
    const id_check = searchParams.get('id');

    const adjustTextAreaHeight = () => {
        const textarea = textAreaRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    };

    // Setup Component
    useEffect(() => {
        adjustTextAreaHeight();
    }, [message]);

    // Handlers
    const handleMessageChange = (e) => {
        setMessage(e.target.value);
    };
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            if (e.shiftKey) {
                // Shift + Enter: add new line
                return;
            } else {
                // Enter only: submit
                e.preventDefault();
                handleSubmit();
            }
        }
    };
    const handleSubmit = () => {
        if (message.trim()) {
            console.log('Submitting message:', message);
            const newMessage = { content: message.trim() };

            // Send the message
            onSendMessage(newMessage);

            // Reset
            setMessage('');
        }
    };

    // Determine background based on page (via query parameter)
    const backgroundStyle = id_check ? '#fff' : 'transparent';

    return (
        <div className={styles.chatInputWrapper} style={{ background: backgroundStyle }}>
            <div className={styles.chatInputContainer}>
                <div className={styles.textareaWrapper}>
                    <textarea
                        ref={textAreaRef}
                        className={styles.chatInput}
                        placeholder="Chat with gAIn..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit();
                            }
                        }}
                        rows={1}
                    />
                    <button
                        className={`${styles.submitButton} ${message.trim() ? styles.active : ''}`}
                        onClick={handleSubmit}
                        disabled={!message.trim()}
                    >
                        <Send />
                    </button>
                </div>
                <div className={styles.inputControls}>
                    <div className={styles.rightControls}>
                        <span className={styles.inputTip}>Use shift + return for new line</span>
                    </div>
                </div>
            </div>
        </div>
    )
}
