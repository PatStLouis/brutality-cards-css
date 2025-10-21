// Pokemon Cards - Interactive 3D Hover Effects
// Based on the original Svelte implementation by @simeydotme

document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    
    // Helper functions
    const clamp = (num, min = 0, max = 100) => Math.min(Math.max(num, min), max);
    const round = (num, fix = 2) => parseFloat(num.toFixed(fix));
    const adjust = (value, fromMin, fromMax, toMin, toMax) => {
        return toMin + (((value - fromMin) / (fromMax - fromMin)) * (toMax - toMin));
    };
    
    cards.forEach(card => {
        const rotator = card.querySelector('.card__rotator');
        let interacting = false;
        
        // Generate random seed for cosmos effect
        const randomSeed = {
            x: Math.random(),
            y: Math.random()
        };
        const cosmosPosition = {
            x: Math.floor(randomSeed.x * 734),
            y: Math.floor(randomSeed.y * 1280)
        };
        
        // Set static CSS variables
        card.style.setProperty('--seedx', randomSeed.x);
        card.style.setProperty('--seedy', randomSeed.y);
        card.style.setProperty('--cosmosbg', `${cosmosPosition.x}px ${cosmosPosition.y}px`);
        
        // Initialize dynamic variables
        card.style.setProperty('--pointer-x', '50%');
        card.style.setProperty('--pointer-y', '50%');
        card.style.setProperty('--pointer-from-center', '0');
        card.style.setProperty('--pointer-from-top', '0.5');
        card.style.setProperty('--pointer-from-left', '0.5');
        card.style.setProperty('--card-opacity', '0');
        card.style.setProperty('--rotate-x', '0deg');
        card.style.setProperty('--rotate-y', '0deg');
        card.style.setProperty('--background-x', '50%');
        card.style.setProperty('--background-y', '50%');
        card.style.setProperty('--card-scale', '1');
        card.style.setProperty('--translate-x', '0px');
        card.style.setProperty('--translate-y', '0px');
        
        const interact = (e) => {
            if (!rotator) return;
            
            interacting = true;
            card.classList.add('interacting');
            
            const rect = rotator.getBoundingClientRect();
            const absolute = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top,
            };
            const percent = {
                x: clamp(round((100 / rect.width) * absolute.x)),
                y: clamp(round((100 / rect.height) * absolute.y)),
            };
            const center = {
                x: percent.x - 50,
                y: percent.y - 50,
            };
            
            // Update background position (for holographic effects)
            const backgroundX = adjust(percent.x, 0, 100, 37, 63);
            const backgroundY = adjust(percent.y, 0, 100, 33, 67);
            
            // Update rotation (3D tilt effect)
            const rotateX = round(center.y / 2);
            const rotateY = round(-(center.x / 3.5));
            
            // Update glare position and opacity
            const glareX = round(percent.x);
            const glareY = round(percent.y);
            const glareOpacity = 1;
            
            // Calculate distance from center
            const distanceFromCenter = clamp(
                Math.sqrt(
                    (glareY - 50) * (glareY - 50) + 
                    (glareX - 50) * (glareX - 50)
                ) / 50,
                0,
                1
            );
            
            // Set CSS custom properties
            card.style.setProperty('--pointer-x', `${glareX}%`);
            card.style.setProperty('--pointer-y', `${glareY}%`);
            card.style.setProperty('--pointer-from-center', distanceFromCenter);
            card.style.setProperty('--pointer-from-top', glareY / 100);
            card.style.setProperty('--pointer-from-left', glareX / 100);
            card.style.setProperty('--card-opacity', glareOpacity);
            card.style.setProperty('--rotate-x', `${rotateX}deg`);
            card.style.setProperty('--rotate-y', `${rotateY}deg`);
            card.style.setProperty('--background-x', `${backgroundX}%`);
            card.style.setProperty('--background-y', `${backgroundY}%`);
        };
        
        const interactEnd = () => {
            interacting = false;
            card.classList.remove('interacting');
            
            // Reset to default values
            card.style.setProperty('--pointer-x', '50%');
            card.style.setProperty('--pointer-y', '50%');
            card.style.setProperty('--pointer-from-center', '0');
            card.style.setProperty('--pointer-from-top', '0.5');
            card.style.setProperty('--pointer-from-left', '0.5');
            card.style.setProperty('--card-opacity', '0');
            card.style.setProperty('--rotate-x', '0deg');
            card.style.setProperty('--rotate-y', '0deg');
            card.style.setProperty('--background-x', '50%');
            card.style.setProperty('--background-y', '50%');
        };
        
        let isFlipped = false;
        
        const activate = (e) => {
            e.preventDefault();
            
            // Toggle the flipped state
            if (isFlipped) {
                // Flipping back to front
                card.classList.remove('flipped');
                card.classList.add('flipping-back');
                setTimeout(() => {
                    card.classList.remove('flipping-back');
                }, 1000);
            } else {
                // Flipping forward to back
                card.classList.add('flipping-forward');
                setTimeout(() => {
                    card.classList.remove('flipping-forward');
                    card.classList.add('flipped');
                }, 1000);
            }
            
            isFlipped = !isFlipped;
        };
        
        // Event listeners
        if (rotator) {
            rotator.addEventListener('pointermove', interact);
            rotator.addEventListener('mouseout', interactEnd);
            rotator.addEventListener('click', activate);
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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
});

