/**
 * РАЗ И НАВСЕГДА — Интерактивные эффекты
 * Яйцо, трещины, вылупление, свет
 */

(function() {
    'use strict';

    // ==========================================
    // STATE
    // ==========================================

    const state = {
        scrollProgress: 0,
        hatchStage: 0,
        crackCount: 0,
        isEggCracked: false,
        mouseX: 0,
        mouseY: 0
    };

    // ==========================================
    // SCROLL PROGRESS
    // ==========================================

    function updateScrollProgress() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        state.scrollProgress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

        // Update CSS variable
        document.documentElement.style.setProperty('--scroll-progress', `${state.scrollProgress}%`);

        // Update progress bar
        const progressBar = document.querySelector('.hatch-progress__bar');
        if (progressBar) {
            progressBar.style.width = `${state.scrollProgress}%`;
        }

        // Update hatch label
        const hatchLabel = document.querySelector('.hatch-label');
        if (hatchLabel) {
            const stage = getHatchStage(state.scrollProgress);
            const labels = [
                'Яйцо целое',
                'Первые трещины',
                'Пробуждение',
                'Скорлупа ломается',
                'Вылупление!'
            ];
            hatchLabel.textContent = labels[stage];
        }

        // Update hatch stage
        updateHatchStage();
    }

    function getHatchStage(progress) {
        if (progress < 20) return 0;
        if (progress < 40) return 1;
        if (progress < 60) return 2;
        if (progress < 80) return 3;
        return 4;
    }

    function updateHatchStage() {
        const newStage = getHatchStage(state.scrollProgress);
        if (newStage !== state.hatchStage) {
            state.hatchStage = newStage;
            document.body.setAttribute('data-hatch-stage', newStage);

            // Trigger stage change effects
            if (newStage > 0) {
                triggerCrackParticles();
            }
        }
    }

    // ==========================================
    // INTERACTIVE EGG
    // ==========================================

    function initEgg() {
        const eggContainer = document.querySelector('.hero__egg-container');
        if (!eggContainer) return;

        // Add cracks SVG
        const cracksSvg = createCracksSVG();
        eggContainer.appendChild(cracksSvg);

        // Click to crack
        eggContainer.addEventListener('click', function(e) {
            if (state.crackCount < 5) {
                addCrack(e.offsetX, e.offsetY, eggContainer);
                state.crackCount++;

                if (state.crackCount >= 3) {
                    eggContainer.classList.add('cracking');
                    state.isEggCracked = true;
                }

                // Particles on click
                triggerClickParticles(e.clientX, e.clientY);
            }
        });

        // Hover glow effect
        eggContainer.addEventListener('mousemove', function(e) {
            const rect = eggContainer.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width - 0.5) * 20;
            const y = ((e.clientY - rect.top) / rect.height - 0.5) * 20;

            const egg = eggContainer.querySelector('.hero__egg');
            if (egg) {
                egg.style.transform = `rotateY(${x}deg) rotateX(${-y}deg)`;
            }
        });

        eggContainer.addEventListener('mouseleave', function() {
            const egg = eggContainer.querySelector('.hero__egg');
            if (egg) {
                egg.style.transform = 'rotateY(0) rotateX(0)';
            }
        });
    }

    function createCracksSVG() {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.classList.add('hero__cracks');
        svg.setAttribute('viewBox', '0 0 300 380');
        svg.setAttribute('preserveAspectRatio', 'none');

        // Container for crack lines
        const cracksGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        cracksGroup.id = 'crack-lines';
        svg.appendChild(cracksGroup);

        return svg;
    }

    function addCrack(x, y, container) {
        const svg = container.querySelector('.hero__cracks');
        if (!svg) return;

        const cracksGroup = svg.querySelector('#crack-lines');
        if (!cracksGroup) return;

        // Scale coordinates to viewBox
        const scaleX = 300 / container.offsetWidth;
        const scaleY = 380 / container.offsetHeight;
        const cx = x * scaleX;
        const cy = y * scaleY;

        // Create random crack pattern
        const numSegments = 3 + Math.floor(Math.random() * 3);
        let path = `M ${cx} ${cy}`;

        for (let i = 0; i < numSegments; i++) {
            const angle = Math.random() * Math.PI * 2;
            const length = 20 + Math.random() * 40;
            const endX = cx + Math.cos(angle) * length;
            const endY = cy + Math.sin(angle) * length;

            // Jagged path
            const midX = (cx + endX) / 2 + (Math.random() - 0.5) * 20;
            const midY = (cy + endY) / 2 + (Math.random() - 0.5) * 20;

            path += ` Q ${midX} ${midY} ${endX} ${endY}`;

            // Branch sometimes
            if (Math.random() > 0.5) {
                const branchAngle = angle + (Math.random() - 0.5) * Math.PI / 2;
                const branchLength = 10 + Math.random() * 20;
                const branchX = endX + Math.cos(branchAngle) * branchLength;
                const branchY = endY + Math.sin(branchAngle) * branchLength;
                path += ` M ${endX} ${endY} L ${branchX} ${branchY}`;
            }
        }

        // Create crack line
        const crackLine = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        crackLine.setAttribute('d', path);
        crackLine.classList.add('crack-line');
        cracksGroup.appendChild(crackLine);

        // Glow line
        const glowLine = crackLine.cloneNode();
        glowLine.classList.add('crack-line--glow');
        cracksGroup.insertBefore(glowLine, crackLine);

        // Animate
        setTimeout(() => {
            crackLine.style.strokeDashoffset = '0';
            glowLine.style.strokeDashoffset = '0';
        }, 10);
    }

    // ==========================================
    // PARTICLES
    // ==========================================

    function triggerClickParticles(x, y) {
        const container = document.querySelector('.crack-particles');
        if (!container) return;

        for (let i = 0; i < 8; i++) {
            const particle = document.createElement('div');
            particle.classList.add('crack-particle');

            // Random position around click
            const angle = (i / 8) * Math.PI * 2;
            const distance = 10 + Math.random() * 30;

            particle.style.left = `${x + Math.cos(angle) * distance}px`;
            particle.style.top = `${y + Math.sin(angle) * distance}px`;

            // Random color
            const colors = ['#ffd700', '#ffb347', '#8b5cf6'];
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];

            container.appendChild(particle);

            // Animate
            setTimeout(() => particle.classList.add('active'), 10);

            // Remove after animation
            setTimeout(() => particle.remove(), 3000);
        }
    }

    function triggerCrackParticles() {
        const container = document.querySelector('.crack-particles');
        if (!container) return;

        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.classList.add('crack-particle');

                particle.style.left = `${Math.random() * window.innerWidth}px`;
                particle.style.top = `${window.innerHeight}px`;

                container.appendChild(particle);
                setTimeout(() => particle.classList.add('active'), 10);
                setTimeout(() => particle.remove(), 3000);
            }, i * 100);
        }
    }

    // ==========================================
    // SCROLL ANIMATIONS
    // ==========================================

    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observe all animated elements
        const animatedElements = document.querySelectorAll('.fade-in, .crack-in, .scroll-scale, .scroll-rotate, .text-reveal');
        animatedElements.forEach(el => observer.observe(el));
    }

    // ==========================================
    // CURSOR EFFECT
    // ==========================================

    function initCursorEffect() {
        const cursor = document.createElement('div');
        cursor.classList.add('cursor-glow-dot');
        document.body.appendChild(cursor);

        let cursorVisible = false;

        document.addEventListener('mousemove', (e) => {
            state.mouseX = e.clientX;
            state.mouseY = e.clientY;

            cursor.style.left = `${e.clientX}px`;
            cursor.style.top = `${e.clientY}px`;

            if (!cursorVisible) {
                cursor.style.opacity = '1';
                cursorVisible = true;
            }
        });

        document.addEventListener('mouseleave', () => {
            cursor.style.opacity = '0';
            cursorVisible = false;
        });

        // Hide on mobile
        if ('ontouchstart' in window) {
            cursor.style.display = 'none';
        }
    }

    // ==========================================
    // PARALLAX
    // ==========================================

    function initParallax() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');

        function updateParallax() {
            const scrollY = window.scrollY;

            parallaxElements.forEach(el => {
                const speed = parseFloat(el.dataset.parallax) || 0.5;
                const offset = scrollY * speed;
                el.style.transform = `translateY(${offset}px)`;
            });
        }

        window.addEventListener('scroll', updateParallax, { passive: true });
    }

    // ==========================================
    // TOC SMOOTH SCROLL
    // ==========================================

    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ==========================================
    // RAZ PHRASE HIGHLIGHT
    // ==========================================

    function initRazPhraseHighlight() {
        const razPhrases = document.querySelectorAll('.raz-phrase');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');

                    // Pulse effect
                    entry.target.style.animation = 'none';
                    setTimeout(() => {
                        entry.target.style.animation = '';
                    }, 10);
                }
            });
        }, { threshold: 0.5 });

        razPhrases.forEach(phrase => observer.observe(phrase));
    }

    // ==========================================
    // KEYBOARD NAVIGATION
    // ==========================================

    function initKeyboardNav() {
        document.addEventListener('keydown', (e) => {
            // Arrow keys for chapter navigation
            if (e.key === 'ArrowRight') {
                const nextLink = document.querySelector('.nav-link--next');
                if (nextLink) nextLink.click();
            }
            if (e.key === 'ArrowLeft') {
                const prevLink = document.querySelector('.nav-link--prev');
                if (prevLink) prevLink.click();
            }

            // Home key to go to TOC
            if (e.key === 'Home') {
                window.location.href = 'index.html';
            }
        });
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        // Scroll progress
        window.addEventListener('scroll', updateScrollProgress, { passive: true });
        updateScrollProgress();

        // Interactive egg
        initEgg();

        // Scroll animations
        initScrollAnimations();

        // Cursor effect (desktop only)
        if (window.innerWidth > 768) {
            initCursorEffect();
        }

        // Parallax
        initParallax();

        // Smooth scroll
        initSmoothScroll();

        // RAZ phrase effects
        initRazPhraseHighlight();

        // Keyboard navigation
        initKeyboardNav();

        // Remove loading state
        document.body.classList.add('loaded');
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
