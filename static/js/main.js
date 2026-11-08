/**
 * ==============================================================================
 * FILE: static/js/main.js
 * ==============================================================================
 * PURPOSE:
 * Provides all client-side interactivity, canvas particle rendering,
 * typing effects, scroll observations, and asynchronous form submission
 * for Druva Teja's portfolio.
 *
 * RESPONSIBILITIES:
 * 1. Render an elegant, non-distracting HTML5 Canvas particle background.
 * 2. Execute a smooth typewriter effect rotating through Druva's roles.
 * 3. Handle responsive navigation (sticky glass header, active spy, mobile drawer).
 * 4. Apply smooth reveal transitions as elements scroll into the viewport.
 * 5. Handle AJAX submission of the contact form to the FastAPI backend (POST /contact).
 *
 * CONNECTED FILES:
 * - templates/index.html: Loads this script right before the closing </body> tag.
 * - static/css/style.css: Works with CSS classes like '.scrolled', '.active', '.revealed'.
 * - routes.py: Receives the JSON payload sent by 'initContactForm'.
 *
 * BEGINNER EXPLANATION:
 * When a visitor loads the website, their browser executes this file.
 * Vanilla JavaScript means we write pure, standard JavaScript without any
 * bulky third-party libraries like jQuery or React. It keeps the site ultra-fast,
 * lightweight, and easy to inspect and understand.
 * ==============================================================================
 */

// Wrap all logic in DOMContentLoaded to ensure the HTML DOM is fully parsed
document.addEventListener("DOMContentLoaded", () => {
  "use strict";

  // Initialize all interactive modules
  initParticleCanvas();
  initTypingEffect();
  initNavigation();
  initMobileMenu();
  initScrollReveal();
  initContactForm();
  initBackToTop();
});

/* -----------------------------------------------------------------------------
   01. CANVAS PARTICLE BACKGROUND
   ----------------------------------------------------------------------------- */
/**
 * Why it exists:
 *   Creates a sophisticated, subtle ambient particle network that gives the dark
 *   background depth—reminiscent of Linear and Stripe—without overwhelming the content.
 *
 * What it does:
 *   1. Targets the <canvas id="particle-canvas"> element.
 *   2. Generates an array of floating node particles with random velocities.
 *   3. Connects nearby nodes with delicate glowing lines based on distance.
 *   4. Automatically adapts to window resize events.
 *
 * Inputs:
 *   None (reads window dimensions and canvas context).
 *
 * Outputs:
 *   Continuous 60 FPS animation loop drawn on the canvas.
 */
