const revealItems = document.querySelectorAll(".reveal");
const assetVersion = new URL(document.currentScript.src).searchParams.get("v");
const versionAsset = (path) => `${path}${assetVersion ? `?v=${assetVersion}` : ""}`;
const toast = document.querySelector(".toast");
const soupModal = document.querySelector(".soup-modal");
const soupDialog = document.querySelector(".soup-dialog");
const soupOpeners = document.querySelectorAll("[data-soup-open]");
const soupClosers = document.querySelectorAll("[data-soup-close]");
const soupPrev = document.querySelector("[data-soup-prev]");
const soupNext = document.querySelector("[data-soup-next]");
const soupModalImage = document.querySelector("[data-soup-modal-image]");
const soupModalTitle = document.querySelector("[data-soup-modal-title]");
const soupModalTagline = document.querySelector("[data-soup-modal-tagline]");
const soupModalDescription = document.querySelector("[data-soup-modal-description]");
const soupModalNote = document.querySelector("[data-soup-modal-note]");
const soupModalGroups = document.querySelector("[data-soup-modal-groups]");
const brothPassport = document.querySelector("[data-broth-passport]");
const soupSiteLink = document.querySelector("[data-soup-site-link]");
const soupUmamiOpen = document.querySelector("[data-soup-umami-open]");
const umamiModal = document.querySelector(".umami-modal");
const umamiClosers = document.querySelectorAll("[data-umami-close]");
const umamiCloseButton = document.querySelector(".umami-close");
const umamiDialog = document.querySelector(".umami-dialog");
const videoModal = document.querySelector(".video-modal");
const videoOpen = document.querySelector("[data-video-open]");
const videoClosers = document.querySelectorAll("[data-video-close]");
const soupVideo = document.querySelector(".soup-video");
const videoPreview = document.querySelector(".gallery-video-preview");
const orderModal = document.querySelector(".order-modal");
const orderDialog = document.querySelector(".order-dialog");
const orderOpeners = document.querySelectorAll("[data-order-open]");
const orderClosers = document.querySelectorAll("[data-order-close]");
const orderCloseButton = document.querySelector(".order-close");
const soupPriceItems = document.querySelectorAll("[data-soup-price]");
const soupSequence = Array.from(soupOpeners)
    .map((opener) => opener.dataset.soupId)
    .filter(Boolean);
let activeSoupTrigger = null;
let activeSoupId = null;
let previousScrollRestoration = null;
let activeUmamiTrigger = null;
let returnToSoupFromUmami = false;
let videoPreviewInView = false;
let activeOrderTrigger = null;
let orderReturnTarget = null;

const parseJsonScript = (id, fallback) => {
    const element = document.getElementById(id);
    if (!element) return fallback;

    try {
        return JSON.parse(element.textContent);
    } catch {
        return fallback;
    }
};

const fallbackDefaultSoupPrices = {
    "1l": "1550 ₽",
    "15l": "2250 ₽",
    "2l": "2850 ₽"
};

const fallbackSoupPriceOverrides = {
    ukha: {
        "1l": "1550 ₽",
        "15l": "2250 ₽",
        "2l": "2850 ₽"
    },
    broth: {
        "2l": "2850 ₽"
    }
};

const defaultSoupPrices = parseJsonScript("default-soup-prices", fallbackDefaultSoupPrices);
const soupPriceOverrides = parseJsonScript("soup-price-overrides", fallbackSoupPriceOverrides);

