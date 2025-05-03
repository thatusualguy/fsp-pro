document.addEventListener('DOMContentLoaded', () => {

    // --- Код для Фильтрации Соревнований (из пред. ответа) ---
    // ... initializeCompetitionFilters(); ...

    // --- Код для Регион/Город (из пред. ответа) ---
    // ... regionSelect.addEventListener('change', ... ); ...

    // --- ОБНОВЛЕННАЯ / НОВАЯ Логика для Мобильного Сайдбара ---
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');       // Бургер кнопка
    const mobileSidebar = document.getElementById('mobileSidebar');       // Сам сайдбар
    const mobileSidebarCloseBtn = document.getElementById('mobileSidebarCloseBtn'); // Кнопка X
    const mobileSidebarOverlay = document.getElementById('mobileSidebarOverlay'); // Оверлей
    const body = document.body;

    // Функция Открытия Сайдбара
    function openMobileSidebar() {
        if (!mobileSidebar) return;
        mobileSidebar.hidden = false;
        // Небольшая задержка/пересчет для анимации transform
        requestAnimationFrame(() => {
             requestAnimationFrame(() => {
                  mobileSidebar.classList.add('active');
                  mobileSidebarOverlay.classList.add('active');
                  mobileSidebarOverlay.hidden = false;
                  body.style.overflow = 'hidden'; // Блокируем прокрутку
                  mobileMenuBtn?.setAttribute('aria-expanded', 'true'); // Обновляем бургер
             });
        });
        // Устанавливаем фокус на кнопку закрытия для доступности
        setTimeout(() => mobileSidebarCloseBtn?.focus(), 300); // Задержка для анимации
    }

    // Функция Закрытия Сайдбара
    function closeMobileSidebar() {
         if (!mobileSidebar) return;
        mobileSidebar.classList.remove('active');
        mobileSidebarOverlay.classList.remove('active');
        body.style.overflow = ''; // Восстанавливаем прокрутку

        // Прячем элементы после завершения анимации
        mobileSidebar.addEventListener('transitionend', () => {
            mobileSidebar.hidden = true;
        }, { once: true }); // Сработает только один раз

         mobileSidebarOverlay.addEventListener('transitionend', () => {
            mobileSidebarOverlay.hidden = true;
        }, { once: true });

        mobileMenuBtn?.setAttribute('aria-expanded', 'false'); // Обновляем бургер
         mobileMenuBtn?.focus(); // Возвращаем фокус на бургер
    }

    // --- Слушатели Событий ---

    // 1. Клик по Бургеру (Открытие)
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', openMobileSidebar);
    }

    // 2. Клик по Кнопке X (Закрытие)
    if (mobileSidebarCloseBtn) {
        mobileSidebarCloseBtn.addEventListener('click', closeMobileSidebar);
    }

    // 3. Клик по Оверлею (Закрытие)
    if (mobileSidebarOverlay) {
        mobileSidebarOverlay.addEventListener('click', closeMobileSidebar);
    }

    // 4. Закрытие при нажатии Esc (Доступность)
     document.addEventListener('keydown', (event) => {
         if (event.key === 'Escape' && mobileSidebar && mobileSidebar.classList.contains('active')) {
            closeMobileSidebar();
         }
     });

    // --- Доп. логика для подменю ---
     const submenuToggles = document.querySelectorAll('.mobile-sidebar-nav li.has-submenu > a');

     submenuToggles.forEach(toggle => {
        // Предотвращаем переход по основной ссылке, если есть подменю, чтобы только открывать его
         toggle.addEventListener('click', (event) => {
             const parentLi = toggle.parentElement;
             const submenu = parentLi?.querySelector('.submenu');

             if (submenu) { // Убеждаемся, что подменю есть
                 event.preventDefault(); // Отменить переход по ссылке
                 parentLi.classList.toggle('submenu-open');
            }
             // Если submenu нет, клик сработает как обычная ссылка
         });
     });

}); // Конец DOMContentLoaded