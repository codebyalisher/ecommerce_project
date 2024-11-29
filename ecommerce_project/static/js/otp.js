document.addEventListener("DOMContentLoaded", () => {
  const sendOtpBtn = document.getElementById("send-otp-btn");
  const verifyOtpBtn = document.getElementById("verify-otp-btn");
  const generateOtpForm = document.getElementById("generate-otp-form");
  const verifyOtpForm = document.getElementById("verify-otp-form");
  const emailHiddenInput = document.getElementById("email-hidden");

  // Function to handle OTP generation
  sendOtpBtn.addEventListener("click", async () => {
    const emailInput = document.getElementById("email");
    const email = emailInput.value;

    if (!email) {
      alert("Please enter your email");
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8001/users/generate-otp/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken(),
          },
          body: new URLSearchParams({ email }),
        }
      );

      if (response.ok) {
        alert("OTP sent to your email");
        emailHiddenInput.value = email; // Save email for verification
        generateOtpForm.style.display = "none";
        verifyOtpForm.style.display = "block";
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || errorData.detail}`);
      }
    } catch (error) {
      console.error("Error sending OTP:", error);
    }
  });

  // Function to handle OTP verification
  verifyOtpBtn.addEventListener("click", async () => {
    const otpInput = document.getElementById("otp");
    const otp = otpInput.value;
    const email = emailHiddenInput.value;

    if (!otp) {
      alert("Please enter the OTP");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8001/users/verify-otp/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": getCSRFToken(),
        },
        body: new URLSearchParams({ email, otp }),
      });

      if (response.redirected) {
        console.log(getCSRFToken());
        window.location.href = response.url; // Redirect to the new URL (login page)
      } else if (response.ok) {
        alert("OTP verified successfully");
        window.location.href = "http://127.0.0.1:8001/users/home/"; // Fallback if no redirect occurs
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || errorData.detail}`);
      }
    } catch (error) {
      console.error("Error verifying OTP:", error);
    }
  });

  // CSRF Token Retrieval
  function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    const csrfCookie = cookies.find((cookie) =>
      cookie.startsWith("csrftoken=")
    );
    return csrfCookie ? csrfCookie.split("=")[1] : "";
  }
});