const soupDetails = {
    borsch: {
        title: "Борщ",
        tagline: "Яркий, здоровый, сочный!",
        description: "Невероятный баланс витаминов и минералов. Источник насыщенной жизни и вкуса умами!",
        image: "/static/landing/img/soup-borsch.png",
        alt: "Борщ в черной чаше",
        accent: "#c51d25",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        groups: [
            ["🍲", "Основа", "Коллагеновый говяжий бульон. Коллагеновый петуховый бульон"],
            ["🥕", "Овощная база", "Свекла, капуста белокочанная, морковь, репчатый лук, лук-порей, болгарский перец, томат протертый, томатная паста, чеснок, сельдерей"],
            ["🥩", "Мясо", "Говядина и телятина"],
            ["🌿", "Зелень", "Укроп, петрушка"],
            ["🧂", "Специи и вкус", "Лавровый лист, гвоздика, черный перец горошком, перец чили, морская соль, тростниковый сахар, подсолнечное масло холодного отжима, натуральные специи"]
        ]
    },
    solyanka: {
        title: "Солянка",
        tagline: "Идеальный завтрак после веселого ужина",
        description: "Густая, яркая и насыщенная. Суп, который собирает весь вкус в одной тарелке.",
        image: versionAsset("/static/landing/img/soup-solyanka.png"),
        alt: "Солянка с оливками и лимоном",
        accent: "#c33123",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        groups: [
            ["🍲", "Основа", "Коллагеновый петуховый бульон"],
            ["🥩", "Копчености", "домашняя утка, говяжьи ребра, петух горячего копчения,  собственного производства"],
            ["🥒", "Соленья и деликатесы", "Квашеная капуста, соленые грузди, бочковые огурцы, оливки, маслины, каперсы"],
            ["🥕", "Овощная база", "Репчатый лук, лук-порей, морковь, чеснок, сельдерей, протертые томаты, томатная паста"],
            ["🌿", "Зелень", "Укроп, петрушка"],
            ["🧂", "Специи и вкус", "Гвоздика, лавровый лист, черный перец горошком, натуральные специи"]
        ]
    },
    ukha: {
        title: "Уха",
        tagline: "На норвежский манер",
        description: "Невероятный вкус и аромат! Три вида морской рыбы. Кокосовое молоко  и свежие овощи обволакивают нежностью и дарят новые краски вкуса!",
        image: "/static/landing/img/soup-ukha.png",
        alt: "Уха с рыбой и картофелем",
        accent: "#1f5c8e",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        prices: soupPriceOverrides.ukha || fallbackSoupPriceOverrides.ukha,
        groups: [
            ["🍲", "Основа", "Коллагеновый бульон из семги. Коллагеновый петуховый бульон"],
            ["🐟", "Рыба", "Семга, зубатка, тунец"],
            ["🥕", "Овощи", "Картофель, морковь, репчатый лук, лук-порей, сельдерей, чеснок, сладкий перец, перец чили, грибы шиитаке, шампиньоны"],
            ["🥛", "Сливочная основа", "Кокосовое молоко, оливковое масло, сливочное масло"],
            ["🌿", "Зелень", "Укроп, петрушка"],
            ["🧂", "Специи и вкус", "Лавровый лист, черный перец горошком, натуральные специи"]
        ]
    },
    pumpkin: {
        title: "Тыквенный суп-пюре",
        tagline: "С лангустинами",
        description: "Безупречная сливочная текстура французской кулинарной школы.",
        image: "/static/landing/img/soup-pumpkin.png",
        alt: "Тыквенный суп-пюре с креветкой",
        accent: "#e36f16",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        groups: [
            ["🍲", "Основа", "Тыква, батат. Коллагеновый петуховый бульон"],
            ["🧈", "Сливочная база", "Cливочное масло"],
            ["🦐", "Морепродукты", "Аргентинские лангустины"],
            ["🥕", "Овощи и зелень", "Репчатый лук, лук-порей, морковь, чеснок, сельдерей, укроп, петрушка, имбирь"],
            ["✨", "Фирменный штрих", "Тыквенные семечки, оливковое масло с ароматом белого трюфеля"],
            ["🧂", "Специи и вкус", "Гвоздика, лавровый лист, черный перец горошком, натуральные специи"]
        ]
    },
    broth: {
        title: "Коллагеновый бульон",
        tagline: "Сила в тебе",
        description: "Для витаминно - минерального эффекта галактического масштаба.",
        image: versionAsset("/static/landing/img/soup-broth.png"),
        alt: "Коллагеновый бульон",
        accent: "#b98335",
        note: "Томится 25 часов, чтобы вкус стал глубоким, а основа — честной",
        prices: soupPriceOverrides.broth || fallbackSoupPriceOverrides.broth,
        passport: {
            types: ["Говяжий", "Петух", "Сёмга"],
            water: "Горная кристально чистая",
            aromatherapy: "Гвоздика, корень сельдерея, лук-порей, укроп, петрушка, розмарин, лук репчатый, морковь, черный перец (горошек), лавровый лист"
        }
    }
};

