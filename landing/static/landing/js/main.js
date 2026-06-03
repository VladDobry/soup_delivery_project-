const revealItems = document.querySelectorAll(".reveal");
const toast = document.querySelector(".toast");
const soupModal = document.querySelector(".soup-modal");
const soupOpeners = document.querySelectorAll("[data-soup-open]");
const soupClosers = document.querySelectorAll("[data-soup-close]");
const soupModalImage = document.querySelector("[data-soup-modal-image]");
const soupModalTitle = document.querySelector("[data-soup-modal-title]");
const soupModalKicker = document.querySelector("[data-soup-modal-kicker]");
const soupModalTagline = document.querySelector("[data-soup-modal-tagline]");
const soupModalDescription = document.querySelector("[data-soup-modal-description]");
const soupModalNote = document.querySelector("[data-soup-modal-note]");
const soupModalChips = document.querySelector("[data-soup-modal-chips]");
const soupModalGroups = document.querySelector("[data-soup-modal-groups]");
const soupModalSecret = document.querySelector("[data-soup-modal-secret]");
const umamiModal = document.querySelector(".umami-modal");
const umamiOpen = document.querySelector("[data-umami-open]");
const umamiClosers = document.querySelectorAll("[data-umami-close]");
const videoModal = document.querySelector(".video-modal");
const videoOpen = document.querySelector("[data-video-open]");
const videoClosers = document.querySelectorAll("[data-video-close]");
let activeSoupTrigger = null;
let activeUmamiTrigger = null;

