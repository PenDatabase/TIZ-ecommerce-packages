// Add fade-in animation to package cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.package-card');
    cards.forEach((card, index) => {
      setTimeout(() => {
        card.classList.add('fade-in');
      }, index * 200);
    });
  });


// Event Listeners
document.addEventListener("click", function (event) {
  // Check if the clicked element is the add-to-cart button
  if (event.target.matches("#add-to-cart")) {
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
  return document.querySelector('[name=csrfmiddlewaretoken]').value
}



async function addToCart(package_pk) {
  console.log("called");
  try {
      const response = await fetch(`${window.location.origin}/cart/add/${package_pk}`, {
          method: "POST",
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': getCSRFToken(),
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

