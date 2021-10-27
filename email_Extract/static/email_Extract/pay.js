let test = document.getElementById("test")
test.innerHTML = "BYEBYE"
let stripe;

//fetch the keys from stripe view url
fetch("../config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  console.log(data)
  stripe = Stripe(data.publicKey);
});

let pay_btn = document.getElementById("submitBtn")
pay_btn.addEventListener("click",() => {
    fetch("../create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });