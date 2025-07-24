// Mobile-optimized package card animations and interactions
document.addEventListener('DOMContentLoaded', () => {
  // Enhanced fade-in animation for package cards
  const cards = document.querySelectorAll('.package-card');
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add('fade-in');
    }, index * 150); // Faster stagger for mobile
  });

  // Mobile-specific optimizations
  if (window.innerWidth <= 768) {
    // Reduce animation delays on mobile
    const animatedElements = document.querySelectorAll('.animate-float');
    animatedElements.forEach(el => {
      el.style.animationDuration = '8s';
    });
  }

  // Touch feedback for interactive elements
  const touchElements = document.querySelectorAll('.touch-manipulation');
  touchElements.forEach(element => {
    element.addEventListener('touchstart', function() {
      this.style.transform = 'scale(0.95)';
      this.style.transition = 'transform 0.1s ease';
    });
    
    element.addEventListener('touchend', function() {
      this.style.transform = '';
      this.style.transition = '';
    });
  });

  // Improved mobile navigation handling
  const mobileMenuButton = document.querySelector('[x-data] button[\\@click]');
  if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', function() {
      // Add haptic feedback simulation
      if (navigator.vibrate) {
        navigator.vibrate(50);
      }
    });
  }
});


// Event Listeners
document.addEventListener("click", function (event) {
  // Check if the clicked element is the add-to-cart button
  if (event.target.matches(".add-to-cart")) {
      let packagePk = event.target.getAttribute("data-package-pk"); 

      if (packagePk) {
          addToCart(packagePk);
      } else {
          console.error("Package ID not found");
      }
  }
});





function showNotification() {
  const notification = document.getElementById("notification");
  notification.style.display = "block";  // Ensure it's visible
  notification.classList.remove("opacity-0");
  notification.classList.add("opacity-100");
  notification.innerText = "✅ Package added to cart!";

  setTimeout(() => {
      notification.classList.remove("opacity-100");
      notification.classList.add("opacity-0");

      setTimeout(() => {
      notification.style.display = "none"; // Hide it after fade-out
      }, 500);
  }, 3000);
}

function getCSRFToken(){
  const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
  if (!csrfElement) {
    console.error('CSRF token not found. Make sure you have {% csrf_token %} in your template.');
    return null;
  }
  return csrfElement.value;
}



async function addToCart(package_pk) {
  console.log("called");
  try {
      const csrfToken = getCSRFToken();
      if (!csrfToken) {
          console.error("Cannot add to cart: CSRF token not available");
          return;
      }

      const response = await fetch(`${window.location.origin}/cart/add/${package_pk}`, {
          method: "POST",
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': csrfToken,
          }
      });

    if (!response.ok){
      throw new Error(`Status: ${response.status}`)
    }

    const data = await response.json();

    if (data.success) {
      showNotification();
    } else if (data.redirect) {
      window.location.href = data.redirect;
    } else {
      console.error("Error:", data.detail);
    }
    
  } catch (error) {
    console.error("Network error:", error);
  }
}

