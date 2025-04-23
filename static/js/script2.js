$(document).ready(function() {
    // افزودن دسته‌بندی جدید
    $('#categoryForm').on('submit', function(e) {
        e.preventDefault();
        this.submit();
    });

    // باز کردن مودال ویرایش
    window.openEditModal = function(id, name, imageUrl) {
        $('#editCategoryForm').attr('action', `/categories/update/${id}/`);
        $('#editCategoryId').val(id);
        $('#editCategoryName').val(name);
        $('#editCategoryImagePreview').attr('src', imageUrl ? imageUrl : '');
        $('#editModal').fadeIn();
    }

    // بروزرسانی دسته‌بندی
    window.updateCategory = function() {
        $('#editCategoryForm').submit();
    }

    // // باز کردن مودال تایید حذف
    // window.openDeleteModal = function(id) {
    //     $('#confirmDeleteBtn').off('click').on('click', function() {
    //         deleteCategory(id);
    //     });
    //     $('#deleteModal').fadeIn();
    // }

    // حذف دسته‌بندی
   $(document).ready(function() {
    // باز کردن مودال تایید حذف
    window.openDeleteModal = function(id) {
        $('#deleteCategoryForm').attr('action', `/categories/delete/${id}/`);
        $('#deleteModal').fadeIn();
    }

    // بستن مودال‌ها
    window.closeModal = function(modalId) {
        $('#' + modalId).fadeOut();
    }

    // بستن مودال‌ها با کلیک بیرون از مودال
    $(window).on('click', function(event) {
        if ($(event.target).hasClass('modal')) {
            $(event.target).fadeOut();
        }
    });
});
});