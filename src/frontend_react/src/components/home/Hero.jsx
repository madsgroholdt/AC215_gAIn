'use client';

import Link from 'next/link';
import styles from './Hero.module.css';

export default function Hero() {
    return (
        <section
            className="relative h-screen flex items-center justify-center text-center bg-black"
            style={{
                backgroundImage: "linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/assets/hero_background.jpg')",
                backgroundSize: 'cover',
                backgroundPosition: 'center'
            }}
        >
            <div className="container mx-auto px-4">
                <h1 className="text-5xl md:text-7xl font-playfair text-white mb-6">
                    gAIn is here
                </h1>
                <p className="text-xl md:text-2xl text-white">
                    Your personal health and fitness expert
                </p>
                {/* Chat Now Button */}
                <Link href="/chat" passHref>
                    <button className={styles.chatNowButton}>
                        Chat now!
                    </button>
                </Link>
            </div>
        </section>
    )
}
