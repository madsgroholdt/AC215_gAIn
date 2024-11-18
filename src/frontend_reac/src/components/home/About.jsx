import Link from 'next/link';
import styles from './About.module.css';

export default function About() {
    return (
        <section className={styles.about} id="about">
            <h1 className={styles.title}>About Us</h1>
            <div className={styles.underline}></div>
            <div className={styles.content}>
                <p>
                Welcome to <strong>gAIn</strong>, your one-stop AI-powered platform for personalized health and fitness guidance.
                Using advanced Retrieval-Augmented Generation (RAG) technology and state-of-the art LLMs, gAIn brings expert knowledge on fitness, nutrition, and well-being directly to you.
                </p>

                <p>
                    Please note that this is a demonstration project, so some features may be incomplete or still under
                    development. However, we hope you enjoy exploring it and would love to hear your thoughts! Feel free to
                    send us an email with comments.
                </p>

                <p>
                    Thank you for visiting <strong>gAIn</strong>, and we hope you have fun exploring the intersection of fitness and
                    AI!
                </p>

                <Link href="mailto:jakepappo@college.harvard.edu" className={styles.contactButton}>
                    CONTACT US
                </Link>
            </div>
        </section>
    );
}
