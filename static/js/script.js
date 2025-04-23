function showInfo() {
    document.getElementById('infoModal').style.display = 'flex';
}

function makeCall() {
    window.location.href = 'tel:02112345678';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// بستن مودال با کلیک خارج از آن
window.onclick = function(event) {
    if (event.target.className === 'modal') {
        event.target.style.display = 'none';
    }
}

// انتخاب دسته‌بندی
const categoryButtons = document.querySelectorAll('.category-btn');
categoryButtons.forEach(button => {
    button.addEventListener('click', () => {
        categoryButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
    });
});

// اسکرول لمسی برای دسته‌بندی‌ها
const categoriesContainer = document.querySelector('.categories');
let isDown = false;
let startX;
let scrollLeft;

categoriesContainer.addEventListener('mousedown', (e) => {
    isDown = true;
    startX = e.pageX - categoriesContainer.offsetLeft;
    scrollLeft = categoriesContainer.scrollLeft;
});

categoriesContainer.addEventListener('mouseleave', () => {
    isDown = false;
});

categoriesContainer.addEventListener('mouseup', () => {
    isDown = false;
});

categoriesContainer.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - categoriesContainer.offsetLeft;
    const walk = (x - startX) * 2;
    categoriesContainer.scrollLeft = scrollLeft - walk;
});
document.addEventListener('DOMContentLoaded', function () {
    const categoryButtons = document.querySelectorAll('.category-btn');
    const products = document.querySelectorAll('.menu-item');

    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const categoryId = button.dataset.categoryId;
            products.forEach(product => {
                if (product.dataset.categoryId === categoryId || categoryId === 'all') {
                    product.style.display = 'block';
                } else if (categoryId === 'all') {
                    product.style.display = 'block';
                } else {
                    product.style.display = 'none';
                }
            });
        });
    });
});

// document.querySelector('.hamburger-menu').addEventListener('click', function() {
//     var nav = document.querySelector('nav');
//
//     if (nav.style.display === 'block') {
//         nav.style.display = 'none';
//     } else {
//         nav.style.display = 'block';
//     }
// });



document.querySelector('.hamburger-menu').addEventListener('click', toggleMenu);

function toggleMenu() {
    var nav = document.querySelector('nav');

    if (nav.style.display === 'block') {
        nav.style.display = 'none';
    } else {
        nav.style.display = 'block';
    }
}

