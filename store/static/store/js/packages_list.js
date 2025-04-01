function searchPackages() {
    const searchInput = document.getElementById('search-bar').value.toLowerCase();
    const packageCards = document.querySelectorAll('.package-card');
    let anyVisible = false;

    packageCards.forEach(card => {
      const packageName = card.querySelector('h3').textContent.toLowerCase();

      if (packageName.includes(searchInput)) {
        card.style.display = 'block';
        anyVisible = true;
      } else {
        card.style.display = 'none';
      }
    });

    // Show/hide the "Press Enter for more results" message
    const enterMessage = document.getElementById('enter-message');
    enterMessage.style.display = anyVisible ? 'none' : 'flex';
    enterMessage.classList.toggle('fade-in', !anyVisible);
  }