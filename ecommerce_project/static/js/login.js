document.addEventListener("DOMContentLoaded", () => {
  const logoutButton = document.getElementById("logoutButton");
  let sessionTimeout;
  const TOKEN_EXPIRATION_BUFFER = 1 * 60 * 1000; // 5 minutes buffer before token expiration

  // Function to retrieve CSRF token from cookies
  function getCSRFToken() {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
      console.log(cookieValue);
    return cookieValue;
  }

  // Dynamically construct the Django URL based on action (e.g., 'logout' or 'refresh_token')
  function getEndpointUrl(action) {
    const baseUrl = "http://127.0.0.1:8001"; // Django base URL
    const endpointMappings = {
      logout: "/users/logout/", // Full URL for logout
      refresh_token: "/users/refresh_token/", // Full URL for refresh token
    };
    return `${baseUrl}${endpointMappings[action] || ""}`;
  }

  // Function to refresh the session
  async function refreshSession() {
    try {
      const csrfToken = getCSRFToken(); // Retrieve the CSRF token
      const response = await fetch(getEndpointUrl("refresh_token"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken, // Add CSRF token in the header
        },
        credentials: "same-origin", // Send session cookies (sessionid, csrftoken) with the request
      });

      if (!response.ok) {
        console.error("Session refresh failed.");
      } else {
        console.log("Session refreshed successfully.");
      }
    } catch (error) {
      console.error("Error refreshing session:", error);
    }
  }

  // Function to log out the user
  async function logout() {
    try {
      const csrfToken = getCSRFToken(); // Retrieve the CSRF token
      const response = await fetch(getEndpointUrl("logout"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken, // Include CSRF token in the header
        },
        credentials: "same-origin", // Ensure cookies (sessionid and csrftoken) are sent with the request
      });

      // Check if the response was a redirect
      if (response.redirected) {
        window.location.href = response.url; // Redirect to the new URL (login page)
      } else if (response.ok) {
        alert("Logout successful");
        window.location.href = "/login/"; // Fallback if no redirect occurs
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Logout error:", error);
      alert("Failed to log out.");
    }
  }

  // Reset session timeout on user interaction
  function resetSessionTimeout() {
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(async () => {
      await refreshSession();
    }, TOKEN_EXPIRATION_BUFFER);
  }

  // Attach event listeners to detect user activity
  ["mousemove", "keydown", "click"].forEach((event) => {
    document.addEventListener(event, resetSessionTimeout);
  });

  // Logout button handler
  logoutButton.addEventListener("click", logout);

  // Start session timeout countdown
  resetSessionTimeout();
});
