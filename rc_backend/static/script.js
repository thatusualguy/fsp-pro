document.addEventListener('DOMContentLoaded', () => {
    const openNavBtn = document.getElementById('openNavBtn');
    const closeNavBtn = document.getElementById('closeNavBtn');
    const mobileNav = document.getElementById('mobileNav');
    const mobileNavLinks = mobileNav.querySelectorAll('a'); // Get links inside menu

    function openMobileMenu() {
        mobileNav.removeAttribute('hidden'); // Make it visible for transition
        // Use setTimeout to allow the 'display' change to take effect before starting transition
        setTimeout(() => {
            mobileNav.classList.add('active');
            openNavBtn.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden'; // Prevent body scroll
            closeNavBtn.focus(); // Move focus to the close button
        }, 10); // Small delay
    }

    function closeMobileMenu() {
        mobileNav.classList.remove('active');
        openNavBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = ''; // Restore body scroll

        // Hide the element fully after transition completes
        mobileNav.addEventListener('transitionend', () => {
            // Check if menu is still closed before hiding
            if (!mobileNav.classList.contains('active')) {
                mobileNav.setAttribute('hidden', '');
            }
        }, { once: true }); // Important: listener runs only once

        openNavBtn.focus(); // Return focus to the toggle button
    }

    if (openNavBtn && closeNavBtn && mobileNav) {
        // Toggle menu open
        openNavBtn.addEventListener('click', () => {
            if (mobileNav.classList.contains('active')) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });

        // Toggle menu close
        closeNavBtn.addEventListener('click', closeMobileMenu);

        // Close menu on link click (for SPA or anchor links)
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });

        // Close menu if user presses ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
                closeMobileMenu();
            }
        });

        // Close menu if user clicks outside the menu (optional)
        document.addEventListener('click', (e) => {
            if (mobileNav.classList.contains('active') && !mobileNav.contains(e.target) && e.target !== openNavBtn) {
                // Check if the click was outside the nav and not on the open button
                closeMobileMenu();
            }
        });
    }
});

// Динамически обновляем высоту SVG, чтобы соответствовать высоте контента
function updateSvgHeight() {
    const svgContainer = document.querySelector('.backgroundImage');
    const bodyHeight = document.body.scrollHeight;
    svgContainer.style.height = `${bodyHeight}px`;
}

window.addEventListener('resize', updateSvgHeight);
window.addEventListener('load', updateSvgHeight);