function initParticleCanvas() {
  const canvas = document.getElementById("particle-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  // Resize handler with debouncing
  window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  // Calculate particle count based on screen width (fewer on mobile for performance)
  const particleCount = width < 768 ? 30 : 65;
  const maxDistance = width < 768 ? 90 : 130;
  const particles = [];

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      // Gentle, calm velocity
      this.vx = (Math.random() - 0.5) * 0.45;
      this.vy = (Math.random() - 0.5) * 0.45;
      this.radius = Math.random() * 1.5 + 0.8;
      // Alternate subtle blue and purple accents
      this.color = Math.random() > 0.4 ? "rgba(79, 140, 255, " : "rgba(139, 92, 246, ";
      this.alpha = Math.random() * 0.4 + 0.2;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      // Wrap around edges seamlessly
      if (this.x < 0) this.x = width;
      if (this.x > width) this.x = 0;
      if (this.y < 0) this.y = height;
      if (this.y > height) this.y = 0;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color + this.alpha + ")";
      ctx.fill();
    }
  }

  // Populate particles
  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  // Animation frame loop
  function render() {
    ctx.clearRect(0, 0, width, height);

    // Draw connecting lines between close particles
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDistance) {
          const lineAlpha = (1 - dist / maxDistance) * 0.14;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(79, 140, 255, ${lineAlpha})`;
          ctx.lineWidth = 0.75;
          ctx.stroke();
        }
      }
    }

    // Update and draw each particle
    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw();
    }

    requestAnimationFrame(render);
  }

  render();
}

/* -----------------------------------------------------------------------------
   02. TYPEWRITER EFFECT FOR HERO ROLES
   ----------------------------------------------------------------------------- */
/**
 * Why it exists:
 *   Demonstrates Druva's multifaceted identity (Full Stack, Python, AI, Hackathons)
 *   in an engaging, clean manner without taking up multiple lines of screen space.
 *
 * What it does:
 *   1. Reads role phrases from the 'data-roles' attribute on the typing element.
 *   2. Cycles character-by-character: typing -> pausing -> deleting -> next role.
 *
 * Inputs:
 *   DOM Element: <span id="typing-text" data-roles='[...]'>
 *
 * Outputs:
 *   Animated text updates with realistic human typing delays.
 */
function initTypingEffect() {
  const typingElement = document.getElementById("typing-text");
  if (!typingElement) return;

  // Retrieve roles from data-attribute or fallback to defaults
  let roles = [];
  try {
    const rawRoles = typingElement.getAttribute("data-roles");
    roles = rawRoles ? JSON.parse(rawRoles) : [];
  } catch (err) {
    console.error("Could not parse data-roles:", err);
  }

  if (roles.length === 0) {
    roles = [
      "Full Stack Developer",
      "Python Engineer",
      "AI Enthusiast",
      "Hackathon Builder",
      "Problem Solver"
    ];
  }

  let roleIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  const typeSpeed = 75;       // Typing speed per character (ms)
  const deleteSpeed = 40;     // Deleting speed per character (ms)
  const pauseAfterComplete = 2000; // Pause when word is finished (ms)
  const pauseBeforeNext = 400;     // Pause before typing next word (ms)

  function tick() {
    const currentRole = roles[roleIndex];

    if (isDeleting) {
      charIndex--;
      typingElement.textContent = currentRole.substring(0, charIndex);
    } else {
      charIndex++;
      typingElement.textContent = currentRole.substring(0, charIndex);
    }

    let nextDelay = isDeleting ? deleteSpeed : typeSpeed;

    // Word completed typing
    if (!isDeleting && charIndex === currentRole.length) {
      nextDelay = pauseAfterComplete;
      isDeleting = true;
    }
    // Word fully deleted
    else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      nextDelay = pauseBeforeNext;
    }

    setTimeout(tick, nextDelay);
  }

  // Start the typewriter loop
  setTimeout(tick, 500);
}

/* -----------------------------------------------------------------------------
   03. NAVIGATION & ACTIVE SECTION SPY
   ----------------------------------------------------------------------------- */
/**
 * Why it exists:
 *   1. Applies glassmorphism background to the header once the user scrolls down.
 *   2. Highlights whichever navigation link corresponds to the section currently
 *      visible on screen.
 *
 * What it does:
 *   Listens to window scroll events and computes section offsets relative to scroll position.
 *
 * Inputs:
 *   DOM Elements: .site-header, .nav-link, section[id]
 *
 * Outputs:
 *   Toggles '.scrolled' on header, toggles '.active' on matching nav link.
 */
function initNavigation() {
  const header = document.querySelector(".site-header");
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll("section[id]");

  function handleScroll() {
    const scrollY = window.pageYOffset;

    // Toggle header glass backdrop
    if (scrollY > 40) {
      header?.classList.add("scrolled");
    } else {
      header?.classList.remove("scrolled");
    }

    // Determine current active section
    let currentSectionId = "";
    sections.forEach((section) => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        currentSectionId = section.getAttribute("id");
      }
    });

    // Update active nav link
    navLinks.forEach((link) => {
      link.classList.remove("active");
      const href = link.getAttribute("href");
      if (href === `#${currentSectionId}`) {
        link.classList.add("active");
      }
    });
  }

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll(); // Initial check on load
}

/* -----------------------------------------------------------------------------
   04. MOBILE DRAWER MENU
   ----------------------------------------------------------------------------- */
/**
 * Why it exists:
 *   Provides a smooth, accessible navigation drawer for mobile and tablet screens.
 *
 * What it does:
 *   Toggles the navigation link list visibility and animates the hamburger icon.
 *   Closes drawer automatically whenever a link is tapped.
 *
 * Inputs:
 *   #mobile-toggle, #nav-links
 *
 * Outputs:
 *   Toggles '.open' class on menu button and navigation list.
 */
function initMobileMenu() {
  const toggleBtn = document.getElementById("mobile-toggle");
  const navLinksList = document.getElementById("nav-links");

  if (!toggleBtn || !navLinksList) return;

  function toggleMenu() {
    const isOpen = toggleBtn.classList.toggle("open");
    navLinksList.classList.toggle("open");
    toggleBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }

  toggleBtn.addEventListener("click", toggleMenu);

  // Close mobile drawer when any link is tapped
  const links = navLinksList.querySelectorAll("a");
  links.forEach((link) => {
    link.addEventListener("click", () => {
      if (navLinksList.classList.contains("open")) {
        toggleMenu();
      }
    });
  });
}

/* -----------------------------------------------------------------------------
   05. SCROLL REVEAL ANIMATIONS (IntersectionObserver)
   ----------------------------------------------------------------------------- */
