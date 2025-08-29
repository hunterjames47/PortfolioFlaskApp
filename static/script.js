document.addEventListener("DOMContentLoaded", () => {
  // === Navbar + Theme Toggle ===
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.querySelectorAll('.navbar a');
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const themeIndicator = document.getElementById('themeIndicator');

  hamburger.addEventListener('click', () => {
    document.getElementById('navbar').classList.toggle('open');
  });

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      document.getElementById('navbar').classList.remove('open');
    });
  });

  themeToggle.addEventListener('click', () => {
    const isDark = document.body.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcon(isDark);
    updateIndicatorPosition(isDark);
  });

  const storedTheme = localStorage.getItem('theme');
  const isDark = storedTheme === 'dark';
  if (isDark) document.body.classList.add('dark');
  updateThemeIcon(isDark);
  updateIndicatorPosition(isDark);

  function updateThemeIcon(isDark) {
    themeIcon.classList.toggle('fa-sun', !isDark);
    themeIcon.classList.toggle('fa-moon', isDark);
  }
  function updateIndicatorPosition(isDark) {
    themeIndicator.style.left = isDark ? '28px' : '4px';
  }

  // === Intersection Observer ===
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.fade-section').forEach(section => {
    observer.observe(section);
  });

  // === Modal Setup (Contact + Notes) ===
  function setupModal(openId, modalId, closeId) {
    const openBtn = document.getElementById(openId);
    const modal = document.getElementById(modalId);
    const closeBtn = document.getElementById(closeId);

    if (!openBtn || !modal || !closeBtn) return;

    openBtn.addEventListener("click", e => {
      e.preventDefault();
      modal.style.display = "flex";
    });
    closeBtn.addEventListener("click", () => {
      modal.style.display = "none";
    });
    window.addEventListener("click", e => {
      if (e.target === modal) modal.style.display = "none";
    });
  }
  setupModal("openContact", "contactModal", "closeContact");
  setupModal("openNotes", "notesModal", "closeNotes");

  // === Edit Notes ===
  document.querySelectorAll('.edit-btn').forEach(editBtn => {
    editBtn.addEventListener('click', e => {
      e.preventDefault();
      const noteId = editBtn.dataset.id;
      const noteContent = editBtn.dataset.content;
      const noteNickname = editBtn.dataset.nickname;

      document.getElementById("editNoteContent").value = noteContent;
      document.getElementById("editNoteForm").dataset.noteId = noteId;
      document.getElementById("editNoteNickname").value = ""; // force re-enter nickname
      document.getElementById("editModal").style.display = "flex";
    });
  });

  // === Edit Note Form Submit ===
  document.getElementById("editNoteForm").addEventListener("submit", e => {
    e.preventDefault();
    const noteId = e.target.dataset.noteId;
    const newContent = document.getElementById("editNoteContent").value;
    const nickname = document.getElementById("editNoteNickname").value;

    if (!nickname) {
      alert("You must enter your nickname to edit this note.");
      return;
    }

    fetch(`/edit/${noteId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
      },
      body: new URLSearchParams({
        content: newContent,
        nickname: nickname
      })
    })
      .then(res => res.json())
      .then(data => {
        if (!data.success) throw new Error("Failed to update note");

        const card = document.querySelector(`.card[data-note-id="${noteId}"]`);
        card.querySelector(".note-content").textContent = data.new_content;
        card.querySelector(".edit-btn").dataset.content = data.new_content;

        document.getElementById("editModal").style.display = "none";
      })
      .catch(err => console.error("Error:", err));
  });

  document.getElementById("closeEdit").addEventListener("click", () => {
    document.getElementById("editModal").style.display = "none";
  });

  // === Delete Form Submit ===
  document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const nickname = prompt("Enter your nickname to delete this note:");
      if (!nickname) return;

      const formData = new FormData(form);
      formData.set("nickname", nickname); // overwrite hidden field

      fetch(form.action, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            form.closest(".card").remove();
          } else {
            alert("Failed to delete note.");
          }
        })
        .catch(err => console.error("Error:", err));
    });
  });
});