document.addEventListener('DOMContentLoaded', () => {

    // --- Навигация SPA ---

    const backgroundIcons = document.querySelectorAll('.background-icon');
    const navLinks = document.querySelectorAll('.nav-link'); // Все ссылки навигации с этим классом
    const sections = document.querySelectorAll('.page-section'); // Все секции контента
    const mobileNav = document.getElementById('mobileNav'); // Мобильное меню
    const closeNavBtn = document.getElementById('closeNavBtn'); // Кнопка закрытия моб. меню

    function showSection(sectionId) {
        // Нормализуем ID (убираем #)
        const targetId = sectionId.startsWith('#') ? sectionId.substring(1) : sectionId;
        if (!targetId) return; // Выходим, если ID пустой

        // Находим контейнер секции
        const sectionContainer = document.getElementById(targetId);
        if (!sectionContainer) {
            console.warn("Section container not found:", targetId);
            // Можно показать дефолтную секцию или ошибку
            // showSection('#hero'); // Как вариант
            return;
        }

        // Скрываем все остальные секции .page-section (или ваш главный селектор секций)
        document.querySelectorAll('.page-section').forEach(sec => {
            if (sec.id !== targetId) {
                sec.classList.remove('active');
                sec.hidden = true;
            }
        });

        // -- Начало добавления/изменения --

        // 1. Очищаем предыдущие классы состояния с <body>
        // Находим все классы на body, которые начинаются с 'section-active-'
        const bodyClassesToRemove = [];
        document.body.classList.forEach(className => {
            if (className.startsWith('section-active-')) {
                bodyClassesToRemove.push(className);
            }
        });
        // Удаляем их
        if (bodyClassesToRemove.length > 0) {
            document.body.classList.remove(...bodyClassesToRemove);
        }


        // 3. Показываем целевую секцию И добавляем класс состояния на <body>
        // if (loadedTemplates[targetId]) { // <-- если используете fetch
        sectionContainer.hidden = false;
        sectionContainer.classList.add('active');

        // Создаем и добавляем класс на body: например, 'section-active-about'
        const bodyStateClass = `section-active-${targetId}`;
        document.body.classList.add(bodyStateClass);

        // (Ваша существующая логика прокрутки, обновления URL и т.д.)
        window.scrollTo(0, 0);
        try {
            history.pushState(null, '', `#${targetId}`);
        } catch (e) { /* ... */

        }

        closeMobileMenuIfNeeded();
        updateSvgHeight();
    }

    function closeMobileMenuIfNeeded() {
         const mobileNav = document.getElementById('mobileNav');
         const openNavBtn = document.getElementById('openNavBtn');
         if (mobileNav && mobileNav.classList.contains('active')) {
              mobileNav.classList.remove('active');
              document.body.style.overflow = '';
             openNavBtn?.setAttribute('aria-expanded', 'false');
              mobileNav.addEventListener('transitionend', () => {
                 mobileNav.hidden = true;
             }, { once: true });
         }
    }

     function handleLocationChange() {
        const currentHash = window.location.hash || '#hero'; // Определяем стартовую секцию
        showSection(currentHash); // Вызываем обновленную функцию
    }
    window.addEventListener('popstate', handleLocationChange);
    handleLocationChange(); // Показать секцию при первой загрузке

    // Функция для показа нужной секции
    // function showSection(sectionId) {
    //
    //     Нормализуем ID (убираем # если он есть)
        // const targetId = sectionId.startsWith('#') ? sectionId.substring(1) : sectionId;
        //
        // let sectionFound = false;
        // sections.forEach(section => {
        //     if (section.id === targetId) {
        //         section.classList.add('active'); // Показываем нужную секцию
        //         sectionFound = true;
        //     } else {
        //         section.classList.remove('active'); // Скрываем остальные
        //     }
        // });
        //
        // Если секция не найдена (например, плохой хеш), показать стартовую
        // if (!sectionFound && sections.length > 0) {
        //     Пытаемся показать 'hero', если ее нет - первую секцию из списка
            // const defaultSection = document.getElementById('hero') || sections[0];
            // if (defaultSection) {
            //     defaultSection.classList.add('active');
            //     updateNavActiveState('#' + defaultSection.id); // Обновляем и нав. ссылки
            // }
        // } else if (sectionFound) {
        //     updateNavActiveState('#' + targetId); // Обновляем состояние нав. ссылок
        // }
        //
        // window.scrollTo(0, 0); // Прокрутка вверх при смене секции
        // if (targetId === "about")
        //     backgroundIcons.forEach(link => {
        //         link.classList.add('hidden');
        //     })
        // updateSvgHeight()
    // })

    // Функция для обновления активного состояния ссылок навигации
    function updateNavActiveState(targetSectionId) {
        // Нормализуем ID, если он с хешем
        const normalizedId = targetSectionId.startsWith('#') ? targetSectionId : `#${targetSectionId}`;

        navLinks.forEach(link => {
            const linkHref = link.getAttribute('href');
            // Сравниваем href ссылки с целевым ID (нормализованным с #)
            console.log(linkHref, normalizedId, linkHref === normalizedId);
            if (linkHref === normalizedId) {
                console.log(linkHref, normalizedId);
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Обработчик кликов по навигационным ссылкам
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            const targetHref = link.getAttribute('href');
            console.log('target href', targetHref);
            updateNavActiveState(targetHref);
            // Обрабатываем только внутренние hash-ссылки
            if (targetHref && targetHref.startsWith('#')) {
                event.preventDefault(); // Отменяем стандартный переход по якорю

                showSection(targetHref); // Показываем нужную секцию

                // Обновляем URL в адресной строке (опционально, но полезно)
                try {
                    history.pushState(null, '', targetHref);
                } catch (e) {
                    console.warn("History API не поддерживается или ошибка:", e);
                    // Если pushState не работает, просто меняем хеш
                    // window.location.hash = targetHref; // Это вызовет событие hashchange
                }


                // Закрываем мобильное меню, если оно было открыто
                if (mobileNav && mobileNav.classList.contains('active')) {
                    // Используем ваш существующий код закрытия меню
                    mobileNav.classList.remove('active');
                    mobileNav.hidden = true; // Если вы используете hidden атрибут
                    document.body.style.overflow = ''; // Возвращаем прокрутку
                    // Обновить aria-expanded для кнопки бургера (если нужно)
                    const openNavBtn = document.getElementById('openNavBtn');
                    if (openNavBtn) {
                        openNavBtn.setAttribute('aria-expanded', 'false');
                    }
                }
            }
            // Иначе (если это внешняя ссылка или ссылка не на секцию), ничего не делаем,
            // браузер перейдет по ней сам.
        });
    });

    // Обработка начальной загрузки страницы и кнопок Назад/Вперед
    function handleLocationChange() {
        // Определяем какую секцию показать: из URL#hash или по умолчанию 'hero'
        const currentHash = window.location.hash || '#hero'; // По умолчанию #hero
        showSection(currentHash);
        updateNavActiveState(currentHash);
    }

    // Обработчик для событий popstate (назад/вперед в браузере)
    window.addEventListener('popstate', handleLocationChange);

    // Показать начальную секцию при загрузке
    handleLocationChange();


    // --- ВАШ СУЩЕСТВУЮЩИЙ КОД для Мобильного Меню (Open/Close) ---
    // Оставьте его здесь как есть
    const openNavBtn = document.getElementById('openNavBtn');
    // ... (весь ваш код для openNavBtn.addEventListener('click', ...)
    // ... (весь ваш код для closeNavBtn.addEventListener('click', ...)

    openNavBtn?.addEventListener('click', () => {
        mobileNav.hidden = false;
        // Форсируем пересчет стилей перед добавлением класса для анимации
        void mobileNav.offsetWidth;
        mobileNav.classList.add('active');
        document.body.style.overflow = 'hidden';
        openNavBtn.setAttribute('aria-expanded', 'true');
        closeNavBtn.focus(); // Фокус на кнопку закрытия для доступности
    });

    closeNavBtn?.addEventListener('click', () => {
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
        openNavBtn.setAttribute('aria-expanded', 'false');
        // Можно добавить задержку перед скрытием для завершения анимации
        mobileNav.addEventListener('transitionend', () => {
            mobileNav.hidden = true;
        }, { once: true }); // Сработает только один раз
        openNavBtn.focus(); // Возврат фокуса на кнопку открытия
    });

    const gridContainer = document.querySelector('.regions-grid'); // Находим контейнер сетки

    function adjustLastGridItemSpan() {
        if (!gridContainer) return; // Выходим, если сетки нет

        const gridItems = gridContainer.querySelectorAll('.region-card'); // Находим элементы сетки
        if (!gridItems || gridItems.length === 0) return; // Выходим, если нет элементов

        // 1. Определяем количество колонок
        const gridComputedStyle = window.getComputedStyle(gridContainer);
        // Получаем значение grid-template-columns. Пример: "repeat(3, 1fr)" или "200px 200px 1fr"
        const gridColumnDefinition = gridComputedStyle.getPropertyValue('grid-template-columns');
        // Пытаемся посчитать колонки, разбив строку по пробелам (упрощенный вариант!)
        const numberOfColumns = gridColumnDefinition.split(' ').length;

        if (numberOfColumns <= 1) {
            // Если колонка одна или не удалось определить, убираем все доп. стили
            gridItems.forEach(item => {
                item.style.gridColumn = ''; // Сброс стиля
            });
            return;
        }

        // 2. Считаем элементы
        const totalItems = gridItems.length;
        let itemsInLastRow = totalItems % numberOfColumns;

        // Если остаток 0, значит последняя строка полная
        if (itemsInLastRow === 0 && totalItems > 0) {
            itemsInLastRow = numberOfColumns;
        }

        // 3. Сбрасываем предыдущие стили span у ВСЕХ элементов перед применением новых
        gridItems.forEach(item => {
            item.style.gridColumn = '';
        });

        // 4. Применяем span, если последняя строка не полная
        if (itemsInLastRow > 0 && itemsInLastRow < numberOfColumns) {
            const lastItem = gridItems[gridItems.length - 1]; // Берем последний элемент
            const spanValue = numberOfColumns - itemsInLastRow + 1; // На сколько колонок растянуть

            if (lastItem) {
                console.log(`Last row incomplete. Spanning last item by ${spanValue} columns.`);
                lastItem.style.gridColumn = `span ${spanValue}`;
            }
        } else {
            // Если последняя строка полная или элементов нет
            console.log("Last row is full or grid is empty. No span applied.");
        }
    }

    // Оборачиваем вызов функции в debounce для события resize
    const debouncedAdjustSpan = debounce(adjustLastGridItemSpan, 250); // Задержка 250ms

    // Вызываем функцию при загрузке
    adjustLastGridItemSpan();

    // Вызываем при изменении размера окна (с debounce)
    window.addEventListener('resize', debouncedAdjustSpan);

    const subjectsList = document.querySelector('.subjects-list');

    if (subjectsList) {
        subjectsList.addEventListener('click', (event) => {
            // Находим ближайший родительский элемент .subject-item, на который кликнули
            // Мы слушаем клик на всем списке для делегирования событий
            const targetItem = event.target.closest('.subject-item.expandable');

            // Если клик был не по expandable элементу или его потомку, выходим
            if (!targetItem) {
                return;
            }

            // Опционально: Закрыть другие открытые элементы (Accordion эффект)
            // const currentlyExpanded = subjectsList.querySelector('.subject-item.expanded');
            // if (currentlyExpanded && currentlyExpanded !== targetItem) {
            //     currentlyExpanded.classList.remove('expanded');
            //     // Обновить ARIA для ранее открытого элемента
            //     const currentlyExpandedHeader = currentlyExpanded.querySelector('.subject-item__header');
            //     if (currentlyExpandedHeader) currentlyExpandedHeader.setAttribute('aria-expanded', 'false');
            // }

            // Переключаем класс 'expanded' у текущего элемента
            targetItem.classList.toggle('expanded');

            // Обновляем ARIA атрибут
            const isExpanded = targetItem.classList.contains('expanded');
            const header = targetItem.querySelector('.subject-item__header');
            if(header) header.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');

        });

        // Добавляем обработку нажатия Enter/Space для доступности
        subjectsList.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                const targetItem = event.target.closest('.subject-item.expandable');
                if (targetItem && document.activeElement === targetItem) { // Проверяем, что фокус на самом элементе
                    event.preventDefault(); // Предотвратить стандартное действие (прокрутка для Space)
                    targetItem.click(); // Имитировать клик
                }
            }
        });

        // Устанавливаем начальное состояние ARIA для всех заголовков
        const expandableHeaders = subjectsList.querySelectorAll('.subject-item.expandable .subject-item__header');
        expandableHeaders.forEach(header => {
            header.setAttribute('aria-expanded', 'false'); // Изначально все закрыты
            // Добавим роль кнопки для семантики (хотя сам item фокусируемый)
            header.setAttribute('role', 'button');
        });
    }

    // --- Modal Window Logic ---
    const loginModal = document.getElementById('loginModal');
    const openLoginButtons = document.querySelectorAll('.desktop-login-btn, .open-login-modal-btn'); // Добавлен новый класс
    const closeLoginButtons = document.querySelectorAll('.modal-close-btn, .modal-back-btn'); // Обе кнопки закрывают
    const modalOverlay = document.querySelector('.modal-overlay'); // Для клика вне окна

    let previouslyFocusedElement = null; // Для возврата фокуса

    // Функция открытия модального окна
    const openModal = () => {
        if (!loginModal) return; // Если модалки нет на странице

        previouslyFocusedElement = document.activeElement; // Запоминаем, откуда открыли

        loginModal.hidden = false;
        // Добавляем класс для показа и анимации
        // Небольшая задержка для срабатывания transition visibility
        requestAnimationFrame(() => {
            loginModal.classList.add('active');
        });

        document.body.style.overflow = 'hidden'; // Блокируем скролл фона

        // Фокус на первое поле ввода (улучшает доступность)
        const firstInput = loginModal.querySelector('input[type="email"], input[type="password"]');
        firstInput?.focus();
    };

    // Функция закрытия модального окна
    const closeModal = () => {
        if (!loginModal) return;

        loginModal.classList.remove('active');
        document.body.style.overflow = ''; // Восстанавливаем скролл фона

        // Прячем после анимации
        loginModal.addEventListener('transitionend', () => {
            if (!loginModal.classList.contains('active')) { // Убедимся, что оно еще не открыто снова
                loginModal.hidden = true;
            }
        }, { once: true }); // Событие сработает один раз

        // Возвращаем фокус на элемент, с которого открыли модалку
        previouslyFocusedElement?.focus();
    };

    // Открытие модалки по клику на кнопки "Войти"
    openLoginButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (button.closest('form') || (button.tagName === 'A' && !button.getAttribute('href')?.startsWith('#')) ) {
                return;
            }
            e.preventDefault(); // На случай если это <a>
            openModal();
        });
    });


    // Закрытие модалки по клику на кнопки "X" или "<-"
    closeLoginButtons.forEach(button => {
        button.addEventListener('click', closeModal);
    });


    // Закрытие модалки по клику на оверлей (вне контента)
    modalOverlay?.addEventListener('click', (event) => {
        // Закрываем, только если клик был точно на оверлее, а не на его дочерних элементах
        if (event.target === modalOverlay) {
            closeModal();
        }
    });

    // Закрытие модалки по нажатию клавиши Escape
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && loginModal && loginModal.classList.contains('active')) {
            closeModal();
        }
    });

    // --- Competition Filtering Logic ---
    const competitionsSection = document.getElementById('competitions');

    // Убедимся, что мы на странице/секции соревнований, прежде чем выполнять код фильтрации
    // (Если вы используете SPA, этот код может выполняться каждый раз при показе секции)
    // Простой вариант: проверять наличие элемента, специфичного для секции
    const filterTogglesContainer = competitionsSection?.querySelector('.filter-toggles');

    if (filterTogglesContainer) { // Запускаем логику фильтров, только если они есть на странице
        const filterButtons = filterTogglesContainer.querySelectorAll('.btn-filter');
        const regionSelect = competitionsSection.querySelector('#region-filter');
        const competitionItems = competitionsSection.querySelectorAll('.competition-item');
        const monthGroups = competitionsSection.querySelectorAll('.competitions-month-group');

        let currentTypeFilter = 'all'; // 'all', 'online', 'offline'
        let currentRegionFilter = 'all'; // 'all', 'msk', 'spb', ...

        // Функция для применения фильтров
        function applyCompetitionFilters() {
            // Обновляем состояние из активных элементов (на случай инициализации)
            const activeTypeButton = filterTogglesContainer.querySelector('.btn-filter.active');
            currentTypeFilter = activeTypeButton ? activeTypeButton.dataset.filter : 'all';
            currentRegionFilter = regionSelect ? regionSelect.value : 'all';

            competitionItems.forEach(item => {
                const itemType = item.dataset.eventType || 'unknown';
                const itemRegion = item.dataset.eventRegion || 'all';

                // Проверка соответствия фильтрам
                const typeMatch = (currentTypeFilter === 'all' || itemType === currentTypeFilter);
                // Регион "all" совпадает с любым регионом фильтра 'all',
                // также событие с регионом 'all' должно показываться для любого выбранного региона в фильтре (кроме случая когда тип - 'offline'?)
                // Упрощенная логика: событие видно если регион совпадает ИЛИ фильтр 'all' ИЛИ регион события 'all'
                // (Эта логика может потребовать уточнений под ваши бизнес-требования!)
                const regionMatch = (currentRegionFilter === 'all' || itemRegion === currentRegionFilter || itemRegion === 'all');

                // Показываем или скрываем элемент
                if (typeMatch && regionMatch) {
                    item.style.display = ''; // Показать (вернуть display по умолчанию)
                } else {
                    item.style.display = 'none'; // Скрыть
                }
            });

            updateEmptyMonthMessages();
        }

        // Функция для обновления сообщений "Нет соревнований"
        function updateEmptyMonthMessages() {
            monthGroups.forEach(group => {
                const visibleItems = group.querySelectorAll('.competition-item:not([style*="display: none"])'); // Ищем видимые элементы
                const emptyMessage = group.querySelector('.competition-item-empty');

                if (emptyMessage) {
                    if (visibleItems.length > 0) {
                        emptyMessage.style.display = 'none'; // Скрыть сообщение, если есть видимые события
                    } else {
                        emptyMessage.style.display = ''; // Показать сообщение, если видимых событий нет
                    }
                }
            });
        }

        // Обработчики событий для кнопок типа (Онлайн/Офлайн)
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Убираем класс active со всех кнопок
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // Добавляем класс active к нажатой кнопке
                button.classList.add('active');
                // Обновляем и применяем фильтры
                applyCompetitionFilters();
            });
        });

        // Обработчик событий для селекта региона
        if (regionSelect) {
            regionSelect.addEventListener('change', () => {
                // Обновляем и применяем фильтры
                applyCompetitionFilters();
            });
        }

        // --- Инициализация ---
        // Применить фильтры один раз при загрузке/показе секции
        applyCompetitionFilters();

    } // Конец if (filterTogglesContainer)


}); // Конец DOMContentLoaded

// Утилита Debounce: Вызывает функцию только после того,
// как прошло определенное время без вызовов.
function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// --- Кнопка Назад на странице деталей региона ---
const backButton = document.getElementById('backToRegionsBtn');
backButton?.addEventListener('click', () => {
    // Вариант 1: Простой возврат по истории
    history.back();

    // Вариант 2: Если хотите гарантированно вернуться на #regions (на случай если пришли не оттуда)
    // showSection('#regions'); // Ваша функция показа секции
    // history.pushState(null, '', '#regions'); // Обновить URL, если нужно
});