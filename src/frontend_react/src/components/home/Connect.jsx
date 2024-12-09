'use client';

import { useState, useEffect } from 'react';
import styles from './Connect.module.css';
import Image from 'next/image';
import stravaLogo from '/public/assets/strava-logo.png';
import { BASE_API_URL } from "../../services/Common";


export default function Connect() {
    const [connected, setConnected] = useState(false);

    // Check if the user is connected to Strava on page load
    useEffect(() => {
        const checkConnection = async () => {
            try {
                const response = await fetch(BASE_API_URL+"/connection_status");
                const data = await response.json();

                // If connected, set the connection state to true
                if (data.connected) {
                    setConnected(true);
                }
            } catch (error) {
                console.error('Error checking connection status:', error);
            }
        };

        checkConnection();
    }, []);

    const handleUnlink = async () => {
        try {
            const response = await fetch(`${BASE_API_URL}/unlink`, {
                method: 'POST', // Ensure the backend supports this method
            });

            if (response.ok) {
                setConnected(false); // Update the state to reflect the disconnection
                alert('Successfully unlinked from Strava.');
            } else {
                console.error('Failed to unlink.');
                alert('Error: Unable to unlink from Strava.');
            }
        } catch (error) {
            console.error('Error during unlink:', error);
            alert('Unexpected error while trying to unlink.');
        }
    };

    return (
        <section className={styles.connect} id="connect">
            <h1 className={styles.title}>Connect Your Apps</h1>
            <div className={styles.underline}></div>
            <div className={styles.content}>
                <p>
                    Seamlessly integrate your favorite health apps with gAIn for a unified fitness and wellness experience.
                </p>
            </div>
            <div className={styles.buttonContainer}>
                {connected ? (
                    <>
                        <button className={styles.connectButton} disabled>
                            <Image src={stravaLogo} alt="Strava Logo" width={20} height={20} />
                            Connected to Strava
                        </button>
                        <button className={styles.unlinkButton}
                            onClick={handleUnlink}
                        >
                            Unlink Strava
                        </button>
                    </>
                ) : (
                    <a href={`${BASE_API_URL}/connect_to_strava`}>
                        <button className={styles.connectButton}>
                            <Image src={stravaLogo} alt="Strava Logo" width={20} height={20} />
                            Connect to Strava
                        </button>
                    </a>
                )}
            </div>
        </section>
    );

    // return (
    //     <section className={styles.connect} id="connect">
    //         <h1 className={styles.title}>Connect Your Apps</h1>
    //         <div className={styles.underline}></div>
    //         <div className={styles.content}>
    //             <p>
    //                 Seamlessly integrate your favorite health apps with gAIn
    //                 for a unified fitness and wellness experience.
    //             </p>
    //         </div>
    //         <div className={styles.buttonContainer}>
    //             {connected ? (
    //                 <button className={styles.connectButton} disabled>
    //                     <Image src={stravaLogo} alt="Strava Logo" width={20} height={20} />
    //                     Connected to Strava
    //                 </button>
    //             ) : (
    //                 // <a href="http://localhost:9000/connect_to_strava">
    //                 <a href={`${BASE_API_URL}/connect_to_strava`}>
    //                     <button className={styles.connectButton}>
    //                         <Image src={stravaLogo} alt="Strava Logo" width={20} height={20} />
    //                         Connect to Strava
    //                     </button>
    //                 </a>
    //             )}
    //         </div>
    //     </section>
    // );
}
