document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.nav');
    const header = document.querySelector('.header');

    if (mobileMenuBtn && nav) {
        const toggleNav = () => nav.classList.toggle('active');

        mobileMenuBtn.addEventListener('click', toggleNav);
        mobileMenuBtn.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') toggleNav();
        });

        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => nav.classList.remove('active'));
        });
    }

    window.addEventListener('scroll', () => {
        if (!header) return;
        if (window.scrollY > 80) {
            header.classList.add('header--scrolled');
        } else {
            header.classList.remove('header--scrolled');
        }
    });

    const urlParams = new URLSearchParams(window.location.search);
    const productParam = urlParams.get('product');

    if (urlParams.has('success')) {
        alert('Thank you for your enquiry! We will get back to you shortly.');
    } else if (urlParams.has('error')) {
        alert('Sorry, something went wrong. Please try again or call us on 07532 721 934.');
    }

    const quoteSelect = document.querySelector('#quote-product');
    if (quoteSelect && productParam) {
        const match = Array.from(quoteSelect.options).find(
            opt => opt.value.toLowerCase() === productParam.toLowerCase()
        );
        if (match) {
            quoteSelect.value = match.value;
        }
    }

    const filterButtons = document.querySelectorAll('.filter-btn');
    const productSections = document.querySelectorAll('.product-types');

    const activateProductSection = (target) => {
        let hasMatch = false;
        filterButtons.forEach(btn => {
            const isMatch = btn.dataset.productTarget === target;
            btn.classList.toggle('active', isMatch);
            if (isMatch) hasMatch = true;
        });
        productSections.forEach(section => {
            section.classList.toggle('active', section.dataset.productSection === target);
        });
        if (!hasMatch && filterButtons.length) {
            const fallback = filterButtons[0].dataset.productTarget;
            activateProductSection(fallback);
        }
    };

    if (filterButtons.length) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => activateProductSection(button.dataset.productTarget));
        });

        const normalizedParam = productParam ? productParam.toLowerCase() : null;
        const validTargets = ['windows', 'doors', 'rooflights', 'conservatories'];
        if (normalizedParam && validTargets.includes(normalizedParam)) {
            activateProductSection(normalizedParam);
            // Scroll to anchor if present in URL
            setTimeout(() => {
                const hash = window.location.hash;
                if (hash) {
                    const targetElement = document.querySelector(hash);
                    if (targetElement) {
                        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            }, 100);
        } else {
            activateProductSection(filterButtons[0].dataset.productTarget);
        }
    }

    // Handle anchor links on products page
    if (window.location.hash) {
        const hash = window.location.hash.substring(1);
        const validTargets = ['windows', 'doors', 'rooflights', 'conservatories'];
        if (validTargets.includes(hash)) {
            setTimeout(() => {
                const targetElement = document.querySelector(`#${hash}`);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 300);
        }
    }

    const initSlider = (root, { auto = false, interval = 4000 } = {}) => {
        const slides = root.querySelectorAll('img');
        if (!slides.length) return;

        let current = 0;

        const updateSlides = () => {
            slides.forEach((slide, index) => {
                slide.classList.toggle('active', index === current);
            });
        };

        const goTo = (direction) => {
            current = (current + direction + slides.length) % slides.length;
            updateSlides();
        };

        root.querySelectorAll('[data-slider-control]').forEach(button => {
            button.addEventListener('click', () => {
                const dir = button.dataset.sliderControl === 'next' ? 1 : -1;
                goTo(dir);
            });
        });

        if (auto) {
            setInterval(() => goTo(1), interval);
        }

        updateSlides();
    };

    document.querySelectorAll('.door-preview').forEach(preview => {
        initSlider(preview, { auto: true, interval: 5000 });
    });

    document.querySelectorAll('.door-slider').forEach(slider => {
        initSlider(slider);
    });
});