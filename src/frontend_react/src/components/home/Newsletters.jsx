'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import styles from './Newsletters.module.css';
//import DataService from "../../services/MockDataService"; // Mock
import DataService from "../../services/DataService";


export default function Newsletter() {
    // Component States
    const [newsletters, setNewsletters] = useState([]);

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetNewsletters(4); // Limiting to 4 episodes for the main view
                setNewsletters(response.data);
            } catch (error) {
                console.error('Error fetching podcasts:', error);
                setNewsletters([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);

    return (
        <section className={styles.section} id="newsletters">
            <h2 className={styles.title}>Newsletters</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.newsletterGrid}>
                    {newsletters.map((newsletter) => (
                        <article key={newsletter.id} className={styles.newsletterCard}>
                            <div className={styles.cardHeader}>
                                <span className={styles.date}>{newsletter.date}</span>
                                <span className={styles.readTime}>{newsletter.readTime}</span>
                            </div>

                            <h3 className={styles.newsletterTitle}>{newsletter.title}</h3>

                            <p className={styles.excerpt}>{newsletter.excerpt}</p>

                            <Link href={`/newsletters?id=${newsletter.id}`} className={styles.readMore}>
                                Read More →
                            </Link>
                        </article>
                    ))}
                </div>
                <div className={styles.aboutNewsletter}>
                    <Image
                        src="/assets/newsletter.png"
                        alt="Newsletter Icon"
                        width={240}
                        height={240}
                        style={{
                            width: 'auto',
                            height: 'auto',
                        }}
                    />
                    <h3>About Newsletters</h3>
                    <p>
                        Welcome to gAIn’s Chronicles, your ultimate weekly digest on everything health and fitness!
                        Our newsletters keep you informed with the latest articles, blogs, research, and expert insights on fitness trends,
                        nutrition breakthroughs, workout routines, and more. Stay ahead with cutting-edge knowledge from the very material
                        our LLM is fine-tuned on, curated to keep you informed and help you achieve your health and wellness goals.
                    </p>
                </div>
            </div>
            <div className={styles.viewAllContainer}>
                <Link href="/newsletters" className={styles.viewAllButton}>
                    View All Newsletters
                </Link>
            </div>
        </section>
    );
}