const renderSoupPrices = (prices = defaultSoupPrices) => {
    const visibleRows = [];

    soupPriceItems.forEach((item) => {
        const price = prices[item.dataset.soupPrice];
        const priceRow = item.closest("span");

        if (price) {
            item.textContent = price;
            if (priceRow) {
                priceRow.hidden = false;
                priceRow.style.display = "";
                priceRow.style.borderLeft = "";
                visibleRows.push(priceRow);
            }
        } else if (priceRow) {
            priceRow.hidden = true;
            priceRow.style.display = "none";
            priceRow.style.borderLeft = "0";
        }
    });

    const priceGrid = soupPriceItems[0]?.closest(".soup-offer-prices");
    if (priceGrid) {
        const columnCount = Math.max(visibleRows.length, 1);
        priceGrid.style.gridTemplateColumns = `repeat(${columnCount}, minmax(0, 1fr))`;
    }

    visibleRows.forEach((row, index) => {
        if (index === 0) {
            row.style.borderLeft = "0";
        }
    });
};

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
        soupModal?.classList.contains("is-open") ||
        umamiModal?.classList.contains("is-open") ||
        videoModal?.classList.contains("is-open") ||
        orderModal?.classList.contains("is-open")
    );
};

const renderSoupGroups = (groups) => {
    if (!soupModalGroups) return;

    soupModalGroups.replaceChildren();
    soupModalGroups.hidden = false;

    groups.forEach(([icon, title, text]) => {
        const group = document.createElement("article");
        group.className = "soup-group";

        const iconEl = document.createElement("span");
        iconEl.textContent = icon;
        iconEl.setAttribute("aria-hidden", "true");

        const copy = document.createElement("div");
        const heading = document.createElement("h3");
        const paragraph = document.createElement("p");

        heading.textContent = title;
        paragraph.textContent = text;
        copy.append(heading, paragraph);
        group.append(iconEl, copy);
        soupModalGroups.append(group);
    });
};

const renderBrothPassport = (passport) => {
    if (!brothPassport) return;

    brothPassport.replaceChildren();
    brothPassport.hidden = !passport;

    if (soupModalGroups) {
        soupModalGroups.hidden = Boolean(passport);
    }

    if (!passport) return;

    const typesSection = document.createElement("section");
    typesSection.className = "broth-passport-section broth-passport-types";

    const typesTitle = document.createElement("h3");
    typesTitle.textContent = "Виды";

    const typeList = document.createElement("div");
    typeList.className = "broth-type-list";
    passport.types.forEach((type) => {
        const item = document.createElement("span");
        item.textContent = type;
        typeList.append(item);
    });
    typesSection.append(typesTitle, typeList);

    const waterSection = document.createElement("section");
    waterSection.className = "broth-passport-section";
    const waterTitle = document.createElement("h3");
    waterTitle.textContent = "Вода";
    const waterText = document.createElement("p");
    waterText.textContent = passport.water;
    waterSection.append(waterTitle, waterText);

    const aromaSection = document.createElement("section");
    aromaSection.className = "broth-passport-section";
    const aromaTitle = document.createElement("h3");
    aromaTitle.textContent = "Ароматерапия";
    const aromaText = document.createElement("p");
    aromaText.textContent = passport.aromatherapy;
    aromaSection.append(aromaTitle, aromaText);

    brothPassport.append(typesSection, waterSection, aromaSection);
};

