function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  async function updateQuantity(cartItemId, change) {
    try {
      const response = await fetch(`${window.location.origin}/cartitem/update/${cartItemId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCSRFToken(),
        },
        body: `change=${change}`
        })

        if (!response.ok){
          throw new Error(`Status: ${response.status}`)
        }

        const data = await response.json();

        if (data.success) {
          document.getElementById(`quantity-${cartItemId}`).innerText = data.new_quantity;
          document.getElementById(`price-${cartItemId}`).innerText = `₦${data.new_price}`;
          document.getElementById("cart-subtotal").innerText = `₦${data.new_subtotal}`;
          document.getElementById("cart-total_price").innerText = `₦${data.new_total_price}`;
        }
      
    } catch (error) {
      console.error(`Network Error: ${error}`)
    }


  }
  function removeItem(cartItemId) {
    fetch(`${window.location.origin}/cart/remove/${cartItemId}`, {
      method: 'POST',
      headers: {
        "Content-Type": 'application/x-www-form-urlencoded',
        "X-CSRFToken": getCSRFToken(),
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        document.getElementById(`cart-item-${cartItemId}`).remove();
        document.getElementById('emptycart').classList.remove('hidden')
      }
    })
    .catch(error => console.error('Error:', error));
  }
