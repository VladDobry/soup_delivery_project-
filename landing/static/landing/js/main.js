const revealItems = document.querySelectorAll(".reveal");
const toast = document.querySelector(".toast");
const soupModal = document.querySelector(".soup-modal");
const soupOpeners = document.querySelectorAll("[data-soup-open]");
const soupClosers = document.querySelectorAll("[data-soup-close]");
const soupModalImage = document.querySelector("[data-soup-modal-image]");
const soupModalTitle = document.querySelector("[data-soup-modal-title]");
const soupModalTagline = document.querySelector("[data-soup-modal-tagline]");
const soupModalDescription = document.querySelector("[data-soup-modal-description]");
const videoModal = document.querySelector(".video-modal");
const videoOpen = document.querySelector("[data-video-open]");
const videoClosers = document.querySelectorAll("[data-video-close]");
let activeSoupTrigger = null;

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.14 });

revealItems.forEach((item) => revealObserver.observe(item));

document.querySelectorAll(".gallery-tile[data-demo-toast]").forEach((tile) => {
    tile.addEventListener("click", () => {
        toast.textContent = tile.dataset.demoToast;
        toast.classList.add("is-visible");
        window.clearTimeout(window.__soupToastTimer);
        window.__soupToastTimer = window.setTimeout(() => {
            toast.classList.remove("is-visible");
        }, 1800);
    });
});

document.querySelectorAll(".soup-card, .feature-card, .gallery-tile").forEach((card) => {
    card.addEventListener("pointermove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        card.style.setProperty("--tilt-x", `${(-y * 4).toFixed(2)}deg`);
        card.style.setProperty("--tilt-y", `${(x * 4).toFixed(2)}deg`);
    });

    card.addEventListener("pointerleave", () => {
        card.style.setProperty("--tilt-x", "0deg");
        card.style.setProperty("--tilt-y", "0deg");
    });
});

const setModalLock = () => {
    document.body.classList.toggle(
        "modal-open",
        soupModal?.classList.contains("is-open") || videoModal?.classList.contains("is-open")
    );
};

const setSoupState = (open, trigger = null) => {
    if (!soupModal) return;

    if (open && trigger) {
        activeSoupTrigger = trigger;
        soupModalImage.src = trigger.dataset.soupImage;
        soupModalImage.alt = trigger.dataset.soupAlt;
        soupModalTitle.textContent = trigger.dataset.soupTitle;
        soupModalTagline.textContent = trigger.dataset.soupTagline;
        soupModalDescription.textContent = trigger.dataset.soupDescription;
    }

    soupModal.classList.toggle("is-open", open);
    soupModal.setAttribute("aria-hidden", String(!open));
    setModalLock();

    if (!open && activeSoupTrigger) {
        activeSoupTrigger.focus();
        activeSoupTrigger = null;
    }
};

const setVideoState = (open) => {
    videoModal.classList.toggle("is-open", open);
    videoModal.setAttribute("aria-hidden", String(!open));
    setModalLock();
};

soupOpeners.forEach((opener) => opener.addEventListener("click", () => setSoupState(true, opener)));
soupClosers.forEach((closer) => closer.addEventListener("click", () => setSoupState(false)));
videoOpen?.addEventListener("click", () => setVideoState(true));
videoClosers.forEach((closer) => closer.addEventListener("click", () => setVideoState(false)));

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        setSoupState(false);
        setVideoState(false);
    }
});

let parallaxFrame = 0;

document.addEventListener("pointermove", (event) => {
    const x = event.clientX / window.innerWidth - 0.5;
    const y = event.clientY / window.innerHeight - 0.5;

    window.cancelAnimationFrame(parallaxFrame);
    parallaxFrame = window.requestAnimationFrame(() => {
        document.documentElement.style.setProperty("--parallax-x", `${x * 16}px`);
        document.documentElement.style.setProperty("--parallax-y", `${y * 16}px`);
    });
});