const renderSoupContent = (trigger) => {
    if (!trigger) return;

    const detail = soupDetails[trigger.dataset.soupId] || soupDetails.borsch;

    activeSoupTrigger = trigger;
    activeSoupId = trigger.dataset.soupId;
    soupModal.style.setProperty("--soup-accent", detail.accent);
    soupModalImage.src = detail.image;
    soupModalImage.alt = detail.alt;
    soupModalTitle.textContent = detail.title;
    soupModalTagline.textContent = detail.tagline;
    soupModalDescription.textContent = detail.description;
    soupModalNote.textContent = detail.note;
    renderSoupPrices(detail.prices);
    renderSoupGroups(detail.groups || []);
    renderBrothPassport(detail.passport);
};

const setSoupState = (open, trigger = null) => {
    if (!soupModal) return;

    if (open && trigger) {
        renderSoupContent(trigger);
    }

    soupModal.classList.toggle("is-open", open);
    soupModal.setAttribute("aria-hidden", String(!open));
    setModalLock();

    if (!open && activeSoupTrigger) {
        activeSoupTrigger.focus({ preventScroll: true });
        activeSoupTrigger = null;
    }

    if (!open) {
        activeSoupId = null;
    }
};

const setVideoState = (open) => {
    if (!videoModal) return;

    const wasOpen = videoModal.classList.contains("is-open");
    videoModal.classList.toggle("is-open", open);
    videoModal.setAttribute("aria-hidden", String(!open));
    setModalLock();

    if (open) {
        if (videoPreview && soupVideo) {
            const previewTime = videoPreview.currentTime;
            if (soupVideo.readyState > 0) {
                soupVideo.currentTime = previewTime;
            } else {
                soupVideo.addEventListener("loadedmetadata", () => {
                    soupVideo.currentTime = previewTime;
                    soupVideo.play().catch(() => {});
                }, { once: true });
            }
            videoPreview.pause();
        }
        videoModal.querySelector(".video-close")?.focus({ preventScroll: true });
        soupVideo?.play().catch(() => {});
    } else if (wasOpen && soupVideo) {
        if (videoPreview?.readyState > 0) {
            videoPreview.currentTime = soupVideo.currentTime;
        }
        soupVideo.pause();
        if (videoPreviewInView) {
            videoPreview?.play().catch(() => {});
        }
        videoOpen?.focus({ preventScroll: true });
    }
};

if (videoPreview) {
    videoPreview.muted = true;

    const videoPreviewObserver = new IntersectionObserver(([entry]) => {
        videoPreviewInView = entry.isIntersecting;

        if (entry.isIntersecting && !videoModal?.classList.contains("is-open")) {
            videoPreview.play().catch(() => {});
        } else {
            videoPreview.pause();
        }
    }, {
        rootMargin: "180px 0px",
        threshold: 0.05,
    });

    videoPreviewObserver.observe(videoPreview);
}

const setUmamiState = (open, trigger = null) => {
    if (!umamiModal) return;

    if (open && trigger) {
        activeUmamiTrigger = trigger;
    }

    umamiModal.classList.toggle("is-open", open);
    umamiModal.setAttribute("aria-hidden", String(!open));

    if (!open && returnToSoupFromUmami && activeSoupId) {
        soupModal?.classList.add("is-open");
        soupModal?.setAttribute("aria-hidden", "false");
    }

    setModalLock();

    if (open) {
        umamiCloseButton?.focus({ preventScroll: true });
    }

    if (!open && activeUmamiTrigger) {
        activeUmamiTrigger.focus({ preventScroll: true });
        activeUmamiTrigger = null;
    }

    if (!open) {
        returnToSoupFromUmami = false;
    }
};

const openUmamiFromSoup = () => {
    if (!soupModal || !activeSoupId || !soupUmamiOpen) return;

    returnToSoupFromUmami = true;
    soupModal.classList.remove("is-open");
    soupModal.setAttribute("aria-hidden", "true");
    setUmamiState(true, soupUmamiOpen);
};

