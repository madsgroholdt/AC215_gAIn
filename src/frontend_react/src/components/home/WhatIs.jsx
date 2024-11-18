import Image from 'next/image';
import styles from './WhatIs.module.css';

export default function WhatIs() {
    return (
        <section className={styles.section}>
            <h2 className={styles.title}>Welcome to gAIn!</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.textContent}>
                    <h3 className={styles.subtitle}>Optimize Your Health Journey with <strong>gAIn</strong></h3>

                    <p>
                        Imagine having a personal health and fitness coach that not only knows the latest research but
                        also understands your unique lifestyle. gAIn uses AI-powered technology to consolidate expert
                        advice and seamlessly integrate with your personal fitness devices to provide you with customized
                        workout plans, nutrition suggestions, and wellness insights.
                    </p>

                    <p>
                        By connecting gAIn with your fitness devices and health data, you receive tailored suggestions that evolve
                        with your progress. Dive deeper into your fitness journey with our interactive chatbot, designed to answer
                        questions about your goals, workout plans, dietary needs, and more.
                    </p>

                    <p>
                        Whether you’re setting a fitness routine, planning meals, or seeking advice on how to achieve your goals,
                        gAIn is here to provide the guidance you need. Our app brings together personalized coaching, cutting-edge
                        health insights, and practical tips in one powerful platform.
                    </p>

                    <p>
                        gAIn is more than an app; it's your all-in-one health and fitness assistant, dedicated to helping you reach
                        your full potential. From advice on workouts to tips on recovery, gAIn is equipped to support every aspect
                        of your journey.
                    </p>

                    <div className={styles.features}>
                        <h4>Key Features:</h4>
                        <ul>
                            <li>Personalized fitness and health recommendations using AI-powered technology</li>
                            <li>Interactive chatbot for answering health and fitness-related questions</li>
                            <li>In-depth insights on workout plans, diet suggestions, and recovery techniques</li>
                            <li>Seamless integration with popular fitness devices and apps</li>
                            <li>Perfect for fitness enthusiasts and anyone looking to improve their health and wellness</li>
                        </ul>
                    </div>
                </div>

                <div className={styles.imageContainer}>
                    <Image
                        src="/assets/gain_logo.png"
                        alt="gAIn logo with robot"
                        fill
                        sizes="(max-width: 768px) 100vw, 800px"
                        style={{
                            objectFit: 'cover', // Ensures the image fills the container
                            objectPosition: 'top', // Aligns the image to the top
                        }}
                        priority
                    />
                </div>
            </div>
        </section>
    );
}