/**
 * Why it exists:
 *   Gives the website that sleek Apple / Linear feel where sections gracefully
 *   fade and slide into place as the user scrolls down the page.
 *
 * What it does:
 *   Uses native IntersectionObserver API to watch elements with class '.reveal'
 *   and adds '.revealed' when they enter the viewport.
 *
 * Inputs:
 *   DOM Elements matching '.reveal'
 *
 * Outputs:
 *   Applies CSS classes that trigger GPU-accelerated opacity and transform transitions.
 */
function initScrollReveal() {
  const revealElements = document.querySelectorAll(".reveal");
  if (revealElements.length === 0) return;

  // Fallback for older browsers without IntersectionObserver
  if (!("IntersectionObserver" in window)) {
    revealElements.forEach((el) => el.classList.add("revealed"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          // Stop observing once revealed to save CPU cycles
          obs.unobserve(entry.target);
        }
      });
    },
    {
      root: null,
      threshold: 0.12, // Reveal when 12% of element is visible
      rootMargin: "0px 0px -40px 0px"
    }
  );

  revealElements.forEach((el) => observer.observe(el));
}

/* -----------------------------------------------------------------------------
   06. ASYNCHRONOUS CONTACT FORM SUBMISSION (FastAPI POST /contact)
   ----------------------------------------------------------------------------- */
/**
 * Why it exists:
 *   Allows users to send messages to Druva without triggering an annoying full-page
 *   reload. Communicates directly with the FastAPI backend endpoint.
 *
 * What it does:
 *   1. Intercepts the form's 'submit' event.
 *   2. Extracts and sanitizes input values (name, email, subject, message).
 *   3. Displays a loading spinner on the submit button.
 *   4. Sends a JSON POST request to '/contact'.
 *   5. Parses the response and displays an elegant success or error banner.
 *   6. Clears form fields upon successful submission.
 *
 * Inputs:
 *   HTML Form: #contact-form
 *
 * Outputs:
 *   Network request to POST /contact and live UI feedback container updates.
 */
function initContactForm() {
  const form = document.getElementById("contact-form");
  const feedback = document.getElementById("form-feedback");
  const submitBtn = document.getElementById("contact-submit-btn");

  if (!form || !feedback || !submitBtn) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default page refresh

    // Reset feedback state
    feedback.className = "form-feedback";
    feedback.style.display = "none";
    feedback.textContent = "";

    // Extract values
    const nameInput = document.getElementById("contact-name");
    const emailInput = document.getElementById("contact-email");
    const subjectInput = document.getElementById("contact-subject");
    const messageInput = document.getElementById("contact-message");

    const payload = {
      name: nameInput.value.trim(),
      email: emailInput.value.trim(),
      subject: subjectInput.value.trim(),
      message: messageInput.value.trim()
    };

    // Simple client-side sanity check
    if (!payload.name || !payload.email || !payload.subject || !payload.message) {
      showFeedback("Please fill out all fields before submitting.", "error");
      return;
    }

    // Set loading button state
    submitBtn.classList.add("loading");
    submitBtn.disabled = true;

    try {
      // Send async POST request to FastAPI backend
      const response = await fetch("/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showFeedback(data.message || "Message sent successfully!", "success");
        form.reset(); // Clear all input fields
      } else {
        // Handle validation errors from FastAPI/Pydantic
        const errorMsg = data.detail
          ? (Array.isArray(data.detail) ? data.detail[0].msg : data.detail)
          : "Could not send message. Please try again or email directly.";
        showFeedback(errorMsg, "error");
      }
    } catch (networkError) {
      console.error("Contact Form Network Error:", networkError);
      showFeedback(
        "Network error. Please check your connection or email druvateja08@gmail.com directly.",
        "error"
      );
    } finally {
      // Restore submit button state
      submitBtn.classList.remove("loading");
      submitBtn.disabled = false;
    }
  });

  /**
   * Helper function to display styled banner message
   */
  function showFeedback(text, type) {
    feedback.textContent = text;
    feedback.className = `form-feedback ${type}`;
    feedback.style.display = "block";

    // Scroll slightly so the user clearly sees the confirmation
    feedback.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

/* -----------------------------------------------------------------------------
   07. BACK TO TOP BUTTON
   ----------------------------------------------------------------------------- */
/**
 * Why it exists:
 *   Provides a quick one-click return to the top of the page from the footer.
 *
 * What it does:
 *   Smoothly scrolls the window to coordinates (0, 0).
 */
function initBackToTop() {
  const backToTopBtn = document.getElementById("back-to-top-btn");
  if (!backToTopBtn) return;

  backToTopBtn.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
}