const setOrderState = (open, trigger = null) => {
    if (!orderModal) return;

    if (open && trigger) {
        activeOrderTrigger = trigger;

        if (soupModal?.classList.contains("is-open")) {
            orderReturnTarget = "soup";
            soupModal.classList.remove("is-open");
            soupModal.setAttribute("aria-hidden", "true");
        } else if (umamiModal?.classList.contains("is-open")) {
            orderReturnTarget = "umami";
            umamiModal.classList.remove("is-open");
            umamiModal.setAttribute("aria-hidden", "true");
        } else {
            orderReturnTarget = null;
        }
    }

    orderModal.classList.toggle("is-open", open);
    orderModal.setAttribute("aria-hidden", String(!open));

    if (!open && orderReturnTarget === "soup" && activeSoupId) {
        soupModal?.classList.add("is-open");
        soupModal?.setAttribute("aria-hidden", "false");
    } else if (!open && orderReturnTarget === "umami") {
        umamiModal?.classList.add("is-open");
        umamiModal?.setAttribute("aria-hidden", "false");
    }

    setModalLock();

    if (open) {
        orderCloseButton?.focus({ preventScroll: true });
    } else {
        activeOrderTrigger?.focus({ preventScroll: true });
        activeOrderTrigger = null;
        orderReturnTarget = null;
    }
};

const findSoupOpener = (soupId) => (
    Array.from(soupOpeners).find((opener) => opener.dataset.soupId === soupId) || null
);

const showAdjacentSoup = (direction) => {
    if (!soupModal?.classList.contains("is-open") || !activeSoupId || !soupSequence.length) {
        return;
    }

    const activeIndex = soupSequence.indexOf(activeSoupId);
    const currentIndex = activeIndex === -1 ? 0 : activeIndex;
    const nextIndex = (currentIndex + direction + soupSequence.length) % soupSequence.length;
    const nextOpener = findSoupOpener(soupSequence[nextIndex]);

    if (!nextOpener || nextOpener.dataset.soupId === activeSoupId) return;

    disableSoupScrollRestoration();
    window.history.pushState(
        { soupId: nextOpener.dataset.soupId },
        "",
        nextOpener.dataset.soupUrl
    );
    setSoupState(true, nextOpener);
};

const restoreSoupScrollRestoration = () => {
    if (previousScrollRestoration === null) return;

    window.history.scrollRestoration = previousScrollRestoration;
    previousScrollRestoration = null;
};

const scrollToSoups = (repeat = false) => {
    const soupsSection = document.querySelector("#soups");
    if (!soupsSection) return;

    const scroll = () => {
        const previousBehavior = document.documentElement.style.scrollBehavior;
        document.documentElement.style.scrollBehavior = "auto";
        soupsSection.scrollIntoView({ block: "start" });
        document.documentElement.style.scrollBehavior = previousBehavior;
    };

    scroll();

    if (repeat) {
        window.requestAnimationFrame(() => {
            scroll();
            window.setTimeout(() => {
                scroll();
                restoreSoupScrollRestoration();
            }, 150);
        });
    }
};

const disableSoupScrollRestoration = () => {
    if (!("scrollRestoration" in window.history) || previousScrollRestoration !== null) {
        return;
    }

    previousScrollRestoration = window.history.scrollRestoration;
    window.history.scrollRestoration = "manual";
};

const showSoupFromUrl = (useInitialSoup = false) => {
    const match = window.location.pathname.match(/^\/soup\/([^/]+)\/$/);
    const soupId = match?.[1] || (useInitialSoup ? document.body.dataset.initialSoup : "");
    const opener = soupId ? findSoupOpener(soupId) : null;

    if (opener) {
        setSoupState(true, opener);
    } else if (soupModal?.classList.contains("is-open")) {
        setSoupState(false);
        scrollToSoups(true);
    }
};

const closeSoupWithNavigation = () => {
    if (window.history.state?.soupId) {
        window.history.back();
        return;
    }

    window.history.replaceState({}, "", "/#soups");
    setSoupState(false);
    scrollToSoups(true);
};

const closeSoupModalDirectly = () => {
    window.history.replaceState({}, "", "/#soups");
    setSoupState(false);
    scrollToSoups(true);
};