const soupDetails = {
    borsch: {
        title: "Борщ",
        kicker: "Супотерапия N1",
        tagline: "На страже твоего желудка",
        description: "Настоящий борщ с насыщенным вкусом и глубоким характером. Такой, каким он и должен быть.",
        image: "/static/landing/img/soup-borsch.png",
        alt: "Борщ в черной чаше",
        accent: "#c51d25",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        secret: "Несколько ингредиентов мы оставляем в тайне. Иначе это будет уже не наш борщ.",
        chips: [
            ["🍲", "Коллагеновый бульон"],
            ["🥩", "Говядина"],
            ["🧅", "Свекла"],
            ["🥬", "Капуста"],
            ["🍅", "Томаты"],
            ["🧄", "Чеснок"]
        ],
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
        kicker: "Супотерапия N2",
        tagline: "После неправильных решений",
        description: "Густая, наваристая, с характером. Солянка — это когда все сложное становится вкусным.",
        image: "/static/landing/img/soup-solyanka.png",
        alt: "Солянка с оливками и лимоном",
        accent: "#c33123",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        secret: "Если день пошел не по плану, солянка все исправит.",
        chips: [
            ["🦆", "Утка"],
            ["🥩", "Копченые ребра"],
            ["🍄", "Грузди"],
            ["🥒", "Огурцы"],
            ["⚫", "Оливки"],
            ["🫒", "Каперсы"]
        ],
        groups: [
            ["🍲", "Основа", "Коллагеновый петуховый бульон"],
            ["🥩", "Копчености", "Фермерская утка горячего копчения. Говяжьи ребра горячего копчения"],
            ["🍄", "Соленья и деликатесы", "Квашеная капуста, соленые грузди, бочковые огурцы, оливки, маслины, каперсы"],
            ["🥕", "Овощная база", "Репчатый лук, лук-порей, морковь, чеснок, сельдерей, протертые томаты, томатная паста"],
            ["🌿", "Зелень", "Укроп, петрушка"],
            ["🧂", "Специи и вкус", "Гвоздика, лавровый лист, черный перец горошком, натуральные специи"]
        ]
    },
    ukha: {
        title: "Уха",
        kicker: "Супотерапия N3",
        tagline: "На норвежский манер",
        description: "Сливочная, ароматная, с благородной рыбой и нотками Севера. Согревает и вдохновляет.",
        image: "/static/landing/img/soup-ukha.png",
        alt: "Уха с рыбой и картофелем",
        accent: "#1f5c8e",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        secret: "Нежность сливочной основы держится на чистом бульоне и правильной рыбе.",
        chips: [
            ["🐟", "Семга"],
            ["🐟", "Тунец"],
            ["🐟", "Зубатка"],
            ["🥛", "Кокосовое молоко"],
            ["🍄", "Шиитаке"],
            ["🥔", "Картофель"]
        ],
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
        title: "Тыквенный крем-суп",
        kicker: "Супотерапия N4",
        tagline: "С лангустинами",
        description: "Нежный, бархатистый, с легкой сладостью тыквы и изысканным ароматом трюфеля.",
        image: "/static/landing/img/soup-pumpkin.png",
        alt: "Тыквенный суп-пюре с креветкой",
        accent: "#e36f16",
        note: "Готовится с любовью и томлением 25 часов на живом огне",
        secret: "Оливковое масло с ароматом белого трюфеля добавляет тот самый финальный штрих.",
        chips: [
            ["🎃", "Тыква"],
            ["🍠", "Батат"],
            ["🦐", "Лангустины"],
            ["🥥", "Кокосовое молоко"],
            ["🧄", "Белый трюфель"],
            ["🍲", "Коллагеновый бульон"]
        ],
        groups: [
            ["🍲", "Основа", "Тыква, батат. Коллагеновый петуховый бульон"],
            ["🥥", "Сливочная база", "Кокосовое молоко, сливочное масло, оливковое масло"],
            ["🦐", "Морепродукты", "Аргентинские лангустины"],
            ["🥕", "Овощи и зелень", "Репчатый лук, лук-порей, морковь, чеснок, сельдерей, укроп, петрушка"],
            ["✨", "Фирменный штрих", "Оливковое масло с ароматом белого трюфеля"],
            ["🧂", "Специи и вкус", "Гвоздика, лавровый лист, черный перец горошком, натуральные специи"]
        ]
    },
    broth: {
        title: "Коллагеновый бульон",
        kicker: "Супотерапия N5",
        tagline: "Сила внутри",
        description: "Долгий коллагеновый бульон, сваренный на живом огне. Чистая основа, глубокий вкус и спокойная сила без химии.",
        image: "/static/landing/img/soup-broth.png",
        alt: "Коллагеновый бульон с овощами",
        accent: "#b98335",
        note: "Томится 25 часов, чтобы вкус стал глубоким, а основа — честной",
        secret: "Главный ингредиент здесь — время. Бульон не торопят, его доводят до силы.",
        chips: [
            ["🍲", "Долгий бульон"],
            ["💧", "Родниковая вода"],
            ["🥕", "Морковь"],
            ["🧅", "Лук"],
            ["🌿", "Зелень"],
            ["🧂", "Специи"]
        ],
        groups: [
            ["🍲", "Основа", "Коллагеновый бульон долгого томления на живом огне"],
            ["💧", "Вода", "Чистая родниковая вода для мягкого вкуса"],
            ["🥕", "Овощная база", "Морковь, репчатый лук, лук-порей, сельдерей, чеснок"],
            ["🌿", "Зелень", "Укроп, петрушка"],
            ["🧂", "Специи и вкус", "Лавровый лист, черный перец горошком, морская соль, натуральные специи"],
            ["✨", "Польза", "Насыщенная основа для супов и самостоятельный горячий бульон"]
        ]
    }
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

document.querySelectorAll(".soup-card, .feature-card, .gallery-tile, .umami-teaser").forEach((card) => {
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
        videoModal?.classList.contains("is-open")
    );
};

const renderSoupChips = (chips) => {
    if (!soupModalChips) return;

    soupModalChips.replaceChildren();

    chips.forEach(([icon, label]) => {
        const chip = document.createElement("span");
        chip.className = "soup-chip";

        const iconEl = document.createElement("b");
        iconEl.textContent = icon;
        iconEl.setAttribute("aria-hidden", "true");

        const labelEl = document.createElement("small");
        labelEl.textContent = label;

        chip.append(iconEl, labelEl);
        soupModalChips.append(chip);
    });
};

const renderSoupGroups = (groups) => {
    if (!soupModalGroups) return;

    soupModalGroups.replaceChildren();

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

const setSoupState = (open, trigger = null) => {
    if (!soupModal) return;

    if (open && trigger) {
        const detail = soupDetails[trigger.dataset.soupId] || soupDetails.borsch;

        activeSoupTrigger = trigger;
        soupModal.style.setProperty("--soup-accent", detail.accent);
        soupModalImage.src = detail.image;
        soupModalImage.alt = detail.alt;
        soupModalTitle.textContent = detail.title;
        soupModalKicker.textContent = detail.kicker;
        soupModalTagline.textContent = detail.tagline;
        soupModalDescription.textContent = detail.description;
        soupModalNote.textContent = detail.note;
        soupModalSecret.textContent = detail.secret;
        renderSoupChips(detail.chips);
        renderSoupGroups(detail.groups);
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

const setUmamiState = (open, trigger = null) => {
    if (!umamiModal) return;

    if (open && trigger) {
        activeUmamiTrigger = trigger;
    }

    umamiModal.classList.toggle("is-open", open);
    umamiModal.setAttribute("aria-hidden", String(!open));
    setModalLock();

    if (!open && activeUmamiTrigger) {
        activeUmamiTrigger.focus();
        activeUmamiTrigger = null;
    }
};

soupOpeners.forEach((opener) => opener.addEventListener("click", () => setSoupState(true, opener)));
soupClosers.forEach((closer) => closer.addEventListener("click", () => setSoupState(false)));
umamiOpen?.addEventListener("click", () => setUmamiState(true, umamiOpen));
umamiClosers.forEach((closer) => closer.addEventListener("click", () => setUmamiState(false)));
videoOpen?.addEventListener("click", () => setVideoState(true));
videoClosers.forEach((closer) => closer.addEventListener("click", () => setVideoState(false)));

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        setSoupState(false);
        setUmamiState(false);
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
