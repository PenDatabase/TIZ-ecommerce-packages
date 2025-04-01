document.addEventListener('DOMContentLoaded', () => {
    const starButton = document.getElementById('star-package');
    starButton.addEventListener('click', () => {
      if (starButton.classList.contains('bg-blue-600')) {
        starButton.classList.remove('bg-blue-600', 'text-white');
        starButton.classList.add('border-blue-600', 'text-blue-600');
        starButton.innerHTML = '<i class="fas fa-star"></i> Star Package';
      } else {
        starButton.classList.add('bg-blue-600', 'text-white');
        starButton.classList.remove('border-blue-600', 'text-blue-600');
        starButton.innerHTML = '<i class="fas fa-star"></i> Starred';
      }
    });
  });