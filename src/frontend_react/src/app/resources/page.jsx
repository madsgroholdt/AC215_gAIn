'use client';

import { useState, useEffect, use } from 'react';
import Image from 'next/image';
import Link from 'next/link';
//import DataService from "../../services/MockDataService"; // Mock
import DataService from "../../services/DataService";

// Import the styles
import styles from "./styles.module.css";


export default function ResourcesPage({ searchParams }) {
    const params = use(searchParams);
    const resource_id = params.id;

    // Component States
    const [resources, setResources] = useState([]);
    const [hasActiveResource, setHasActiveResource] = useState(false);
    const [resource, setResource] = useState(null);

    const fetchResource = async (id) => {
        try {
            setResource(null);
            const response = await DataService.GetResource(id);
            setResource(response.data);
            console.log(resource);
        } catch (error) {
            console.error('Error fetching resource:', error);
            setResource(null);
        }
    };

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetResources(100);
                setResources(response.data);
            } catch (error) {
                console.error('Error fetching podcasts:', error);
                setResources([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);
    useEffect(() => {
        if (resource_id) {
            fetchResource(resource_id);
            setHasActiveResource(true);
        } else {
            setResource(null);
            setHasActiveResource(false);
        }
    }, [resource_id]);

    return (
        <div className={styles.container}>
            {/* Hero Section */}
            <section className={styles.hero}>
                <div className={styles.heroContent}>
                    <h1>Cheese Chronicles</h1>
                    <p>Explore our collection of articles about the fascinating world of cheese and AI</p>
                </div>
            </section>

            {/* About Section */}
            {!hasActiveResource && (
                <section className={styles.about}>
                    <div className={styles.aboutContent}>
                        <h2>About Resources</h2>
                        <p>
                            Welcome to Formaggio.me's Cheese Chronicles, your weekly digest of all things cheese!
                            Our resource dive deep into the fascinating world of artisanal cheese-making,
                            featuring expert insights, tasting notes, and the latest innovations in cheese technology.
                        </p>
                    </div>
                </section>
            )}

            {/* Resource Grid */}
            {!hasActiveResource && (
                <section className={styles.resourceSection}>
                    <div className={styles.grid}>
                        {resources.map((resource) => (
                            <article key={resource.id} className={styles.card}>
                                <div className={styles.imageContainer}>
                                    <img
                                        src={DataService.GetResourceImage(resource.image)}
                                        alt={resource.title}
                                        width={400}
                                        height={250}
                                        className={styles.image}
                                    />
                                    <span className={styles.category}>{resource.category}</span>
                                </div>

                                <div className={styles.content}>
                                    <div className={styles.meta}>
                                        <span className={styles.date}>{resource.date}</span>
                                        <span className={styles.readTime}>{resource.readTime}</span>
                                    </div>

                                    <h3 className={styles.title}>{resource.title}</h3>
                                    <p className={styles.excerpt}>{resource.excerpt}</p>

                                    <Link href={`/resources?id=${resource.id}`} className={styles.readMore}>
                                        Read More <span className={styles.arrow}>→</span>
                                    </Link>
                                </div>
                            </article>
                        ))}
                    </div>

                    {/* Resource Subscription */}
                    <div className={styles.subscriptionBox}>
                        <h3>Stay Updated</h3>
                        <p>Subscribe to receive our latest resource directly in your inbox.</p>
                        <form className={styles.subscriptionForm}>
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className={styles.emailInput}
                            />
                            <button type="submit" className={styles.subscribeButton}>
                                Subscribe
                            </button>
                        </form>
                    </div>
                </section>
            )}

            {/* Resource Detail View */}
            {hasActiveResource && resource && (
                <section className={styles.resourceDetail}>
                    <div className={styles.detailContainer}>
                        <Link href="/resource" className={styles.backButton}>
                            ← Back to Resources
                        </Link>

                        <div className={styles.detailHeader}>
                            <span className={styles.detailCategory}>{resource.category}</span>
                            <div className={styles.detailMeta}>
                                <span className={styles.date}>{resource.date}</span>
                                <span className={styles.readTime}>{resource.readTime}</span>
                            </div>
                            <h1 className={styles.detailTitle}>{resource.title}</h1>
                        </div>

                        <div className={styles.detailImageContainer}>
                            <img
                                src={DataService.GetResourceImage(resource.image)}
                                alt={resource.title}
                                className={styles.detailImage}
                            />
                        </div>

                        <div className={styles.detailContent}>
                            <div dangerouslySetInnerHTML={{ __html: resource.detail }} />
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