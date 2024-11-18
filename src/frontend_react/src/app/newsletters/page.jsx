'use client';

import { useState, useEffect, use } from 'react';
import Image from 'next/image';
import Link from 'next/link';
//import DataService from "../../services/MockDataService"; // Mock
import DataService from "../../services/DataService";

// Import the styles
import styles from "./styles.module.css";


export default function NewslettersPage({ searchParams }) {
    const params = use(searchParams);
    const newsletter_id = params.id;

    // Component States
    const [newsletters, setNewsletters] = useState([]);
    const [hasActiveNewsletter, setHasActiveNewsletter] = useState(false);
    const [newsletter, setNewsletter] = useState(null);

    const fetchNewsletter = async (id) => {
        try {
            setNewsletter(null);
            const response = await DataService.GetNewsletter(id);
            setNewsletter(response.data);
            console.log(newsletter);
        } catch (error) {
            console.error('Error fetching newsletter:', error);
            setNewsletter(null);
        }
    };

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetNewsletters(100);
                setNewsletters(response.data);
            } catch (error) {
                console.error('Error fetching podcasts:', error);
                setNewsletters([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);
    useEffect(() => {
        if (newsletter_id) {
            fetchNewsletter(newsletter_id);
            setHasActiveNewsletter(true);
        } else {
            setNewsletter(null);
            setHasActiveNewsletter(false);
        }
    }, [newsletter_id]);

    return (
        <div className={styles.container}>
            {/* Hero Section */}
            <section className={styles.hero}>
                <div className={styles.heroContent}>
                    <h1>gAIn Chronicles</h1>
                    <p>Explore our collection of articles about the world of health and fitness</p>
                </div>
            </section>

            {/* About Section */}
            {!hasActiveNewsletter && (
                <section className={styles.about}>
                    <div className={styles.aboutContent}>
                        <h2>About Newsletters</h2>
                        <p>
                        Welcome to gAIn’s Chronicles, your ultimate weekly digest on everything health and fitness!
                        Our newsletters keep you informed with the latest articles, blogs, research, and expert insights on fitness trends,
                        nutrition breakthroughs, workout routines, and more. Stay ahead with cutting-edge knowledge from the very material
                        our LLM is fine-tuned on, curated to keep you informed and help you achieve your health and wellness goals.
                        </p>
                    </div>
                </section>
            )}

            {/* Newsletter Grid */}
            {!hasActiveNewsletter && (
                <section className={styles.newsletterSection}>
                    <div className={styles.grid}>
                        {newsletters.map((newsletter) => (
                            <article key={newsletter.id} className={styles.card}>
                                <div className={styles.imageContainer}>
                                    <img
                                        src={DataService.GetNewsletterImage(newsletter.image)}
                                        alt={newsletter.title}
                                        width={400}
                                        height={250}
                                        className={styles.image}
                                    />
                                    <span className={styles.category}>{newsletter.category}</span>
                                </div>

                                <div className={styles.content}>
                                    <div className={styles.meta}>
                                        <span className={styles.date}>{newsletter.date}</span>
                                        <span className={styles.readTime}>{newsletter.readTime}</span>
                                    </div>

                                    <h3 className={styles.title}>{newsletter.title}</h3>
                                    <p className={styles.excerpt}>{newsletter.excerpt}</p>

                                    <Link href={`/newsletters?id=${newsletter.id}`} className={styles.readMore}>
                                        Read More <span className={styles.arrow}>→</span>
                                    </Link>
                                </div>
                            </article>
                        ))}
                    </div>
                </section>
            )}

            {/* Newsletter Detail View */}
            {hasActiveNewsletter && newsletter && (
                <section className={styles.newsletterDetail}>
                    <div className={styles.detailContainer}>
                        <Link href="/newsletters" className={styles.backButton}>
                            ← Back to Newsletters
                        </Link>

                        <div className={styles.detailHeader}>
                            <span className={styles.detailCategory}>{newsletter.category}</span>
                            <div className={styles.detailMeta}>
                                <span className={styles.date}>{newsletter.date}</span>
                                <span className={styles.readTime}>{newsletter.readTime}</span>
                            </div>
                            <h1 className={styles.detailTitle}>{newsletter.title}</h1>
                        </div>

                        <div className={styles.detailImageContainer}>
                            <img
                                src={DataService.GetNewsletterImage(newsletter.image)}
                                alt={newsletter.title}
                                className={styles.detailImage}
                            />
                        </div>

                        <div className={styles.detailContent}>
                            <div dangerouslySetInnerHTML={{ __html: newsletter.detail }} />
                        </div>

                        <div className={styles.shareSection}>
                            <h3>Share this article</h3>
                            <div className={styles.shareButtons}>
                                <button className={styles.shareButton}>Twitter</button>
                                <button className={styles.shareButton}>Facebook</button>
                                <button className={styles.shareButton}>LinkedIn</button>
                            </div>
                        </div>
                    </div>
                </section>
            )}
        </div>
    );
}
