// main.js

// DOM Elements
const header = document.querySelector('.header');
const hamburger = document.querySelector('.hamburger');
const mobileMenu = document.querySelector('.mobile-menu');
const resourceGrid = document.querySelector('.resource-grid');

// Mobile Menu Toggle
hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Sticky Header
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll <= 0) {
        header.classList.remove('scroll-up');
        return;
    }

    if (currentScroll > lastScroll && !header.classList.contains('scroll-down')) {
        // Scroll Down
        header.classList.remove('scroll-up');
        header.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && header.classList.contains('scroll-down')) {
        // Scroll Up
        header.classList.remove('scroll-down');
        header.classList.add('scroll-up');
    }
    lastScroll = currentScroll;
});

// Sample Resource Data (This would normally come from an API)
const resourceData = [
    {
        title: "5-Minute Stretch Routine",
        description: "A quick and effective stretch routine to start your day.",
        date: "October 10, 2024",
        duration: "5:00"
    },
    {
        title: "Healthy Eating Tips",
        description: "Learn the basics of healthy eating for better fitness.",
        date: "October 12, 2024",
        duration: "3:30"
    },
    {
        title: "Cardio vs Strength Training",
        description: "Understand the benefits of both cardio and strength training.",
        date: "October 15, 2024",
        duration: "8:00"
    },
    // Add more resources as needed
];

// Create Resource Cards
function createResourceCard(resource) {
    return `
        <div class="resource-card">
            <div class="resource-content">
                <h3>${resource.title}</h3>
                <p>${resource.description}</p>
                <div class="resource-meta">
                    <span>${resource.date}</span>
                    <span>${resource.duration}</span>
                </div>
            </div>
            <div class="resource-controls">
                <button class="play-button" aria-label="Play">▶</button>
            </div>
        </div>
    `;
}

// Render Resource Cards
function renderResources() {
    resourceGrid.innerHTML = resourceData.map(resource =>
        createResourceCard(resource)
    ).join('');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Header scroll effect
    const header = document.querySelector('.header');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mobile menu functionality
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    renderResources();
});

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
            // Close mobile menu if open
            mobileMenu.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });
});
