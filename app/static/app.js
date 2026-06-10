(function () {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function highlightSql(sql) {
    return escapeHtml(sql)
      .replace(/\b(SELECT|FROM|WHERE|AND)\b/g, '<span class="sql-keyword">$1</span>')
      .replace(/&#39;/g, '<span class="sql-quote">&#39;</span>')
      .replace(/--/g, '<span class="sql-comment">--</span>');
  }

  function buildLoginSql() {
    const username = document.querySelector('[data-sqli-username]');
    const password = document.querySelector('[data-sqli-password]');
    const preview = document.querySelector('[data-sqli-preview]');
    if (!username || !password || !preview) return;

    const render = () => {
      const sql = `SELECT * FROM users WHERE username = '${username.value}' AND password = '${password.value}'`;
      preview.innerHTML = highlightSql(sql);
    };

    username.addEventListener("input", render);
    password.addEventListener("input", render);
    render();
  }

  function setupPageTransitions() {
    document.body.classList.add("loaded");
    if (prefersReducedMotion) return;

    document.querySelectorAll('a[href^="/"], a[href^="' + window.location.origin + '"]').forEach((link) => {
      link.addEventListener("click", (event) => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        if (link.target && link.target !== "_self") return;
        event.preventDefault();
        document.body.classList.add("page-out");
        window.setTimeout(() => {
          window.location.href = link.href;
        }, 170);
      });
    });
  }

  function setupThemeToggle() {
    const toggle = document.querySelector("[data-theme-toggle]");
    const label = document.querySelector("[data-theme-label]");
    if (!toggle || !label) return;

    const sync = () => {
      const activeTheme = document.documentElement.dataset.theme === "light" ? "light" : "dark";
      label.textContent = activeTheme === "light" ? "Dark mode" : "Light mode";
      toggle.setAttribute("aria-pressed", String(activeTheme === "light"));
    };

    toggle.addEventListener("click", () => {
      const nextTheme = document.documentElement.dataset.theme === "light" ? "dark" : "light";
      if (nextTheme === "dark") {
        delete document.documentElement.dataset.theme;
      } else {
        document.documentElement.dataset.theme = nextTheme;
      }
      try {
        if (nextTheme === "dark") {
          localStorage.removeItem("lab-theme");
        } else {
          localStorage.setItem("lab-theme", nextTheme);
        }
      } catch (error) {}
      sync();
    });

    sync();
  }

  function setupTiltCards() {
    if (prefersReducedMotion) return;
    document.querySelectorAll("[data-tilt-card]").forEach((card) => {
      card.addEventListener("mousemove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `translateY(-7px) rotateX(${(-y * 5).toFixed(2)}deg) rotateY(${(x * 7).toFixed(2)}deg)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  }

  function setupSubmittingForms() {
    document.querySelectorAll("form").forEach((form) => {
      form.addEventListener("submit", () => {
        form.classList.add("is-submitting");
        const button = form.querySelector('button[type="submit"]');
        if (button) {
          button.dataset.originalText = button.textContent;
          button.textContent = form.dataset.safeFlow === "true" ? "Checking..." : "Executing...";
        }
      });
    });
  }

  function setupTypewriter() {
    if (prefersReducedMotion) return;
    document.querySelectorAll("[data-typewriter]").forEach((node) => {
      const text = node.textContent.trim();
      if (!text) return;
      node.textContent = "";
      let index = 0;
      const tick = () => {
        node.textContent = text.slice(0, index);
        index += 1;
        if (index <= text.length) window.setTimeout(tick, 22);
      };
      tick();
    });
  }

  function fireConfetti() {
    if (prefersReducedMotion) return;
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const colors = ["#54f0a7", "#65d8ff", "#a78bfa", "#ffd166"];
    const particles = Array.from({ length: 90 }, () => ({
      x: window.innerWidth / 2,
      y: window.innerHeight * 0.22,
      vx: (Math.random() - 0.5) * 9,
      vy: Math.random() * -7 - 2,
      gravity: 0.18 + Math.random() * 0.08,
      size: 4 + Math.random() * 5,
      rotation: Math.random() * Math.PI,
      color: colors[Math.floor(Math.random() * colors.length)],
      life: 90 + Math.random() * 30,
    }));

    canvas.className = "confetti-canvas";
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    document.body.appendChild(canvas);

    const animate = () => {
      context.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach((particle) => {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.vy += particle.gravity;
        particle.rotation += 0.16;
        particle.life -= 1;
        context.save();
        context.translate(particle.x, particle.y);
        context.rotate(particle.rotation);
        context.fillStyle = particle.color;
        context.fillRect(-particle.size / 2, -particle.size / 2, particle.size, particle.size * 0.55);
        context.restore();
      });

      if (particles.some((particle) => particle.life > 0 && particle.y < canvas.height + 30)) {
        requestAnimationFrame(animate);
      } else {
        canvas.remove();
      }
    };

    animate();
  }

  function setupResultStates() {
    const panel = document.querySelector(".demo-panel");
    const dangerResult = document.querySelector(".result.danger[data-result]");
    const safeResult = document.querySelector(".result.safe[data-result], .result.safe[data-prepared]");

    if (panel && dangerResult) panel.classList.add("hacked");
    if (safeResult) safeResult.classList.add("is-confirmed");
    if (document.querySelector("[data-confetti='true']")) {
      window.setTimeout(fireConfetti, 260);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    setupPageTransitions();
    setupThemeToggle();
    setupTiltCards();
    setupSubmittingForms();
    setupTypewriter();
    setupResultStates();
    buildLoginSql();
  });
})();
