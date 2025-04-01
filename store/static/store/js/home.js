// Initialize carousel functionality
document.addEventListener('DOMContentLoaded', () => {
    const carouselImages = document.getElementById('carousel-images');
    const totalImages = carouselImages.children.length;
    let index = 0;

    // Function to update carousel position
    const updateCarousel = () => {
        carouselImages.style.transform = `translateX(-${index * 100}%)`;
    };

    // Handle "previous" button click
    const prevButton = document.getElementById('prev');
    prevButton.addEventListener('click', () => {
        index = (index - 1 + totalImages) % totalImages; // Circular navigation
        updateCarousel();
    });

    // Handle "next" button click
    const nextButton = document.getElementById('next');
    nextButton.addEventListener('click', () => {
        index = (index + 1) % totalImages; // Circular navigation
        updateCarousel();
    });
});