soupPrev?.addEventListener("click", () => showAdjacentSoup(-1));
soupNext?.addEventListener("click", () => showAdjacentSoup(1));

let soupSwipeStart = null;

soupDialog?.addEventListener("pointerdown", (event) => {
    if (event.pointerType === "mouse" || !soupModal?.classList.contains("is-open")) {
        soupSwipeStart = null;
        return;
    }

    soupSwipeStart = {
        pointerId: event.pointerId,
        x: event.clientX,
        y: event.clientY,
    };
});

soupDialog?.addEventListener("pointerup", (event) => {
    if (!soupSwipeStart || soupSwipeStart.pointerId !== event.pointerId) return;

    const deltaX = event.clientX - soupSwipeStart.x;
    const deltaY = event.clientY - soupSwipeStart.y;
    const absX = Math.abs(deltaX);
    const absY = Math.abs(deltaY);
    soupSwipeStart = null;

    if (absX < 50 || absX <= absY * 1.25) return;

    showAdjacentSoup(deltaX < 0 ? 1 : -1);
});

soupDialog?.addEventListener("pointercancel", () => {
    soupSwipeStart = null;
});

soupOpeners.forEach((opener) => opener.addEventListener("click", () => {
    if (activeSoupId === opener.dataset.soupId) return;

    disableSoupScrollRestoration();
    window.history.pushState(
        { soupId: opener.dataset.soupId },
        "",
        opener.dataset.soupUrl
    );
    setSoupState(true, opener);
}));

soupClosers.forEach((closer) => closer.addEventListener("click", (event) => {
    if (closer.matches("a[href]")) {
        setSoupState(false);
        restoreSoupScrollRestoration();
        return;
    }

    event.preventDefault();
    closeSoupModalDirectly();
}));

soupSiteLink?.addEventListener("click", (event) => {
    event.preventDefault();
    window.history.replaceState({}, "", soupSiteLink.href);
    setSoupState(false);
    scrollToSoups(true);
});

window.addEventListener("popstate", () => showSoupFromUrl());
showSoupFromUrl(true);
soupUmamiOpen?.addEventListener("click", openUmamiFromSoup);
umamiClosers.forEach((closer) => closer.addEventListener("click", () => {
    if (closer.matches("a[href]") && returnToSoupFromUmami) {
        returnToSoupFromUmami = false;
        activeUmamiTrigger = null;
        activeSoupTrigger = null;
        setSoupState(false);
        restoreSoupScrollRestoration();
    }

    setUmamiState(false);
}));
videoOpen?.addEventListener("click", () => setVideoState(true));
videoClosers.forEach((closer) => closer.addEventListener("click", () => setVideoState(false)));
orderOpeners.forEach((opener) => opener.addEventListener("click", () => {
    setOrderState(true, opener);
}));
orderClosers.forEach((closer) => closer.addEventListener("click", () => setOrderState(false)));

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        if (orderModal?.classList.contains("is-open")) {
            setOrderState(false);
            return;
        }

        if (soupModal?.classList.contains("is-open")) {
            closeSoupModalDirectly();
        }
        setUmamiState(false);
        setVideoState(false);
    }

    const soupIsOnlyOpenModal = soupModal?.classList.contains("is-open") &&
        !orderModal?.classList.contains("is-open") &&
        !umamiModal?.classList.contains("is-open") &&
        !videoModal?.classList.contains("is-open");

    if (soupIsOnlyOpenModal && event.key === "ArrowLeft") {
        event.preventDefault();
        showAdjacentSoup(-1);
    } else if (soupIsOnlyOpenModal && event.key === "ArrowRight") {
        event.preventDefault();
        showAdjacentSoup(1);
    }

    const activeDialog = orderModal?.classList.contains("is-open")
        ? orderDialog
        : umamiModal?.classList.contains("is-open")
            ? umamiDialog
            : null;

    if (event.key === "Tab" && activeDialog) {
        const focusable = Array.from(
            activeDialog.querySelectorAll(
                'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
            )
        ).filter((element) => element.getClientRects().length > 0);

        if (!focusable.length) return;

        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
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
