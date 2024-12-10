import Hero from '@/components/home/Hero';
import About from '@/components/home/About';
import Newsletters from '@/components/home/Newsletters';
import WhatIs from '@/components/home/WhatIs';
import Connect from '@/components/home/Connect'

export default function Home() {
    return (
        <>
            <Hero />
            <WhatIs></WhatIs>
            <Connect></Connect>
            <Newsletters />
            <About />
        </>
    )
}
